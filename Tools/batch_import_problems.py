#!/usr/bin/env python3
"""Import multiple Markdown-formatted problems through the LPOJ HTTP API.

The input is split on level-1 headings.  Each problem uses level-2 headings for
its statement sections.  The default is a dry run; add --commit only after the
parsed preview looks correct.
"""

from __future__ import annotations

import argparse
import getpass
import hashlib
import json
import re
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, Iterable, List, Optional, Sequence, Tuple

import requests


FIELD_ALIASES = {
    "题目描述": "des",
    "问题描述": "des",
    "描述": "des",
    "description": "des",
    "输入": "input",
    "输入格式": "input",
    "输入说明": "input",
    "input": "input",
    "输出": "output",
    "输出格式": "output",
    "输出说明": "output",
    "output": "output",
    "提示": "hint",
    "说明": "hint",
    "备注": "hint",
    "hint": "hint",
    "模板": "template",
    "代码模板": "template",
    "template": "template",
}

META_ALIASES = {
    "题号": "problem",
    "编号": "problem",
    "problem": "problem",
    "id": "problem",
    "标题": "title",
    "title": "title",
    "作者": "author",
    "author": "author",
    "来源": "source",
    "source": "source",
    "oj": "oj",
    "时间限制": "time",
    "时间": "time",
    "time": "time",
    "内存限制": "memory",
    "内存": "memory",
    "memory": "memory",
    "权限": "auth",
    "可见性": "auth",
    "auth": "auth",
    "难度": "level",
    "level": "level",
    "分值": "score",
    "score": "score",
    "标签": "tag",
    "tags": "tag",
    "tag": "tag",
}

AUTH_VALUES = {"公开": 1, "public": 1, "私密": 2, "private": 2, "比赛": 3, "contest": 3}
HEADING_RE = re.compile(r"(?m)^#\s+(.+?)\s*$")
SECTION_RE = re.compile(r"(?m)^##\s+(.+?)\s*$")
META_RE = re.compile(r"^\s*(?:[-*]\s*)?([^:：]+?)\s*[:：]\s*(.*?)\s*$")
SAMPLE_INPUT_RE = re.compile(r"^(?:样例|示例|sample)\s*(?:输入|input)\s*(\d*)$", re.I)
SAMPLE_OUTPUT_RE = re.compile(r"^(?:样例|示例|sample)\s*(?:输出|output)\s*(\d*)$", re.I)


class ImportErrorDetail(Exception):
    pass


@dataclass
class ParsedProblem:
    detail: Dict[str, object]
    summary: Dict[str, object]

    @property
    def problem_id(self) -> str:
        return str(self.detail["problem"])


def clean_block(text: str) -> str:
    text = text.strip()
    match = re.fullmatch(r"```[^\n]*\n(.*?)\n?```", text, re.S)
    return match.group(1).strip("\n") if match else text


def normalize_name(value: str) -> str:
    return re.sub(r"[\s_-]+", "", value.strip()).lower()


def parse_number(value: object, field: str, problem_id: str) -> int:
    match = re.search(r"-?\d+", str(value))
    if not match:
        raise ImportErrorDetail(f"题目 {problem_id} 的 {field} 不是整数：{value!r}")
    return int(match.group())


def parse_auth(value: object, problem_id: str) -> int:
    normalized = str(value).strip().lower()
    if normalized in AUTH_VALUES:
        return AUTH_VALUES[normalized]
    result = parse_number(value, "auth", problem_id)
    if result not in (1, 2, 3):
        raise ImportErrorDetail(f"题目 {problem_id} 的 auth 必须是 1、2 或 3")
    return result


def split_documents(text: str) -> Iterable[Tuple[str, str]]:
    matches = list(HEADING_RE.finditer(text))
    if not matches:
        raise ImportErrorDetail("没有找到一级标题；每道题必须以 '# 题号 标题' 开始")
    prefix = text[: matches[0].start()].strip()
    if prefix and not prefix.startswith("<!--"):
        raise ImportErrorDetail("第一道题之前存在无法识别的内容")
    for index, match in enumerate(matches):
        end = matches[index + 1].start() if index + 1 < len(matches) else len(text)
        yield match.group(1).strip(), text[match.end() : end].strip()


