from django.contrib import admin
from app00.models import *

# Register your models here.
def deal_message(message):
    print("Dealing message in admin.py")
    ## 修改每个msg的内容
    box=[]
    for msg in message:
        #msg.message = msg.message.upper()  # 示例处理：将内容转换为大写
        msg.source = tb_login.objects.get(id=msg.host_id).username
        msg.email = tb_login.objects.get(id=msg.host_id).email
        ##时间戳精确到分钟为止
        msg.timestamp = msg.timestamp.strftime("%Y-%m-%d %H:%M")
        if  msg.showreceive:
            box.append(msg)
    return box

def myissue(request):
    pass

def distribute(request):
    print("发布相关命令")
    pass

def checkissue(request):
    pass