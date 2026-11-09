# LPOJ 中文评测问题修复指南

## 问题描述

当测试数据包含中文字符时，评测程序会出错。

## 根本原因

Python 3 的 `open()` 函数在不指定 `encoding` 参数时，会使用系统默认编码（通常是 locale.getpreferredencoding()）。在某些系统上，默认编码可能是 ASCII 或其他非 UTF-8 编码，导致读取包含中文的文件时抛出 `UnicodeDecodeError` 异常。

## 修复内容

已在 `Judger/main.py` 中修复了以下所有文件读取操作，全部添加了 `encoding='utf-8'`：

### 1. 配置文件读取（Line 58, 75）
```python
# 修复前
myjsonfile = open("./setting.json", 'r')
datajsonfile = open("./datatime.json", 'r')

# 修复后
myjsonfile = open("./setting.json", 'r', encoding='utf-8')
datajsonfile = open("./datatime.json", 'r', encoding='utf-8')
```

### 2. 编译错误信息读取（Line 505, 525, 575, 594）
```python
# 修复前
filece = open("%sce.txt" % judgername, "r")

# 修复后
filece = open("%sce.txt" % judgername, "r", encoding='utf-8')
```

适用于：
- C 编译错误 (Line 505)
- C++ 编译错误 (Line 525)
- Java 编译错误 (Line 575)
- Swift 编译错误 (Line 594)

### 3. 测试数据读取（Line 895-911）
```python
# 修复前
inputfile = open("./ProblemData/%s/%s.in" % (problem, filename), "r")
outputfile = open("./ProblemData/%s/%s.out" % (problem, filename), "r")
useroutputfile = open(GlobalVar.judgername+"temp.out", "r")

# 修复后
inputfile = open("./ProblemData/%s/%s.in" % (problem, filename), "r", encoding='utf-8')
outputfile = open("./ProblemData/%s/%s.out" % (problem, filename), "r", encoding='utf-8')
useroutputfile = open(GlobalVar.judgername+"temp.out", "r", encoding='utf-8')
```

### 4. 输出文件比较（Line 995-997）
```python
# 修复前
file1 = open(GlobalVar.judgername+"temp.out", "r")
file2 = open("./ProblemData/%s/%s.out" % (problem, filename), "r")

# 修复后
file1 = open(GlobalVar.judgername+"temp.out", "r", encoding='utf-8')
file2 = open("./ProblemData/%s/%s.out" % (problem, filename), "r", encoding='utf-8')
```

### 5. Special Judge 消息读取（Line 988）
```python
# 已有正确编码
tmsg = open("./spjmsg.txt", "r", encoding='utf-8')
```

### 6. 测试用例描述读取（Line 819）
```python
# 已有正确编码
file3 = open("./ProblemData/%s/casedes.txt" % problem, "r", encoding='utf-8')
```

## 部署步骤

### 方法 1: 使用自动化脚本（推荐）

1. 将修复后的代码同步到服务器 10.188.2.252
2. SSH 登录到服务器：
   ```bash
   ssh zq@10.188.2.252
   ```

3. 进入项目目录：
   ```bash
   cd /home/lzc/LPOJ
   ```

4. 运行修复脚本：
   ```bash
   ./fix_chinese_encoding.sh
   ```

### 方法 2: 手动部署

1. SSH 登录到服务器：
   ```bash
   ssh zq@10.188.2.252
   ```

2. 进入项目目录：
   ```bash
   cd /home/lzc/LPOJ
   ```

3. 停止 judger 服务：
   ```bash
   sudo docker-compose stop judger
   ```

4. 验证修复是否已应用：
   ```bash
   grep -n "encoding='utf-8'" Judger/main.py | head -10
   ```
   应该看到多个包含 `encoding='utf-8'` 的行。

5. 重新构建 judger 镜像：
   ```bash
   sudo docker-compose -f docker-compose-build.yml build judger
   ```

6. 启动 judger 服务（3个实例）：
   ```bash
   sudo docker-compose -f docker-compose-build.yml up -d --scale judger=3
   ```

7. 检查服务状态：
   ```bash
   sudo docker-compose ps judger
   ```

8. 查看日志确认启动成功：
   ```bash
   sudo docker-compose logs judger --tail 50
   ```

## 验证修复

### 测试用例 1: 中文输入输出

创建一个简单的测试题目：

**输入文件 (1.in):**
```
你好世界
```

**输出文件 (1.out):**
```
你好世界
```

**测试代码 (C++):**
```cpp
#include <iostream>
#include <string>
using namespace std;

int main() {
    string s;
    getline(cin, s);
    cout << s << endl;
    return 0;
}
```

提交后，应该显示 "Accepted"。

### 测试用例 2: 中文编译错误

提交一个有语法错误的代码，检查编译错误信息是否正常显示（不会因为中文路径或消息而崩溃）。

## 故障排查

### 问题 1: 容器无法启动

**检查日志：**
```bash
sudo docker-compose logs judger --tail 100
```

**可能原因：**
- Python 依赖问题：检查 requirements.txt
- 端口冲突：检查其他 judger 实例是否已停止

### 问题 2: 仍然出现编码错误

**进入容器检查：**
```bash
# 找到运行中的 judger 容器
sudo docker-compose ps judger

# 进入容器
sudo docker-compose exec judger bash

# 检查修复是否生效
grep -n "encoding='utf-8'" /Judger/main.py | wc -l
# 应该显示 10 或更多

# 检查 Python 默认编码
python3 -c "import locale; print(locale.getpreferredencoding())"
# 应该显示 UTF-8

# 退出容器
exit
```

### 问题 3: 容器是旧版本

**强制重新构建：**
```bash
sudo docker-compose -f docker-compose-build.yml build --no-cache judger
sudo docker-compose -f docker-compose-build.yml up -d --scale judger=3
```

## 相关文件清单

- `Judger/main.py` - 主要修复文件
- `Judger/Dockerfile` - 已升级到 Swift 5.9
- `Judger/requirements.txt` - 已升级依赖版本
- `fix_chinese_encoding.sh` - 自动化部署脚本
- `work.md` - 完整工作记录

## 技术说明

### 为什么之前能工作？

在某些 Linux 发行版（如 Ubuntu 20.04+）上，系统默认使用 UTF-8 编码，所以即使不指定 `encoding='utf-8'`，也能正确处理中文。但在其他系统或 Docker 容器中，默认编码可能不同。

### 最佳实践

在 Python 3 中读写文本文件时，**始终显式指定编码**：

```python
# 正确的做法
with open('file.txt', 'r', encoding='utf-8') as f:
    content = f.read()

# 不推荐（依赖系统默认编码）
with open('file.txt', 'r') as f:
    content = f.read()
```

### 性能影响

指定 `encoding='utf-8'` 对性能的影响微乎其微，但能避免编码问题，提高代码的可移植性。

## 联系信息

如有问题，请联系：
- 项目地址: https://github.com/Linzecong/LPOJ
- 文档地址: https://docs.lpoj.cn
