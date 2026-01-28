# LPOJ 项目工作记录

## 2025-12-27 工作内容

### 1. 修复中文测试数据评测错误问题

**问题描述：**
当测试数据中包含中文字符时，评测程序会出错。

**问题原因：**
在 `Judger/main.py` 中，读取测试数据文件和输出文件时没有指定 `encoding='utf-8'`，导致 Python 使用系统默认编码（通常是 ASCII），遇到中文时抛出 `UnicodeDecodeError` 异常。

**修复位置：**
1. **Line 895-916**：读取测试数据用于展示
   - `inputfile = open(..., "r")` → `open(..., "r", encoding='utf-8')`
   - `outputfile = open(..., "r")` → `open(..., "r", encoding='utf-8')`
   - `useroutputfile = open(..., "r")` → `open(..., "r", encoding='utf-8')`

2. **Line 995-997**：比较输出文件
   - `file1 = open(..., "r")` → `open(..., "r", encoding='utf-8')`
   - `file2 = open(..., "r")` → `open(..., "r", encoding='utf-8')`

**文件修改：**
- `/home/zq/project/LPOJ/Judger/main.py`

---

### 2. 升级所有 Docker 基础镜像和依赖版本

**升级动机：**
原有基础镜像版本过旧，存在大量兼容性问题和安全漏洞。

#### 2.1 Database (MySQL)

**文件：** `Database/Dockerfile`

**变更：**
```diff
- FROM mysql:5.7
+ FROM mysql:8.0
- MAINTAINER linzecong
+ LABEL maintainer="linzecong"
```

**原因：** MySQL 5.7 已 EOL，8.0 是当前 LTS 版本

---

#### 2.2 Backend (Django REST API)

**文件：**
- `Backend/Dockerfile`
- `Backend/requirements.txt`

**Dockerfile 变更：**
```diff
- FROM python:3.7.2
+ FROM python:3.11-slim
- RUN apt-get update && apt-get install python-django -y
- RUN pip install -r requirements.txt
+ RUN apt-get update && \
+     apt-get install -y --no-install-recommends \
+     default-libmysqlclient-dev \
+     build-essential \
+     pkg-config && \
+     rm -rf /var/lib/apt/lists/*
+ RUN pip install --no-cache-dir -r requirements.txt
```

**requirements.txt 变更：**
```diff
- Django==2.2.8
- djangorestframework==3.9.3
- django-filter==2.1.0
- django-cors-headers==2.5.3
- mysqlclient==1.4.2.post1
- django-sslserver
- gevent
- gunicorn==19.9.0
+ Django==4.2.11
+ djangorestframework==3.14.0
+ django-filter==23.5
+ django-cors-headers==4.3.1
+ mysqlclient==2.2.4
+ django-sslserver==0.22
+ gevent==24.2.1
+ gunicorn==21.2.0
```

**改进：**
- 使用 slim 镜像减小体积
- Django 升级到 4.2 LTS
- 合并 RUN 命令减少镜像层数
- 清理 apt 缓存

---

#### 2.3 JudgerServer (判题协调服务器)

**文件：**
- `JudgerServer/Dockerfile`
- `JudgerServer/requirements.txt`

**Dockerfile 变更：**
```diff
- FROM python:3.7.2
+ FROM python:3.11-slim
+ RUN apt-get update && \
+     apt-get install -y --no-install-recommends \
+     default-libmysqlclient-dev \
+     build-essential \
+     pkg-config && \
+     rm -rf /var/lib/apt/lists/*
- RUN pip install -r requirements.txt
+ RUN pip install --no-cache-dir -r requirements.txt
```

**requirements.txt 变更：**
```diff
- mysqlclient==1.4.2.post1
+ mysqlclient==2.2.4
```

---

#### 2.4 CrawlingServer (爬虫服务器)

**文件：**
- `CrawlingServer/Dockerfile`
- `CrawlingServer/requirements.txt`

**Dockerfile 变更：**
```diff
- FROM python:3.7.2
+ FROM python:3.11-slim
+ RUN apt-get update && \
+     apt-get install -y --no-install-recommends \
+     default-libmysqlclient-dev \
+     build-essential \
+     pkg-config && \
+     rm -rf /var/lib/apt/lists/*
- RUN pip install -r requirements.txt
+ RUN pip install --no-cache-dir -r requirements.txt
```

