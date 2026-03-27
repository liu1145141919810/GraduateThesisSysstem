# DB大作业（课题系统）

## 实现版本 2.1

## 技术栈

架构：Django 5.2.7, 主要语言：Python ,数据库：PostgreSQL ,加密：cryptography 前端：JavaScript等

## 项目结构

```
GraduateThesisSystem/ 毕业论文管理系统
│
├── 📄 配置与初始化文件
│ ├── .env # 环境变量文件（数据库账号、API 密钥等）
│ ├── manage.py # Django 项目管理脚本（用于执行启动、迁移等命令）
│ ├── README.md # 项目说明文档
│ ├── db_evn # 需要自己设置的环境数据
│ └── test.py # 基础功能测试脚本
│
├── 🔧 开发工具配置
│ ├── .idea/ # IntelliJ IDEA 编辑器配置
│ └── .vscode/ # VS Code 编辑器配置
│
├── 📦 mysite/（Django 项目核心配置）
│ ├── init.py
│ ├── asgi.py # 异步服务网关配置（用于异步 Web 服务）
│ ├── wsgi.py # 生产部署网关配置（用于正式环境部署）
│ ├── settings.py # Django 全局配置（数据库、应用、中间件等）
│ ├── urls.py # 项目总路由配置
│ └── pycache/ # Python 编译缓存文件
│
├── 🎨 app00/（系统主应用）、
│ ├── init.py
│ ├── models.py # 数据库模型（论文、学生、指导教师等数据结构）
│ ├── views.py # 视图逻辑（处理请求、渲染页面）
│ ├── admin.py # Django 后台管理界面自定义配置
│ ├── apps.py # 应用配置
│ ├── tests.py # 单元测试文件
│ │
│ ├── migrations/ # 数据库迁移文件（记录数据表结构变更）
│ ├── migrations.bak/ # 迁移文件备份
│ │
│ ├── templates/ # HTML 模板文件（前端页面渲染）
│ │ └── [毕业论文管理系统相关页面]
│ │
│ └── pycache/ # Python 编译缓存文件
│└── 🎯 static/（前端静态资源）
├── css/ # 样式表文件（负责页面样式）
│ └── [页面样式文件]
│├── js/ # JavaScript 文件（负责页面交互与异步请求）
│ └── [交互逻辑文件]
│├── pages/ # 静态 HTML 页面
│ └── [静态页面文件]
│├── images/ # 图片资源（Logo、图标、照片等）
│ └── [PNG、JPG、GIF 等格式文件]
│├── fonts/ # 自定义字体文件
│ └── [TTF、WOFF、OTF 等格式字体]
│└── plugins/ # 第三方依赖库（jQuery、Bootstrap 等）
└── [插件库文件]
```

## 使用方法

Step1： pip install -r requirements.txt 安装依赖

Step2: 配置环境变量，格式如下：

```
# Django
DJANGO_SECRET_KEY=replace-me-with-a-random-secret
DEBUG=True
ALLOWED_HOSTS=127.0.0.1,localhost

# Database (PostgreSQL)
DB_ENGINE=django.db.backends.postgresql
DB_NAME=dbenv
DB_USER=postgres
DB_PASSWORD=replace-me
DB_HOST=localhost
DB_PORT=5432

# Encryption
ENCRYPTION_KEY=replace-me-with-32-bytes-key-or-a-safe-string
```


## 核心功能

## 演示效果

## 更新日志

### 0.0

 搭建起了网站

### 0.1 

数据库使用Django提供的ORM语言，修复部分跳转问题实现了注册和登录

### 0.2 

改进了models数据表，加入了身份识别，密码复杂度检测,和登录日志记录

### 0.3 

加入了登录注册的错误提醒和约束，加密存储密码,python库依赖存储在requirements.txt中

### 0.4 

禁止了非勾选提交，/index/会话管理,/index/展示会话数据测试

### 0.5 

静态文件更新，消息通知栏跳转，简易展示，路径问题调试

### 0.6 

消息界面调试，消息数据库构造，编写消息存入数据库

### 0.7 