def parse_metadata(lines: Sequence[str]) -> Tuple[Dict[str, str], str]:
    metadata: Dict[str, str] = {}
    body_start = 0
    for index, line in enumerate(lines):
        if line.startswith("## "):
            body_start = index
            break
        if not line.strip() or line.strip() == "---":
            continue
        match = META_RE.match(line)
        if not match:
            body_start = index
            break
        key = META_ALIASES.get(normalize_name(match.group(1)))
        if key:
            metadata[key] = match.group(2).strip()
        body_start = index + 1
    return metadata, "\n".join(lines[body_start:]).strip()


def parse_title(heading: str, metadata: Dict[str, str]) -> Tuple[str, str]:
    # Accepted examples: "1001 A+B", "1001. A+B", "[1001] A+B".
    match = re.match(r"^\[?([\w.-]+)\]?\s*(?:[.、:：-]\s*)?(.*)$", heading)
    problem_id = metadata.get("problem")
    title = metadata.get("title")
    if match:
        if not problem_id:
            problem_id = match.group(1)
            title = title or match.group(2).strip()
        elif not title:
            # If metadata supplies the ID, the H1 may be either "ID title" or
            # simply "title".
            title = match.group(2).strip() if match.group(1) == str(problem_id) else heading.strip()
    if not problem_id:
        raise ImportErrorDetail(f"无法从一级标题解析题号：{heading!r}")
    if not title:
        raise ImportErrorDetail(f"题目 {problem_id} 缺少标题")
    return str(problem_id), title


def parse_sections(body: str) -> Tuple[Dict[str, str], List[str], List[str]]:
    matches = list(SECTION_RE.finditer(body))
    sections: Dict[str, str] = {}
    sample_inputs: List[Tuple[str, str]] = []
    sample_outputs: List[Tuple[str, str]] = []
    for index, match in enumerate(matches):
        end = matches[index + 1].start() if index + 1 < len(matches) else len(body)
        name = normalize_name(match.group(1))
        content = clean_block(body[match.end() : end])
        input_match = SAMPLE_INPUT_RE.match(name)
        output_match = SAMPLE_OUTPUT_RE.match(name)
        if input_match:
            sample_inputs.append((input_match.group(1), content))
        elif output_match:
            sample_outputs.append((output_match.group(1), content))
        elif name in FIELD_ALIASES:
            sections[FIELD_ALIASES[name]] = content
    sample_inputs.sort(key=lambda item: int(item[0] or 0))
    sample_outputs.sort(key=lambda item: int(item[0] or 0))
    return sections, [x[1] for x in sample_inputs], [x[1] for x in sample_outputs]


def normalize_tags(value: object) -> str:
    tags = [item.strip() for item in re.split(r"[|,，;；]", str(value)) if item.strip()]
    return "|".join(dict.fromkeys(tags))


def parse_problem(heading: str, raw_body: str, defaults: argparse.Namespace) -> ParsedProblem:
    metadata, body = parse_metadata(raw_body.splitlines())
    problem_id, title = parse_title(heading, metadata)
    sections, sample_inputs, sample_outputs = parse_sections(body)
    required = ("des", "input", "output")
    missing = [field for field in required if not sections.get(field)]
    if missing:
        raise ImportErrorDetail(f"题目 {problem_id} 缺少章节：{', '.join(missing)}")
    if len(sample_inputs) != len(sample_outputs):
        raise ImportErrorDetail(
            f"题目 {problem_id} 的样例输入数（{len(sample_inputs)}）和输出数（{len(sample_outputs)}）不同"
        )

    detail: Dict[str, object] = {
        "problem": problem_id,
        "author": metadata.get("author", defaults.author),
        "oj": metadata.get("oj", defaults.oj),
        "title": title,
        "des": sections["des"],
        "input": sections["input"],
        "output": sections["output"],
        "sinput": "|#)".join(sample_inputs),
        "soutput": "|#)".join(sample_outputs),
        "source": metadata.get("source", defaults.source),
        "time": parse_number(metadata.get("time", defaults.time), "time", problem_id),
        "memory": parse_number(metadata.get("memory", defaults.memory), "memory", problem_id),
        "hint": sections.get("hint", ""),
        "auth": parse_auth(metadata.get("auth", defaults.auth), problem_id),
        # The model has a non-blank template field even for ordinary problems.
        "template": sections.get("template") or "请删除这行",
    }
    summary: Dict[str, object] = {
        "problem": problem_id,
        "title": title,
        "level": parse_number(metadata.get("level", defaults.level), "level", problem_id),
        "tag": normalize_tags(metadata.get("tag", defaults.tags)),
        "score": parse_number(metadata.get("score", defaults.score), "score", problem_id),
        "auth": detail["auth"],
        "oj": detail["oj"],
    }
    return ParsedProblem(detail, summary)