**requirements.txt 变更：**
```diff
- feedparser==5.2.1
- mysqlclient==1.4.2.post1
+ feedparser==6.0.11
+ mysqlclient==2.2.4
```

---

#### 2.5 Frontend (桌面前端)

**文件：** `Frontend/Dockerfile`

**变更：**
```diff
- FROM node:13.10-slim
+ FROM node:18-slim
- RUN apt-get update
- RUN npm install
- RUN npm run build
- RUN apt-get install nginx -y
- RUN rm -rf /Frontend/node_modules
+ RUN apt-get update && \
+     apt-get install -y --no-install-recommends nginx && \
+     rm -rf /var/lib/apt/lists/*
+ RUN npm install --legacy-peer-deps && \
+     npm run build && \
+     rm -rf /Frontend/node_modules
```

**改进：**
- Node.js 13 → 18 LTS
- 添加 `--legacy-peer-deps` 解决依赖冲突
- 合并命令减少镜像层数

---

#### 2.6 FrontendMobile (移动前端)

**文件：** `FrontendMobile/Dockerfile`

**变更：**
```diff
- FROM node:13.10-slim
+ FROM node:18-slim
- RUN apt-get update
- RUN npm install
- RUN npm run build
- RUN apt-get install nginx -y
- RUN rm -rf /Frontend/node_modules
+ RUN apt-get update && \
+     apt-get install -y --no-install-recommends nginx && \
+     rm -rf /var/lib/apt/lists/*
+ RUN npm install --legacy-peer-deps && \
+     npm run build && \
+     rm -rf /FrontendMobile/node_modules
```

**修复：** 原 Dockerfile 中 `rm -rf /Frontend/node_modules` 路径错误，已修正为 `/FrontendMobile/node_modules`

---

#### 2.7 Judger (判题执行引擎)

**文件：**
- `Judger/Dockerfile`
- `Judger/requirements.txt`

**Dockerfile 变更：**
```diff
- FROM swift:5.1
+ FROM swift:5.9-jammy
- RUN apt-get update
- RUN mv /usr/lib/python2.7/site-packages /usr/lib/python2.7/dist-packages
- RUN ln -s dist-packages /usr/lib/python2.7/site-packages
- RUN apt-get install python2.7 -y
- RUN apt-get install python3 -y
- ... (多个独立的 RUN 命令)
+ RUN apt-get update && \
+     apt-get install -y --no-install-recommends \
+     python2.7 \
+     python3 \
+     python3-pip \
+     default-mysql-client \
+     default-libmysqlclient-dev \
+     libatomic1 \
+     libssl-dev \
+     zlib1g-dev \
+     pkg-config \
+     net-tools \
+     nano \
+     iputils-ping \
+     time \
+     cmake \
+     openjdk-11-jdk \
+     libseccomp-dev \
+     build-essential && \
+     rm -rf /var/lib/apt/lists/*
+ RUN if [ -d /usr/lib/python2.7/site-packages ]; then \
+         mv /usr/lib/python2.7/site-packages /usr/lib/python2.7/dist-packages && \
+         ln -s dist-packages /usr/lib/python2.7/site-packages; \
+     fi
- RUN pip3 install -r requirements.txt
+ RUN pip3 install --no-cache-dir -r requirements.txt
- RUN apt-get install libseccomp-dev -y && mkdir build && cd build && cmake /Judger && make && make install && cd .. && cd JudgerCore && python3 setup.py install
+ RUN mkdir -p build && \
+     cd build && \
+     cmake /Judger && \
+     make && \
+     make install && \
+     cd /Judger/JudgerCore && \
+     python3 setup.py install
```

**requirements.txt 变更：**
```diff
- paramiko==2.4.2
- mysqlclient==1.4.2.post1
- requests==2.20.0
+ paramiko==3.4.0
+ mysqlclient==2.2.4
+ requests==2.31.0
```

**改进：**
- Swift 5.1 → 5.9（基于 Ubuntu 22.04 Jammy）
- OpenJDK 8 → 11
- 大幅优化 Dockerfile 结构
- 添加条件判断处理 Python 2.7 兼容性

---

### 3. Docker 镜像优化总结

