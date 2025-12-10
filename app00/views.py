from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.core.validators import EmailValidator
from django.core.exceptions import ValidationError
from django.template.loader import get_template
from django.http import Http404
from django.db import transaction
from app00.admin import *
from app00.models import *
import re
import os
from cryptography.fernet import Fernet
import base64
import hashlib
from dotenv import load_dotenv
import json
from django.http import JsonResponse

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
    print("请求方法：", request.method)
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
                print("登录成功，Session 数据：", request.session.items())
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
                tb_teacher.objects.create(email=mail,username=user,login_id=tb_login.objects.get(username=user))
                return redirect("/login/")
            except Exception:
                return render(request, "registration.html", {
                    'error': f'注册失败: {"非法注册"}'
               })
        if role==2:
            try:
                pwd=encrypt_password(pwd)  # 加密密码后存储
                tb_login.objects.create(email=mail,username=user,pwd=pwd,role=role)
                tb_student.objects.create(email=mail,username=user,login_id=tb_login.objects.get(username=user))
                return redirect("/login/")
            except Exception:
                return render(request, "registration.html", {
                    'error': f'注册失败: {"非法注册"}'
                })
def index_page(request, page):
    print("请求页面：", page)
    if 'username' not in request.session:
        return redirect("/login/")
    # 假设模板放在 templates/ 下且文件名是 ui-buttons.html、ui-panels.html 等
    template_name = f"{page}.html"
    login_user = tb_login.objects.get(id=request.session.get('user_id'))
    role=login_user.role
    username=""
    if role==1:
        username=tb_teacher.objects.get(email=login_user.email).username
    elif role==2:
        username=tb_student.objects.get(email=login_user.email).username
    
    if tellit(template_name):
        return issue_deal(request,page,role)
    
     # 先获取当前用户

    user_id = request.session.get('user_id')
    sent_notices = []
    user = None

    # 可选：先检查模板是否存在，避免没有模板时报 500
    try:
        get_template(template_name)
    except Exception:
        raise Http404("Page not found")
    if page == "profile":
        return redirect("/profile/")
    
    if page == "message-view":
        if request.method == "POST":
            data= json.loads(request.body)
            id= data.get("id")
            notice=tb_notice.objects.get(id=id)
            notice.showreceive=False
            notice.save()
            print("删除消息ID：",id)
            return JsonResponse({"status": "ok"})
            
        user_id = request.session.get('user_id')
        message=tb_notice.objects.filter(recipient_id=user_id,send=True).order_by('-timestamp')#获取已发送的通知
        with transaction.atomic():
            for m in message:
                m.read = True
                m.save()
        message=deal_message(message)
        return render(request,template_name,{'username':username,'message':message})
        #return render(request, template_name, {'sent_notices': sent_notices, 'success': success})#发送的消息一并送出

    if page == "compose":#通知发送页面特殊处理
        print("方法：", request.method)
        print("Compose 页面特殊处理")

        if request.method == "GET":
            return render(request, template_name,{'username':username})
        elif request.method == "POST":
            To = request.POST.get("to")
            subject = request.POST.get("subject")
            message = request.POST.get("message")
            try:
                sender_id = request.session.get('user_id')
                sender = tb_login.objects.get(id=sender_id)
                recipient = tb_login.objects.get(username=To)
                if sender == recipient:
                    return render(request, "compose.html", {'error': '编写失败：不能给自己发送通知'})
                 # 创建并保存通知记录
                tb_notice.objects.create(
                    host=sender,
                    recipient=recipient,
                    subject=subject,
                    message=message,
                    send=False
                )
                print("通知发送成功")
                # 在 session 中标记成功消息，重定向到 inbox 页面对应的 URL
                request.session['success'] = '编写成功'
                return redirect("/index/inbox.html")
            except tb_login.DoesNotExist:
                if role==1:
                    username=tb_teacher.objects.get(email=sender.email).username
                elif role==2:
                    username=tb_student.objects.get(email=sender.email).username
                return render(request, "compose.html",{'username':username,'error': '编写失败：收件人不存在'})

    if page == "inbox":#提取该用户发送的数据库通知
        # 先获取当前用户
        user_id = request.session.get('user_id')
        sent_notices = []
        user = None
        try:
            if user_id:
                user = tb_login.objects.get(id=user_id)
        except Exception:
            user = None
        # 处理 POST 操作（批量操作：标为已读/未读、删除）
        if request.method == "POST":
            action = request.POST.get('action')
            selected_ids = request.POST.getlist('selected_ids')
            print("Inbox POST 操作", action, "选中：", selected_ids)
            send=request.POST.get('send')
            edit=request.POST.get('edit')
            view=request.POST.get('view')
            delete=request.POST.get('delete')
            print("按钮状态：",send,edit,view,delete)
            if user and selected_ids:
                try:
                    # 将 id 字符串转为整数列表
                    ids = [int(x) for x in selected_ids if x.isdigit()]
                    qs = tb_notice.objects.filter(id__in=ids, host=user)
                    if send != None:
                        qs.update(send=True)
                        print("发送成功")
                        request.session['success'] = '所选通知已发送'
                    elif edit !=None:
                        pass
                        #request.session['success'] = '所选通知已标为未读'
                    elif view !=None:
                        pass
                        #deleted_count = qs.count()
                        #qs.delete()
                        #request.session['success'] = f'已删除 {deleted_count} 条通知'
                    elif delete !=None:
                        qs.update(showsend=False)
                        print("删除成功")
                        request.session['success'] = f'已删除所选通知'
                except Exception as e:
                    request.session['success'] = '操作失败'
                    print('Inbox 批量操作异常：', e)
            else:
                request.session['success'] = '未选择任何通知或未登录'
            # 使用 PRG 模式：重定向到 inbox 页面以避免重复提交
            return redirect('/index/inbox.html')

        # GET：获取并展示当前用户的已发送通知
        try:
            if user:
                sent_notices = tb_notice.objects.filter(host=user, showsend=True).order_by('-timestamp')#按时间排序的发送消息
        except Exception:
            sent_notices = []
        # 读取并移除可能存在的成功消息
        success = request.session.pop('success', None)
        return render(request, template_name, {'username':username, 'sent_notices': sent_notices, 'success': success})#发送的消息一并送出
    return render(request, template_name,{'username':username})