def parse_file(path: Path, defaults: argparse.Namespace) -> List[ParsedProblem]:
    text = path.read_text(encoding="utf-8-sig")
    problems = [parse_problem(heading, body, defaults) for heading, body in split_documents(text)]
    ids = [problem.problem_id for problem in problems]
    duplicates = sorted({problem_id for problem_id in ids if ids.count(problem_id) > 1})
    if duplicates:
        raise ImportErrorDetail("输入文件内题号重复：" + ", ".join(duplicates))
    return problems


class LPOJClient:
    def __init__(self, base_url: str, timeout: float) -> None:
        self.base_url = base_url.rstrip("/") + "/"
        self.timeout = timeout
        self.session = requests.Session()
        self.session.headers.update({"User-Agent": "LPOJ-Batch-Problem-Importer/1.0"})

    def url(self, path: str) -> str:
        return self.base_url + path.lstrip("/")

    def request(self, method: str, path: str, **kwargs: object) -> requests.Response:
        try:
            response = self.session.request(method, self.url(path), timeout=self.timeout, **kwargs)
        except requests.RequestException as exc:
            raise ImportErrorDetail(f"请求 {path} 失败：{exc}") from exc
        if not response.ok:
            try:
                detail = json.dumps(response.json(), ensure_ascii=False)
            except ValueError:
                detail = response.text[:500]
            raise ImportErrorDetail(f"{method} {path} 返回 HTTP {response.status_code}：{detail}")
        return response

    def login(self, username: str, password: str, password_is_md5: bool) -> None:
        encoded = password if password_is_md5 else hashlib.md5(password.encode("utf-8")).hexdigest()
        response = self.request("POST", "login/", json={"username": username, "password": encoded})
        data = response.json()
        if isinstance(data, str) and data in {"usererror", "passworderror", "error"}:
            messages = {
                "usererror": "用户不存在",
                "passworderror": "密码错误",
                "error": "用户数据错误",
            }
            raise ImportErrorDetail(f"登录失败：{messages[data]}")
        if isinstance(data, dict) and data.get("status") in {"usererror", "passworderror", "error"}:
            raise ImportErrorDetail(f"登录失败：{data.get('message', data['status'])}")
        if not isinstance(data, dict) or int(data.get("type", 1)) not in (2, 3):
            raise ImportErrorDetail("登录账号不是教师或管理员，不能添加题目")

    def exists(self, resource: str, problem_id: str) -> bool:
        response = self.session.get(self.url(f"{resource}/{problem_id}/"), timeout=self.timeout)
        if response.status_code == 404:
            return False
        if not response.ok:
            raise ImportErrorDetail(f"检查 {resource}/{problem_id} 失败：HTTP {response.status_code}")
        return True

    def write_resource(self, resource: str, problem_id: str, payload: Dict[str, object], existing: str) -> str:
        found = self.exists(resource, problem_id)
        if found and existing == "skip":
            return "skipped"
        if found and existing == "error":
            raise ImportErrorDetail(f"{resource}/{problem_id} 已存在（可使用 --existing update 或 skip）")
        if found:
            self.request("PATCH", f"{resource}/{problem_id}/", json=payload)
            return "updated"
        self.request("POST", f"{resource}/", json=payload)
        return "created"

    def ensure_tags(self, tags: str) -> None:
        for tag in filter(None, tags.split("|")):
            response = self.session.get(self.url("problemtag/"), params={"tagname": tag}, timeout=self.timeout)
            if not response.ok:
                raise ImportErrorDetail(f"检查标签 {tag!r} 失败：HTTP {response.status_code}")
            data = response.json()
            results = data.get("results", []) if isinstance(data, dict) else data
            if not any(item.get("tagname") == tag for item in results):
                self.request("POST", "problemtag/", json={"tagname": tag, "count": 1})

    def upload_data(self, problem_id: str, data_dir: Path) -> List[str]:
        uploaded: List[str] = []
        for suffix in (".zip", ".jpg"):
            path = data_dir / f"{problem_id}{suffix}"
            if path.is_file():
                with path.open("rb") as file_handle:
                    self.request("POST", "uploadfile/", files={"file": (path.name, file_handle)})
                uploaded.append(path.name)
        return uploaded


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="从一个 Markdown/TXT 文件批量导入 LPOJ 题目")
    parser.add_argument("input", type=Path, help="UTF-8 编码的 Markdown/TXT 文件")
    parser.add_argument("--base-url", default="http://localhost:8080/api/", help="API 根地址")
    parser.add_argument("--username", help="教师或管理员用户名；--commit 时必填")
    parser.add_argument("--password", help="不建议在共享终端使用；省略时安全提示输入")
    parser.add_argument("--password-is-md5", action="store_true", help="提供的密码已经是 MD5")
    parser.add_argument("--commit", action="store_true", help="真正调用 API；默认只解析预览")
    parser.add_argument("--existing", choices=("error", "skip", "update"), default="error")
    parser.add_argument("--continue-on-error", action="store_true", help="单题失败后继续处理后面的题")
    parser.add_argument("--data-dir", type=Path, help="可选：上传其中的 <题号>.zip 和 <题号>.jpg")
    parser.add_argument("--timeout", type=float, default=20.0)
    parser.add_argument("--author", default="admin")
    parser.add_argument("--oj", default="LPOJ")
    parser.add_argument("--source", default="LPOJ")
    parser.add_argument("--time", type=int, default=1000)
    parser.add_argument("--memory", type=int, default=64)
    parser.add_argument("--auth", default="2")
    parser.add_argument("--level", type=int, default=3)
    parser.add_argument("--score", type=int, default=100)
    parser.add_argument("--tags", default="")
    return parser


