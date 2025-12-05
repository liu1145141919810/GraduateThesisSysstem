from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

# Create your models here.
from django.db import models
class tb_login(models.Model):#用户账号表
    id = models.AutoField(primary_key=True)
    email = models.CharField(max_length=100,default='email')          #邮箱
    username = models.CharField(max_length=100,default='user')        #用户名
    pwd = models.CharField(max_length=100,default='pwd')              #密码   
    role = models.IntegerField(default=2)#0:管理员 1:教师 2:学生

class tb_teacher(models.Model):#教师表
    id = models.AutoField(primary_key=True)                           #教师ID
    email = models.CharField(max_length=100,default='email')          #邮箱
    username = models.CharField(max_length=100,default='user')        #用户名
    display_name = models.CharField(max_length=100, default='未设置')   #姓名
    gender = models.CharField(max_length=10,default='unknown')        #性别
    phone = models.CharField(max_length=20,default='000000')     #联系电话
    college = models.CharField(max_length=100,default='unknown')      #所属学院
    student_id = models.CharField(max_length=50,default='000000')     #工号
    major = models.CharField(max_length=100,default='unknown')        #专业


class tb_student(models.Model):#学生表
    id = models.AutoField(primary_key=True)                            #学生ID
    email = models.CharField(max_length=100,default='email')           #邮箱
    username = models.CharField(max_length=100,default='user')         #用户名
    display_name = models.CharField(max_length=100, default='未设置')   #姓名
    gender = models.CharField(max_length=10,default='unknown')         #性别
    phone = models.CharField(max_length=20,default='000000')           #联系电话
    college = models.CharField(max_length=100,default='unknown')       #所属学院
    student_id = models.CharField(max_length=50,default='000000')      #学号
    major = models.CharField(max_length=100,default='unknown')         #专业
    
class tb_topic(models.Model):#课题表
    id = models.AutoField(primary_key=True)
    title=models.CharField(max_length=200,default='untitled')

class tb_student_topic(models.Model):#学生课题关联表
    id = models.AutoField(primary_key=True)

class tb_content(models.Model):#内容表
    id = models.AutoField(primary_key=True) 
    write_id=models.IntegerField(default=0)

class tb_login_log(models.Model):#登录日志
    id = models.AutoField(primary_key=True)
    username=models.ForeignKey(tb_login,on_delete=models.CASCADE)
    log_time=models.DateTimeField(auto_now_add=True)
    STATUS_CHOICES=[
        ('success','Success'),
        ('fail','Fail')
    ]
    status=models.CharField(max_length=10,default='fail',choices=STATUS_CHOICES)#success/failed

class tb_notice(models.Model):#通知表
    id = models.AutoField(primary_key=True)
    read = models.BooleanField(default=False)
    send = models.BooleanField(default=False)
    showsend = models.BooleanField(default=True)
    showreceive = models.BooleanField(default=True)
    host = models.ForeignKey(tb_login, on_delete=models.CASCADE, related_name='notices_sent', null=True, blank=True)
    recipient = models.ForeignKey(tb_login, on_delete=models.CASCADE, related_name='notices_received', null=True, blank=True)
    subject = models.CharField(max_length=100, default='No subject')
    message = models.TextField(default='No message')
    timestamp = models.DateTimeField(auto_now_add=True, null=True, blank=True)

###后台执行函数

@receiver(post_save, sender=tb_notice)
def auto_delete_notice(sender, instance, **kwargs):
    # 如果两个显示都关闭，则自动删除这条消息
    if not instance.showsend and not instance.showreceive:
        instance.delete()

"""
python manage.py makemigrations
python manage.py migrate
"""

"""
123456@teach.com
teacher0
TeacherPwd123

54321@student.com
student0
54321Stu
"""