def index(request):
    if 'username' not in request.session:
        return redirect("/login/")
    print("Session 数据：", request.session.items())
    if request.method == "POST":
       pass
    error=request.session.pop('error',None)
    print("Error message on index page:",error)
    return render(request, "index.html", {"error": error})
#========================
def profile(request):
    """个人信息页面（优化：实时查询数据库最新数据）"""
    #print("访问个人信息页面")
    #print("Session 数据：", request.session.items())
    if 'user_id' not in request.session:  # 仅判断 user_id 是否存在
        return redirect("/login/")
    if request.method == "POST":
        # 打印payload以调试
        data= json.loads(request.body)
        user_id = request.session.get('user_id')
        login_user = tb_login.objects.get(id=user_id)  # 实时查询，确保数据最新
        if login_user.role==1:
            try:
               tb_teacher.objects.filter(email=login_user.email).update(
                    display_name=data.get("display_name", "未设置"),
                    gender=data.get("gender", "unknown"),
                    phone=data.get("phone", "000000"),
                    college=data.get("college", "unknown"),
                    student_id=data.get("student_id", "000000"),
                    major=data.get("major", "unknown"),
                )
            except Exception as e:
                print(f"更新教师信息错误: {e}")
        elif login_user.role==2:
            try:
                tb_student.objects.filter(email=login_user.email).update(
                    display_name=data.get("display_name", "未设置"),
                    gender=data.get("gender", "unknown"),
                    phone=data.get("phone", "000000"),
                    college=data.get("college", "unknown"),
                    student_id=data.get("student_id", "000000"),
                    major=data.get("major", "unknown"),        
                )
            except Exception as e:
                print(f"更新学生信息错误: {e}")
    try:
        user_id = request.session.get('user_id')
        login_user = tb_login.objects.get(id=user_id)  # 实时查询，确保数据最新
        
        # 2. 基础用户信息（从实时查询的 login_user 中获取）
        user_info = {
            'username': login_user.username,  # 实时用户名
            'email': login_user.email,        # 实时邮箱
            'role': login_user.role,          # 实时角色
        }
        
        # 3. 根据角色实时查询教师/学生表的最新数据
        if login_user.role == 1:  # 教师
            try:
                teacher_info = tb_teacher.objects.get(email=login_user.email)  # 实时查询
                display_name = teacher_info.display_name if teacher_info.display_name and teacher_info.display_name != '未设置' else teacher_info.username
                user_info.update({
                    'display_name': display_name,
                    'login_username': teacher_info.username,
                    'gender': teacher_info.gender if teacher_info.gender and teacher_info.gender != '未设置' else '未设置',
                    'phone': teacher_info.phone if teacher_info.phone and teacher_info.phone != '未设置' else '未设置',
                    'college': teacher_info.college if teacher_info.college and teacher_info.college != '未设置' else '未设置',
                    'student_id': teacher_info.student_id if teacher_info.student_id else f"T{teacher_info.id}".zfill(10),
                    'major': teacher_info.major if teacher_info.major and teacher_info.major != '未设置' else '未设置',
                    'role_display': '教师'
                })
            except tb_teacher.DoesNotExist:
                # 若教师表无数据，用登录表数据填充默认值
                user_info.update({
                    'display_name': login_user.username,
                    'login_username': login_user.username,
                    'gender': '未设置',
                    'phone': '未设置',
                    'college': '未设置',
                    'student_id': f"T{user_id}".zfill(10) if user_id else '未知',
                    'major': '未设置',
                    'role_display': '教师'
                })
        
        elif login_user.role == 2:  # 学生（
            try:
                student_info = tb_student.objects.get(email=login_user.email)  # 实时查询
                display_name = student_info.display_name if student_info.display_name and student_info.display_name != '未设置' else student_info.username
                user_info.update({
                    'display_name': display_name,
                    'login_username': student_info.username,
                    'gender': student_info.gender if student_info.gender and student_info.gender != '未设置' else '未设置',
                    'phone': student_info.phone if student_info.phone and student_info.phone != '未设置' else '未设置',
                    'college': student_info.college if student_info.college and student_info.college != '未设置' else '未设置',
                    'student_id': student_info.student_id if student_info.student_id else f"S{student_info.id}".zfill(10),
                    'major': student_info.major if student_info.major and student_info.major != '未设置' else '未设置',
                    'role_display': '学生'
                })
            except tb_student.DoesNotExist:
                user_info.update({
                    'display_name': login_user.username,
                    'login_username': login_user.username,
                    'gender': '未设置',
                    'phone': '未设置',
                    'college': '未设置',
                    'student_id': f"S{user_id}".zfill(10) if user_id else '未知',
                    'major': '未设置',
                    'role_display': '学生'
                })
    
        else:  # 管理员
            user_info.update({
                'display_name': login_user.username,
                'login_username': login_user.username,
                'gender': '未设置',
                'phone': '未设置',
                'college': '未设置',
                'student_id': f"A{user_id}".zfill(10) if user_id else '未知',
                'major': '未设置',
                'role_display': '管理员' if login_user.role == 0 else '用户'
            })
        #print("\n===== 个人信息页面调试 =====")
        #print(f"当前登录用户 ID: {user_id}")
        #print(f"登录表（tb_login）中的 email: {login_user.email}")
        #print(f"传递给模板的 user_info 数据：")
        #for key, value in user_info.items():
            #print(f"  {key}: {value}")
        #print("===========================\n")

        return render(request, "profile.html", {'user_info': user_info})
    
    except Exception as e:
        print(f"个人信息页面错误: {e}")
        return redirect("/login/")
    
def issue_deal(request,page,role=None):
    print("role :",role)
    template=f"{page}.html"
     # 可选：先检查模板是否存在，避免没有模板时报 500
    if template=="myissue.html":
        if role!=2:
           request.session['error'] = '只有学生才能查看作业'
           return redirect("/index/")
        return myissue(request)
    elif template=="distribute.html":
        if role!=1:
           request.session['error'] = '只有教师才能进行课题分配操作'
           return redirect("/index/")
        return distribute(request)
    elif template=="checkissue.html":
        return checkissue(request,role)
    elif template=="homework_update.html":
        return homework_update(request,role)
    elif template=="homeworkcheck.html":
        if role!=1:
           request.session['error'] = '只有教师才能批改作业'
           return redirect("/index/")
        return homeworkcheck(request)
    elif template=="homeworkwrite.html":
        if role!=2:
           request.session['error'] = '只有学生才能编写作业'
           return redirect("/index/")
        return homeworkwrite(request)