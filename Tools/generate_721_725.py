#!/usr/bin/env python3
"""Generate the Markdown statements and judge ZIPs for LPOJ 721--725."""

from decimal import Decimal
from pathlib import Path
from zipfile import ZIP_DEFLATED, ZipFile


ROOT = Path(__file__).resolve().parent / "import_721_725"
DATA_DIR = ROOT / "data"


PROBLEMS = {
    "721": {
        "title": "进口成本与销售估算",
        "score": 10,
        "level": 1,
        "tags": "顺序结构|浮点数|格式化输出",
        "description": """某电商平台进口一批商品，已知单件商品的采购价（外币）、当日汇率、进口关税比例以及预期的利润率。请计算：

1. 单件商品的采购成本（人民币）；
2. 包含关税后的总成本，其中总成本 = 采购成本 × (1 + 关税比例)；
3. 建议销售价，其中建议销售价 = 总成本 × (1 + 利润率)。

所有金额均保留 2 位小数。""",
        "input": """共 3 行：

第 1 行为采购价（外币，浮点数）；第 2 行为外币兑人民币汇率（浮点数）；第 3 行为关税比例与利润率，以空格分隔，例如 `0.15 0.25` 表示 15% 关税和 25% 利润率。

所有输入数据均为非负数。""",
        "output": """共 3 行，格式如下：

`采购成本：XXX.XX元`

`含税总成本：XXX.XX元`

`建议销售价：XXX.XX元`""",
        "sample_in": "50.00\n7.20\n0.10 0.30",
        "sample_out": "采购成本：360.00元\n含税总成本：396.00元\n建议销售价：514.80元",
        "hint": "计算时不要手动添加千位分隔符。",
    },
    "722": {
        "title": "阶梯物流费用计算",
        "score": 10,
        "level": 2,
        "tags": "分支结构|浮点数|格式化输出",
        "description": """某跨境物流公司根据包裹重量（kg）计费，收费标准如下：

| 重量区间 | 收费标准 | 输出档次文字 |
| --- | --- | --- |
| 重量 ≤ 2kg | 固定收费 50 元 | `2kg及以下档` |
| 2kg < 重量 ≤ 10kg | 50 元 + 超过 2kg 部分按 15 元/kg | `2kg-10kg档` |
| 10kg < 重量 ≤ 30kg | 170 元 + 超过 10kg 部分按 12 元/kg | `10kg-30kg档` |
| 重量 > 30kg | 410 元 + 超过 30kg 部分按 10 元/kg | `30kg以上档` |

请输出收费档次及总费用。""",
        "input": "一行，一个大于 0 的浮点数，表示包裹重量（kg）。",
        "output": """共 2 行，格式如下：

`计费档次：XXX`

`物流总费用：XXX.XX元`

费用保留 2 位小数。""",
        "sample_in": "15.5",
        "sample_out": "计费档次：10kg-30kg档\n物流总费用：236.00元",
        "hint": "区间端点 2、10、30 分别属于其左侧收费档次。",
    },
    "723": {
        "title": "资产折旧计算",
        "score": 15,
        "level": 2,
        "tags": "循环结构|浮点数|格式化输出",
        "description": """某公司购置一台价值为 P 的设备，预计使用 8 年。本题采用固定比例折旧法：每年末的设备余值等于上年末余值乘以 `(1 - 折旧率)`。

请逐年输出第 1 年至第 8 年末的设备余值。计算过程中不进行中间舍入，仅在输出每一行时保留 2 位小数。""",
        "input": """共 2 行：第 1 行为设备原值（人民币，正浮点数）；第 2 行为年折旧率 r，满足 `0 ≤ r ≤ 1`。""",
        "output": "逐年输出 8 行，格式为：`第X年末设备余值：¥XXX.XX`。",
        "sample_in": "50000\n0.15",
        "sample_out": """第1年末设备余值：¥42500.00
第2年末设备余值：¥36125.00
第3年末设备余值：¥30706.25
第4年末设备余值：¥26100.31
第5年末设备余值：¥22185.27
第6年末设备余值：¥18857.48
第7年末设备余值：¥16028.85
第8年末设备余值：¥13624.53""",
        "hint": "原题示例中的第 8 年数值有计算误差；按题目公式计算应为 ¥13624.53。",
    },
    "724": {
        "title": "每日客流量数据分析",
        "score": 15,
        "level": 2,
        "tags": "列表|循环结构|数据统计",
        "description": """给定某零售店一周（周一至周日）的每日客流量，请依次完成以下分析：

1. 计算全周总客流量与日均客流量，日均值只保留整数部分；
2. 输出客流量最高和最低的日期，周一为第 1 天；
3. 输出所有客流量严格低于日均值的日期编号。

若最高值或最低值在多天出现，输出其中日期编号最小的一天。""",
        "input": "一行 7 个非负整数，以空格分隔，依次为周一至周日的客流量。",
        "output": """共 4 行，格式如下：

`总客流量：XXX 人次，日均：XXX 人次`

`最高日期：第 X 天（XXX 人次）`

`最低日期：第 X 天（XXX 人次）`

`低于日均的日期：X X X`

若没有低于日均的日期，第四行冒号后不输出日期编号。""",
        "sample_in": "120 150 110 180 210 320 280",
        "sample_out": "总客流量：1370 人次，日均：195 人次\n最高日期：第 6 天（320 人次）\n最低日期：第 3 天（110 人次）\n低于日均的日期：1 2 3 4",
        "hint": "本题输入均为非负整数，日均值等于总客流量除以 7 后向下取整。",
    },
    "725": {
        "title": "图书库存查询与管理",
        "score": 10,
        "level": 2,
        "tags": "字典|字符串|模拟",
        "description": """书店用字典记录每本书的库存数量。请依次完成：

1. 读入 4 本书的初始库存；
2. 办理一次入库：增加指定图书的库存，若图书不存在则新增；
3. 办理一次出库：减少指定图书的库存。若图书不存在，输出 `图书不存在`；若库存不足，输出 `库存不足`；否则完成出库；
4. 输出所有图书及其最终库存。

最终库存按图书加入字典的先后顺序输出：先输出最初的 4 本书，新入库的图书放在最后。失败的出库操作不改变库存。""",
        "input": """共 6 行。前 4 行格式为 `书名 库存量`；第 5 行格式为 `入库 书名 数量`；第 6 行格式为 `出库 书名 数量`。

书名不包含空白字符，库存量和操作数量均为非负整数，最初的 4 个书名互不相同。""",
        "output": """第 1 行输出入库结果 `入库成功`。第 2 行输出出库结果：`出库成功`、`图书不存在` 或 `库存不足`。

之后每行按 `书名：库存` 格式输出所有图书及其最终库存。冒号为中文全角冒号 `：`。""",
        "sample_in": """Python基础 10
数据分析 5
机器学习 3
算法导论 8
入库 Python基础 5
出库 数据分析 10""",
        "sample_out": """入库成功
库存不足
Python基础：15
数据分析：5
机器学习：3
算法导论：8""",
        "hint": "当出库数量恰好等于当前库存时，操作成功，最终库存为 0。",
    },
}


