from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.core.validators import EmailValidator
from django.core.exceptions import ValidationError
from django.template.loader import get_template
from django.http import Http404
from app00.models import *
import re
import os
from cryptography.fernet import Fernet
import base64
import hashlib
from dotenv import load_dotenv

load_dotenv()
# 生成加密密钥
SECRET_KEY = os.getenv('ENCRYPTION_KEY', 'your-secret-key-32-characters-long!')
cipher = Fernet(base64.urlsafe_b64encode(hashlib.sha256(SECRET_KEY.encode()).digest()))
def encrypt_password(pwd):
    """加密密码"""
    encrypted = cipher.encrypt(pwd.encode())
    return encrypted.decode()

def decrypt_password(encrypted_pwd):
    """解密密码"""
    try:
        decrypted = cipher.decrypt(encrypted_pwd.encode())
        return decrypted.decode()
    except Exception:
        return None
# Create your views here.
def is_strong_password(pwd):#验证密码强度
    """
    密码要求：
    - 长度至少 8 个字符
    - 包含至少一个大写字母
    - 包含至少一个小写字母
    - 包含至少一个数字
    - 包含至少一个特殊字符（可选）
    返回值：(True/False, 错误信息)
    """
    if len(pwd) < 8:
        return False, '密码长度至少 8 个字符'
    
    if not re.search(r'[a-z]', pwd):
        return False, '密码必须包含小写字母'
    
    if not re.search(r'[A-Z]', pwd):
        return False, '密码必须包含大写字母'
    
    if not re.search(r'[0-9]', pwd):
        return False, '密码必须包含数字'
    
    return True, '密码强度符合要求'
def is_valid_email(email):#验证邮箱格式
    validator = EmailValidator()
    try:
        validator(email)
        return True
    except ValidationError:
        return False
def roleteller(email,usr,pwd):#判断注册合法性
    try:
        login_info=tb_login.objects.get(email=email)
        return -3#错误种类3：邮箱已经被使用
    except Exception:
        pass
    if not is_valid_email(email):
        return -1#错误种类1：邮箱格式错误
    # 根据邮箱后缀区分角色
    if email.endswith('@teacher.com'):
        return 1  # 教师
    elif email.endswith('@student.com'):
        return 2  # 学生
    elif email.endswith('@admin.com'):
        return 0  # 管理员
    else:
        return -2  # 错误种类2：邮箱后缀不符合规则
def login(request):
    """用户登录"""
    if request.method == "GET":
        return render(request, "login.html")
    elif request.method == "POST":
        user = request.POST.get("user")
        pwd = request.POST.get("pwd")
        if user=="Admin" and pwd =="123456":#管理员特殊登录
            return redirect("/index/")
        try:
            login_record = tb_login.objects.get(username=user)
            # ✓ Bug 修复：解密后比对密码
            stored_pwd = decrypt_password(login_record.pwd)
            if stored_pwd == pwd:
                request.session['user_id'] = login_record.id
                request.session['username'] = login_record.username
                request.session['email'] = login_record.email
                request.session['role'] = login_record.role
                tb_login_log.objects.create(username=login_record, status='success')
                return redirect("/index/")
            else:
                tb_login_log.objects.create(username=login_record, status='fail')
                return render(request, "login.html", {'error': '登录失败：密码错误'})
        except tb_login.DoesNotExist:
            return render(request, "login.html", {'error': '登录失败：用户不存在'})

    return redirect("index/")
def register(request):#用户注册
    if request.method=="GET":
        return render(request,"registration.html")
    elif request.method=="POST":
        mail=request.POST.get("email")
        user=request.POST.get("usr")
        pwd=request.POST.get("pwd")
        is_strong, message = is_strong_password(pwd)
         # 后端强制校验：必须同意条款
        if not is_strong:
            return render(request, "registration.html", {
                    'error': f'注册失败: {message}'
               })
        role=roleteller(mail,user,pwd)
        if role==-1:
            return render(request, "registration.html", {
                    'error': f'注册失败: {"邮箱格式错误"}'
               })
        if role==-2:
            return render(request, "registration.html", {
                    'error': f'注册失败: {"请使用学校提供邮箱"}'
               })
        if role==-3:
            return render(request, "registration.html", {
                    'error': f'注册失败: {"此邮箱已经被使用过"}'
               })
        if role==0:
            return render(request, "registration.html", {
                    'error': f'注册失败: {"联系管理员申请管理权限"}'
               })
        if role==1:
            try:
                pwd=encrypt_password(pwd)  # 加密密码后存储
                tb_login.objects.create(email=mail,username=user,pwd=pwd,role=role)
                tb_teacher.objects.create(email=mail,username=user)
                return redirect("/login/")
            except Exception:
                return render(request, "registration.html", {
                    'error': f'注册失败: {"非法注册"}'
               })
        if role==2:
            try:
                pwd=encrypt_password(pwd)  # 加密密码后存储
                tb_login.objects.create(email=mail,username=user,pwd=pwd,role=role)
                tb_student.objects.create(email=mail,username=user)
                return redirect("/login/")
            except Exception:
                return render(request, "registration.html", {
                    'error': f'注册失败: {"非法注册"}'
                })
def index_page(request, page):
    if 'username' not in request.session:
        return redirect("/login/")
    # 假设模板放在 templates/ 下且文件名是 ui-buttons.html、ui-panels.html 等
    template_name = f"{page}.html"

    # 可选：先检查模板是否存在，避免没有模板时报 500
    try:
        get_template(template_name)
    except Exception:
        raise Http404("Page not found")
    
    if page == "compose":#通知发送页面特殊处理
        print("方法：", request.method)
        print("Compose 页面特殊处理")
        if request.method == "GET":
            return render(request, template_name)
        elif request.method == "POST":
            To = request.POST.get("to")
            subject = request.POST.get("subject")
            message = request.POST.get("message")
            try:
                sender_id = request.session.get('user_id')
                sender = tb_login.objects.get(id=sender_id)
                recipient = tb_login.objects.get(username=To)
                tb_notice.objects.create(
                    host=sender,
                    recipient=recipient,
                    subject=subject,
                    message=message,
                    send=True
                )
                print("通知发送成功")
                return render(request, "inbox.html", {'success': '编写成功'})
            except tb_login.DoesNotExist:
                return render(request, "compose.html", {'error': '编写失败：收件人不存在'})
            return render(request,"inbox.html")
        
    if page == "inbox":
        print("方法：", request.method)
        print("Inbox 页面特殊处理")
    return render(request, template_name)
def index(request):
    if 'username' not in request.session:
        return redirect("/login/")
    print("Session 数据：", request.session.items())
    if request.method == "POST":
       pass
    return render(request, "index.html")