消息存在性检测，inbox待发送的展示，发送操作和删除

### 1.0 

加入了个人的消息界面，可以数据库存取，改进重定位问题

### 1.1 

发送邮件进入展示页面参数区域，展示栏名字调整，页面跳转优化

### 1.2 

页面端完全展示实现，删除通知功能，邮件查看方法啊优化

### 1.3 

学生禁止进入选题发布界面等无关部分，内容提交，批改，反馈界面初级处理

### 1.4 

发布选题相关搭建完毕

### 1.5

 选择选题界面，选择入库，选择逻辑，错误提示

### 1.6 

选题报告内容填入，按截至时间在学生端和展示端过滤内容

### 1.7 

教师评语相关的修改，以及录入,学院匹配合适才能进行

### 1.8

 学生和教师查看批改成绩,以及统计工作

### 2.0 

管理员登入检查界面，各个界面的美化

### 2.1 

管理员修改用户信息和登录权限，教师端选题级联删除

## 学习日志

### 1插入内容

table.objects.create(atrribute1=v1,...)

### 2查得到

obj=table.objects.get(attribute1=v1,...)

### 3unique约束

email = models.CharField(max_length=100, unique=True)      # 邮箱唯一

### 4 外键

username=models.ForeignKey(tb_login,on_delete=models.CASCADE)

### 5 加入警告详细
{% if error %}
    <div class="alert alert-danger alert-dismissible fade in" role="alert">
        <button type="button" class="close" data-dismiss="alert" aria-label="Close">
            <span aria-hidden="true">&times;</span>
        </button>
        <strong>错误！</strong> {{ error }}
    </div>
{% endif %}

### 6 密码加密

加密：encrypted_pwd = encrypt_password(pwd) # ← 加密密码
解码：decrypted = cipher.decrypt(encrypted_pwd.encode())

### 7 redirect

避免路径累积
return redirect("/index/")

### 8 会话数据传递

request.session['user_id'] = login_record.id
                request.session['username'] = login_record.username
                request.session['email'] = login_record.email
                request.session['role'] = login_record.role
                tb_login_log.objects.create(username=login_record, status='success')
                return redirect("/index/")

### 9 会话数据在.html使用

{{request.session.username}}

### 10 选项栏内容在

ui-buttons.html

### 11 路径正确生成器

path("index/<str:page>.html", views.index_page, name="index_page"),

### 12 记录，通知页面静态文件

<li><a href="inbox.html">系统通知</a></li>
<li><a href="compose.html">发送通知</a></li>
<li><a href="message-view.html">查看通知</a></li>

### 13 POST方法实现

<form method="POST">
    {% csrf_token %}
    <div class="pull-right">
        <input id="signup-btn" type="submit" value="Sign Up" class="btn btn-primary btn-block">
    </div>
</form>

### 14 request找到目标：

加入 xxname="xxx"的内容,且必须整个加入<form></form>

### 15 用两个同样引用外键时，要指明related_name,防止自动反向生成冲突

 host = models.ForeignKey(tb_login, on_delete=models.CASCADE, related_name='notices_sent')
    recipient = models.ForeignKey(tb_login, on_delete=models.CASCADE, related_name='notices_received')

### 16 数据库迁移撤销

#### 先备份数据库和 migrations 目录
Copy-Item .\db.sqlite3 .\db.sqlite3.bak
Copy-Item .\app00\migrations .\app00\migrations.bak -Recurse

#### 列出迁移文件，确认有哪些（检查是否有 0008 / 0009）
Get-ChildItem .\app00\migrations\ -Name

#### 删除 0009 及以后的迁移（示例删除 0009）
Remove-Item .\app00\migrations\0009_*.py
Remove-Item .\app00\migrations\__pycache__\0009_*.py -ErrorAction SilentlyContinue

#### 重新生成迁移并应用
python manage.py makemigrations app00
python manage.py migrate


### 17 时间属性的加入

timestamp = models.DateTimeField(auto_now_add=True, null=True, blank=True)

### 18 正确跳转新页面

return redirect("/index/inbox.html")

