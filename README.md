# Blog-YK

一个基于 Django 的响应式个人博客系统，支持 PC 端和移动端访问。

## 功能特性

### 用户端功能
- 📝 首页文章展示，支持分页
- 📖 文章详情页，包含阅读量统计、上下篇导航
- 🗂️ 分类和标签页面
- 🔍 全文搜索功能
- 🔥 热门文章推荐
- 💬 评论系统（需登录）
- 👤 用户注册、登录、个人资料管理
- 📱 响应式设计，支持移动端

### 管理端功能
- ✏️ 文章管理（新增、编辑、删除、草稿/发布）
- 🗃️ 分类和标签管理
- 💬 评论审核管理
- 👥 用户管理
- ⚙️ 网站设置
- 📊 统计数据展示

## 技术栈

- **后端**: Django 4.2.7
- **前端**: Bootstrap 5 + 自定义 CSS/JS
- **数据库**: MySQL 8.x
- **对象存储**: 七牛云
- **缓存**: Redis (可选)
- **部署**: Nginx + Gunicorn + Supervisor

## 快速开始

### 环境要求

- Python 3.8+
- MySQL 8.0+
- Redis (可选)

### 安装步骤

1. **克隆项目**
   ```bash
   git clone https://github.com/jhzhou002/blog-yk.git
   cd blog-yk
   ```

2. **创建虚拟环境**
   ```bash
   python -m venv venv
   source venv/bin/activate  # Linux/Mac
   # 或
   venv\Scripts\activate     # Windows
   ```

3. **安装依赖**
   ```bash
   pip install -r requirements.txt
   ```

4. **配置环境变量**
   ```bash
   cp .env.example .env
   # 编辑 .env 文件，填写数据库和七牛云配置
   ```

5. **数据库迁移**
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

6. **创建超级用户**
   ```bash
   python manage.py createsuperuser
   ```

7. **收集静态文件**
   ```bash
   python manage.py collectstatic
   ```

8. **运行开发服务器**
   ```bash
   python manage.py runserver
   ```

访问 http://127.0.0.1:8000 查看网站，访问 http://127.0.0.1:8000/admin 进入管理后台。

## 配置说明

### 数据库配置
在 `.env` 文件中设置数据库连接信息：
```
DB_HOST=your_host
DB_NAME=your_database
DB_USER=your_username
DB_PASSWORD=your_password
DB_PORT=3306
```

### 七牛云配置
```
QINIU_ACCESS_KEY=your_access_key
QINIU_SECRET_KEY=your_secret_key
QINIU_BUCKET_NAME=your_bucket_name
QINIU_DOMAIN=your_domain.com
```

### Redis 配置（可选）
```
REDIS_URL=redis://localhost:6379/0
```

## 项目结构

```
blog-yk/
├── blog_yk/              # 项目主配置
├── blog/                 # 博客核心功能
├── accounts/             # 用户管理
├── common/               # 公共模块
├── dashboard/            # 管理面板
├── templates/            # 模板文件
├── static/               # 静态文件
├── requirements.txt      # 依赖包列表
├── manage.py            # Django 管理脚本
└── README.md            # 项目说明
```

## 部署指南

### 使用宝塔面板部署

1. **环境准备**
   - 安装 Python 3.8+
   - 安装 MySQL
   - 安装 Redis (可选)

2. **项目部署**
   - 上传代码到服务器
   - 配置虚拟环境和依赖
   - 设置环境变量
   - 运行数据库迁移

3. **Web 服务配置**
   - 使用 Nginx 作为反向代理
   - 使用 Gunicorn 作为 WSGI 服务器
   - 使用 Supervisor 管理进程

## 开发指南

### 添加新功能

1. 在相应的 app 中创建模型
2. 生成并运行迁移
3. 创建视图和 URL 配置
4. 编写模板
5. 添加测试用例

### 测试

```bash
python manage.py test
```

### 代码风格

项目遵循 PEP 8 代码规范，建议使用以下工具：

- `flake8` 进行代码检查
- `black` 进行代码格式化

## 贡献指南

1. Fork 项目
2. 创建功能分支
3. 提交更改
4. 发起 Pull Request

## 许可证

本项目使用 MIT 许可证，详情请参阅 LICENSE 文件。

## 联系方式

- 作者: jhzhou002
- 邮箱: 318352733@qq.com
- GitHub: https://github.com/jhzhou002/blog-yk

## 更新日志

### v1.0.0 (2024-01-01)
- 初始版本发布
- 完成基本博客功能
- 集成七牛云存储
- 添加响应式设计