EXTRA_INPUTS = {
    "721": [
        "100\n6.50\n0.10 0.20",
        "80\n7.50\n0.20 0.25",
        "1\n1.25\n0 0",
        "200\n7.00\n0.05 0.10",
        "125\n6.40\n0.15 0.25",
    ],
    "722": ["2", "10", "30", "45.75", "5.2"],
    "723": ["10000\n0.10", "8000\n0", "1000\n0.50", "25000\n0.20", "64000\n0.25"],
    "724": [
        "100 100 100 100 100 100 100",
        "10 20 30 40 50 60 70",
        "70 60 50 40 30 20 10",
        "1 2 3 4 5 6 8",
        "100 200 200 50 50 150 50",
    ],
    "725": [
        """红楼梦 5
西游记 6
三国演义 7
水浒传 8
入库 新华字典 3
出库 不存在的书 1""",
        """A 1
B 2
C 3
D 4
入库 A 9
出库 D 2""",
        """甲 10
乙 20
丙 30
丁 40
入库 戊 5
出库 戊 5""",
        """编程入门 0
数据库 12
计算机网络 7
操作系统 9
入库 编程入门 2
出库 数据库 12""",
        """Book1 100
Book2 1
Book3 0
Book4 25
入库 Book5 10
出库 Book2 2""",
    ],
}


def money(value: Decimal) -> str:
    return f"{value:.2f}"


def solve_721(text: str) -> str:
    lines = text.splitlines()
    price, rate = Decimal(lines[0]), Decimal(lines[1])
    duty, profit = map(Decimal, lines[2].split())
    cost = price * rate
    taxed = cost * (Decimal(1) + duty)
    sale = taxed * (Decimal(1) + profit)
    return f"采购成本：{money(cost)}元\n含税总成本：{money(taxed)}元\n建议销售价：{money(sale)}元"


