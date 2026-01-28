# LPOJ 开发环境 - 快速参考

## 🚀 快速启动 (一键启动所有服务)

```bash
cd /home/zq/project/LPOJ
bash dev-start.sh
```

这会自动:
1. ✅ 启动MySQL数据库容器
2. ✅ 创建数据库和初始数据
3. ✅ 启动Backend服务
4. ✅ 启动Frontend桌面版
5. ✅ 启动FrontendMobile移动版

## 🌐 访问地址

| 服务 | 地址 | 说明 |
|------|------|------|
| 前端(桌面) | http://localhost:8080 | Vue.js应用 |
| 前端(移动) | http://localhost:8081 | 移动响应版本 |
| 后端API | http://localhost:9003 | Django REST API |
| 管理后台 | http://localhost:9003/admin | 账户: admin / 密码: admin |
| 数据库 | 127.0.0.1:3306 | MySQL (根密码: lpojdatabase) |

## 🛑 停止所有服务

```bash
bash dev-stop.sh
```

## 📊 查看服务状态

```bash
bash dev-status.sh
```

## 💻 单独启动服务

### 只启动数据库
```bash
docker-compose -f docker-compose-dev.yml up -d
```

### 只启动Backend
```bash
cd Backend
python manage.py runserver 0.0.0.0:9003
```

### 只启动Frontend
```bash
cd Frontend
npm run dev
```

### 只启动Mobile Frontend
```bash
cd FrontendMobile
npm run dev
```

## 🔄 开发工作流

### 修改Backend代码
- Django runserver会自动检测文件变化并重启
- 修改后刷新浏览器即可看到更改

### 修改Frontend代码
- `npm run dev` 支持HMR (Hot Module Replacement)
- 修改代码会自动重新编译
- 浏览器会自动刷新或模块热更新

### 修改数据库Schema
```bash
cd Backend
python manage.py makemigrations
python manage.py migrate
```

## 📦 数据库操作

### 查看数据库
```bash
mysql -h 127.0.0.1 -u root -p
# 输入密码: lpojdatabase
```

### 重置数据库
```bash
cd Backend
python manage.py flush --no-input
python manage.py migrate
```

### 导入初始数据
```bash
cd Backend
python manage.py loaddata initial_data.json  # 如果有的话
```

## 📝 日志查看

### 查看Docker日志
```bash
docker-compose -f docker-compose-dev.yml logs -f db
```

### 查看Backend日志
在Backend运行的终端中可以直接看到输出

### 查看Frontend日志
在Frontend运行的终端中可以直接看到输出

## ⚙️ 环境配置

### Python依赖安装
```bash
cd Backend
pip install -r requirements.txt
```

### Node依赖安装
```bash
cd Frontend
npm install --legacy-peer-deps

cd ../FrontendMobile
npm install --legacy-peer-deps
```

## 🔍 常见问题

### Q: 无法连接数据库?
```bash
# 检查MySQL容器是否运行
docker ps | grep mysql

# 检查容器IP和端口
docker inspect $(docker-compose -f docker-compose-dev.yml ps -q db)

# 尝试重启数据库
docker-compose -f docker-compose-dev.yml restart db
```

### Q: 前端无法连接后端?
- 检查后端是否运行: `bash dev-status.sh`
- 检查Backend地址配置
- 检查CORS设置

### Q: npm install失败?
```bash
# 清除缓存重试
npm cache clean --force
rm -rf node_modules package-lock.json
npm install --legacy-peer-deps
```

### Q: 管理员账户信息?
- 账户: admin
- 密码: admin
- 邮箱: admin@example.com

### Q: 如何修改数据库密码?
编辑 `docker-compose-dev.yml`:
```yaml
MYSQL_ROOT_PASSWORD: "新密码"
```
然后重启数据库

## 📚 文件结构

```
/home/zq/project/LPOJ/
├── docker-compose-dev.yml   # 开发用Docker配置
├── dev-start.sh             # 一键启动脚本
├── dev-stop.sh              # 停止脚本
├── dev-status.sh            # 状态检查脚本
├── Backend/                 # Django后端
├── Frontend/                # Vue.js前端
├── FrontendMobile/          # 移动前端
├── Judger/                  # 判题引擎
└── ...
```

## 💡 开发技巧

### 快速导入大量数据
```bash
cd Backend
python manage.py shell
>>> # 在Python REPL中执行Django ORM操作
```

### 调试API
```bash
# 使用curl测试
curl -X GET http://localhost:9003/api/problems/

# 使用postman或similar工具
# GUI界面更方便
```

### 监视文件变化
```bash
# Linux/Mac
watch 'bash dev-status.sh'

# 或使用Python
python -m http.server 8000  # 查看输出
```

### 清理日志
```bash
# 清理Docker日志
docker-compose -f docker-compose-dev.yml logs --tail=0 -f

# 清理npm cache
npm cache clean --force
```

## 🎯 生产构建测试

### 测试生产版Frontend
```bash
cd Frontend
npm run build
# 输出到 dist/ 目录

# 用Python启动本地服务器
python -m http.server 8000
```

### 生产模式运行Backend
```bash
cd Backend
gunicorn -w 5 --bind 0.0.0.0:9003 -k 'gevent' Backend.wsgi:application
```

---

**祝开发愉快! 🎉**