def preview(problems: Sequence[ParsedProblem]) -> None:
    print(f"解析成功：{len(problems)} 道题")
    for problem in problems:
        print(
            f"  {problem.problem_id}: {problem.detail['title']} | "
            f"time={problem.detail['time']}ms memory={problem.detail['memory']}MB "
            f"auth={problem.detail['auth']} tags={problem.summary['tag'] or '-'}"
        )


def main(argv: Optional[Sequence[str]] = None) -> int:
    args = build_parser().parse_args(argv)
    try:
        problems = parse_file(args.input, args)
        preview(problems)
        if not args.commit:
            print("预览模式：未调用 API。确认无误后加 --commit。")
            return 0
        if not args.username:
            raise ImportErrorDetail("--commit 时必须提供 --username")
        if args.data_dir and not args.data_dir.is_dir():
            raise ImportErrorDetail(f"数据目录不存在：{args.data_dir}")

        password = args.password
        if password is None:
            password = getpass.getpass("LPOJ 密码：")
        client = LPOJClient(args.base_url, args.timeout)
        client.login(args.username, password, args.password_is_md5)

        # Detect every conflict before the first write under the default policy.
        if args.existing == "error":
            conflicts: List[str] = []
            for problem in problems:
                for resource in ("problem", "problemdata"):
                    if client.exists(resource, problem.problem_id):
                        conflicts.append(f"{resource}/{problem.problem_id}")
            if conflicts:
                raise ImportErrorDetail(
                    "以下记录已经存在，尚未写入任何题目："
                    + ", ".join(conflicts)
                    + "（可使用 --existing update 或 skip）"
                )

        successes = 0
        failures: List[Tuple[str, str]] = []
        for problem in problems:
            try:
                detail_action = client.write_resource("problem", problem.problem_id, problem.detail, args.existing)
                summary_action = client.write_resource("problemdata", problem.problem_id, problem.summary, args.existing)
                client.ensure_tags(str(problem.summary["tag"]))
                uploaded = client.upload_data(problem.problem_id, args.data_dir) if args.data_dir else []
                successes += 1
                upload_text = f"，上传 {', '.join(uploaded)}" if uploaded else ""
                print(f"[成功] {problem.problem_id}: problem={detail_action}, problemdata={summary_action}{upload_text}")
            except ImportErrorDetail as exc:
                failures.append((problem.problem_id, str(exc)))
                print(f"[失败] {problem.problem_id}: {exc}", file=sys.stderr)
                if not args.continue_on_error:
                    break

        print(f"完成：成功 {successes}，失败 {len(failures)}")
        return 1 if failures else 0
    except (OSError, UnicodeError, ImportErrorDetail, ValueError) as exc:
        print(f"错误：{exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
