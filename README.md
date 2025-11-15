# DB大作业（课题系统）

## 实现版本 0.4

## 更新操作

### 0.0 搭建起了网站

### 0.1 数据库使用Django提供的ORM语言，修复部分跳转问题实现了注册和登录

### 0.2 改进了models数据表，加入了身份识别，密码复杂度检测,和登录日志记录

### 0.3 加入了登录注册的错误提醒和约束，加密存储密码,python库依赖存储在requirements.txt中

### 0.4 禁止了非勾选提交，/index/会话管理,/index/展示会话数据测试

### 0.5 静态文件更新，消息通知栏跳转，简易展示，路径问题调试

### 0.6 消息界面调试，消息数据库构造，编写消息存入数据库

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