### 19 html在Dijango里可以使用如下的循环

{% for item in items %}
    <p>{{ item }}</p>
{% endfor %}

### 20 测试：重新运行不需要打开新的界面

### 21 实现返回选中ID:

html:
<div class="checkbox">
    <input type="checkbox" class="checkbox-mail" name="selected_ids" value="{{ notice.id }}">
    <label></label>
</div>
会返回一个序列
之后使用 selected_ids = request.POST.getlist('selected_ids')检索即可

### 22 包含多行记录的查询集示例
qs = tb_notice.objects.filter(id__in=ids, host=user)

### 23 删除
qs.delete()

### 24 中notice来自外界所以要指示为{{notice.id}},即勾选之后就返回该notice的id值

### 25 强制覆盖

\$ git push origin main --force

### 26 POST提交

 editButton.addEventListener('click', function() {
            if(editButton.textContent=="确定"){
                fetch("/profile/",{
                    method:"POST",
                    headers:{
                        "Content-Type":"application/json",
                        "X-CSRFToken": "{{ csrf_token }}"
                    },
                    body:JSON.stringify({
                        // 在这里收集需要提交的数据
                        display_name: profileContainer.querySelector('[data-field="display_name"]').textContent,
                    })
                    })
                editButton.textContent = "编辑信息";  // 或 innerText 也行
            }})

### 27 编辑方法，先选再对每个做...
function enterEdit(){//向目标输入
        //console打印当前信息
        console.log("Entering edit mode");
        const profileContainer = document.getElementById('profileForm');
        const infoValues = profileContainer.querySelectorAll('.info-value');
        infoValues.forEach(function(valueDiv) {
            valueDiv.contentEditable = "true";
        });
    }
    </script>

### 28 结构体传输

 //打印payload以调试
        data= json.loads(request.body)
        print("打印体",data)

### 29 优秀的重定位

<a href="/index/"><img src="/static/images/logo-icon.png" alt=""></a>

### 30 后台函数

@receiver(post_save, sender=tb_notice)
def auto_delete_notice(sender, instance, **kwargs):
    # 如果两个显示都关闭，则自动删除这条消息
    if not instance.showsend and not instance.showreceive:
        instance.delete()
触发
m.save()

<<<<<<< HEAD
### 31 crsf提交

headers: {
    'Content-Type': 'application/json',
    'X-CSRFToken': '{{ csrf_token }}'  // ⭐ Django 必须要这个
},

### 32 加入交互数据处理传输

<button class="edit-btn" data-id="{{ msg.id }}">删除</button>

### 33 刷新立即触发

后
return JsonResponse({"status": "ok"})
前
then(...),then(...)

### 34 批量更新方法

qs.update(showsend=False)


### 35 错误提示

1 {% if error %}
    <div class="alert alert-danger alert-dismissible fade in" role="alert">
        <button type="button" class="close" data-dismiss="alert" aria-label="Close">
            <span aria-hidden="true">&times;</span>
        </button>
        <strong>错误！</strong>{{ error }}
    </div>
{% endif %}
2  error=request.session.pop('error',None)
    return render(request, "index.html", {"error": error})
3  if role!=1:
    request.session['error'] = '只有教师才能进行课题分配操作'
    return redirect("/index/")   

### 36 文段输入框

 <textarea class="form-control" id="introduction" name="introduction" rows="8"></textarea>


 ### 37 时间处理

 deadline_str = data['deadline_year'] + data['deadline_day'] + data['deadline_time']
# deadline_str = "2025-12-08T14:00:00"

deadline_dt = datetime.fromisoformat(deadline_str)

### 38 防止过时信息重复

request.session.pop('error', None)


### 39 重要：警告的搭建
1.POST机制将之加入request.session
2.后端触发器写.then(...reload)
3.前端GET，做error=request.session.pop('error', None),然后return render({'error':error})
4.前端写{% if error %}

### 40时间填入标准形式
2025     10-01 00：00

### 41方便的触发操作
<button class="btn btn-xs btn-info" onclick="editUser({{ user.id }})">编辑</button>