def solve_722(text: str) -> str:
    weight = Decimal(text.strip())
    if weight <= 2:
        tier, fee = "2kg及以下档", Decimal(50)
    elif weight <= 10:
        tier, fee = "2kg-10kg档", Decimal(50) + (weight - 2) * 15
    elif weight <= 30:
        tier, fee = "10kg-30kg档", Decimal(170) + (weight - 10) * 12
    else:
        tier, fee = "30kg以上档", Decimal(410) + (weight - 30) * 10
    return f"计费档次：{tier}\n物流总费用：{money(fee)}元"


def solve_723(text: str) -> str:
    original, depreciation = map(Decimal, text.split())
    values = []
    current = original
    for year in range(1, 9):
        current *= Decimal(1) - depreciation
        values.append(f"第{year}年末设备余值：¥{money(current)}")
    return "\n".join(values)


def solve_724(text: str) -> str:
    visits = list(map(int, text.split()))
    total = sum(visits)
    average = total // 7
    maximum, minimum = max(visits), min(visits)
    max_day, min_day = visits.index(maximum) + 1, visits.index(minimum) + 1
    below = " ".join(str(index + 1) for index, value in enumerate(visits) if value < average)
    return (
        f"总客流量：{total} 人次，日均：{average} 人次\n"
        f"最高日期：第 {max_day} 天（{maximum} 人次）\n"
        f"最低日期：第 {min_day} 天（{minimum} 人次）\n"
        f"低于日均的日期：{below}"
    )


def solve_725(text: str) -> str:
    lines = text.splitlines()
    inventory = {}
    for line in lines[:4]:
        name, count = line.split()
        inventory[name] = int(count)
    _, incoming_name, incoming_count = lines[4].split()
    inventory[incoming_name] = inventory.get(incoming_name, 0) + int(incoming_count)
    _, outgoing_name, outgoing_count = lines[5].split()
    outgoing_count = int(outgoing_count)
    if outgoing_name not in inventory:
        outgoing_result = "图书不存在"
    elif inventory[outgoing_name] < outgoing_count:
        outgoing_result = "库存不足"
    else:
        inventory[outgoing_name] -= outgoing_count
        outgoing_result = "出库成功"
    rows = ["入库成功", outgoing_result]
    rows.extend(f"{name}：{count}" for name, count in inventory.items())
    return "\n".join(rows)


SOLVERS = {
    "721": solve_721,
    "722": solve_722,
    "723": solve_723,
    "724": solve_724,
    "725": solve_725,
}


def render_markdown() -> str:
    chunks = []
    for problem_id, problem in PROBLEMS.items():
        chunks.append(
            f"""# {problem_id} {problem['title']}

- 作者：admin
- 来源：课程练习
- OJ：LPOJ
- 时间限制：1000 ms
- 内存限制：64 MB
- 权限：公开
- 难度：{problem['level']}
- 分值：{problem['score']}
- 标签：{problem['tags']}

## 题目描述

{problem['description']}

## 输入格式

{problem['input']}

## 输出格式

{problem['output']}

## 样例输入 1

```text
{problem['sample_in']}
```

## 样例输出 1

```text
{problem['sample_out']}
```

## 提示

{problem['hint']}
"""
        )
    return "\n".join(chunks)


def main() -> None:
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    (ROOT / "problems.md").write_text(render_markdown(), encoding="utf-8")
    for problem_id, problem in PROBLEMS.items():
        inputs = [problem["sample_in"], *EXTRA_INPUTS[problem_id]]
        outputs = [SOLVERS[problem_id](case) for case in inputs]
        assert outputs[0] == problem["sample_out"], f"sample mismatch for {problem_id}"
        zip_path = DATA_DIR / f"{problem_id}.zip"
        with ZipFile(zip_path, "w", ZIP_DEFLATED) as archive:
            for index, (case_input, case_output) in enumerate(zip(inputs, outputs), start=1):
                archive.writestr(f"{index}.in", case_input.rstrip("\n") + "\n")
                archive.writestr(f"{index}.out", case_output.rstrip("\n") + "\n")
        print(f"generated {zip_path}: {len(inputs)} cases")


if __name__ == "__main__":
    main()