#### 3.1 镜像体积优化
- 使用 `slim` 变体基础镜像
- 添加 `--no-install-recommends` 只安装必要依赖
- 使用 `rm -rf /var/lib/apt/lists/*` 清理 apt 缓存
- pip 安装使用 `--no-cache-dir` 不缓存包

#### 3.2 构建性能优化
- 合并多个 `RUN` 命令减少镜像层数
- 按依赖变化频率排序命令，利用 Docker 层缓存

#### 3.3 安全性改进
- 升级到有安全支持的版本
- Python 3.7 (EOL) → 3.11
- Node.js 13 (EOL) → 18 LTS
- MySQL 5.7 (EOL) → 8.0

---

## 版本对比表

| 组件 | 旧版本 | 新版本 | 备注 |
|------|--------|--------|------|
| **基础镜像** |
| Database | mysql:5.7 | mysql:8.0 | LTS 版本 |
| Backend | python:3.7.2 | python:3.11-slim | 更快、更小 |
| JudgerServer | python:3.7.2 | python:3.11-slim | 同上 |
| CrawlingServer | python:3.7.2 | python:3.11-slim | 同上 |
| Frontend | node:13.10-slim | node:18-slim | LTS 版本 |
| FrontendMobile | node:13.10-slim | node:18-slim | LTS 版本 |
| Judger | swift:5.1 | swift:5.9-jammy | Ubuntu 22.04 基础 |
| **Python 依赖** |
| Django | 2.2.8 | 4.2.11 | LTS 版本 |
| djangorestframework | 3.9.3 | 3.14.0 | 稳定版 |
| django-filter | 2.1.0 | 23.5 | 最新稳定版 |
| django-cors-headers | 2.5.3 | 4.3.1 | 最新稳定版 |
| mysqlclient | 1.4.2.post1 | 2.2.4 | 支持 MySQL 8.0 |
| gunicorn | 19.9.0 | 21.2.0 | 性能提升 |
| gevent | (未指定) | 24.2.1 | 最新稳定版 |
| requests | 2.20.0 | 2.31.0 | 安全更新 |
| paramiko | 2.4.2 | 3.4.0 | 安全更新 |
| feedparser | 5.2.1 | 6.0.11 | 最新稳定版 |
| **JDK** |
| OpenJDK | 8 | 11 | LTS 版本 |

---

## 部署和测试

### 部署命令

```bash
cd /home/zq/project/LPOJ

# 1. 停止现有服务
sudo docker-compose stop

# 2. 使用升级后的配置重新构建并启动（3个judger实例）
sudo docker-compose -f docker-compose-build.yml up -d --build --scale judger=3

# 3. 查看容器状态
sudo docker-compose ps

# 4. 查看日志
sudo docker-compose logs -f
```

### 测试清单

- [ ] 用户注册和登录
- [ ] 题目浏览和搜索
- [ ] 代码提交（C/C++/Java/Python/Swift）
- [ ] **中文测试数据评测**
- [ ] Special Judge 功能
- [ ] 选择题评测
- [ ] 比赛功能
- [ ] 班级和作业功能
- [ ] 讨论板
- [ ] 博客系统
- [ ] Wiki 知识库
- [ ] 移动端界面

---

## 注意事项

### MySQL 8.0 兼容性
- 默认身份验证插件变更：`mysql_native_password` → `caching_sha2_password`
- docker-compose.yml 中已配置 `--default-authentication-plugin=mysql_native_password` 保持兼容

### Django 4.2 迁移
- 部分 API 有破坏性变更，需要测试
- 已知问题：某些第三方包可能不兼容，需要更新或替换

### 首次构建
- 需要下载新的基础镜像，时间较长
- 建议配置 Docker 镜像加速器

---

## 相关文件

- `CLAUDE.md` - 项目架构和开发指南
- `docker-compose.yml` - 生产环境配置（使用远程镜像）
- `docker-compose-build.yml` - 开发环境配置（本地构建）
- `Judger/main.py` - 判题核心逻辑（已修复中文支持）

---

## 未来改进建议

1. **添加测试用例**：目前项目没有自动化测试
2. **CI/CD 集成**：添加 GitHub Actions 自动构建和测试
3. **监控和日志**：集成 Prometheus + Grafana
4. **性能优化**：数据库查询优化，添加 Redis 缓存
5. **安全加固**：定期更新依赖，添加 WAF
6. **文档完善**：API 文档、部署文档、开发者文档
