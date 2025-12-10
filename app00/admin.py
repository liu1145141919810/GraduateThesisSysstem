from django.contrib import admin
from app00.models import *
from django.shortcuts import render,redirect
from datetime import datetime
import json
from django.utils import timezone
from django.db.models import Count, Q
from django.core.cache import cache


def tellit(template):
    if(template=="myissue.html" or template=="distribute.html" or template=="checkissue.html"
    or template=="homework_update.html" or template=="homeworkcheck.html"
    or template=="homeworkwrite.html" or template=="finishwork.html"):
        return True
    return False

# Register your models here.
def deal_message(message):
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
    id=request.session.get('user_id')
    student=tb_student.objects.get(login_id=id)
    if request.method=="POST":
        data=json.loads(request.body)
        content_obj=tb_content.objects.get(id=int(data['content_id']))
        content_obj.content=data['content']
        content_obj.timestamp=datetime.now()
        stu_topic=tb_student_topic.objects.get(student_id=student.id,topic_id=content_obj.topic_id.id)
        stu_topic.state="已完成"
        content_obj.save()
        stu_topic.save()
    message1=tb_student_topic.objects.filter(student_id=student.id)
    message2=[]
    for msg in message1:
        topic=tb_topic.objects.get(id=msg.topic_id.id)
        topic.teacher=tb_teacher.objects.get(id=topic.teacher_id.id).username
        stu_topic=tb_student_topic.objects.get(student_id=student.id,topic_id=topic.id)
        topic.write_id=stu_topic.content_id.id
        component=tb_content.objects.get(id=stu_topic.content_id.id)
        topic.write_content=component.content
        if timezone.now() < topic.timestamp:
           message2.append(topic)
        else:
            stu_topic.state="已截止"
            stu_topic.save()
    return render(request,"myissue.html",{"message":message2})

def distribute(request):
    id=request.session.get('user_id')
    teacher=tb_teacher.objects.get(login_id=id)
    if request.method=="POST":
        data= json.loads(request.body)
        if data['type']==1:
            deadline_str=data['deadline_year']+"-"+ data['deadline_day'] +"T"+data['deadline_time']+":00"
            time= datetime.fromisoformat(deadline_str)
            #try:
            tb_topic.objects.create(
                title=data['title'],
                profession=data['collage'],
                scale=int(data['capacity']),
                teacher_id=teacher,
                introduction=data['content'],
                timestamp=time
                )
            #except Exception as e:
                #print("Error creating topic:", e)
        if data['type']==2:
            print("modifying data:",data)
            deadline_str = f"{data['year']}-{data['month_day']} {data['time']}:00"
            time = datetime.strptime(deadline_str, "%Y-%m-%d %H:%M:%S")
            topic=tb_topic.objects.get(id=int(data['title_id'])) 
            topic.profession=data['college']
            topic.scale=int(data['scale'])
            topic.timestamp=time
            topic.introduction=data['introduction']
            topic.save()
            print("Modified topic:",topic)
            return redirect("/index/distribute.html")
    print("teacher id:",teacher.id)
    cache.clear()
    message=tb_topic.objects.filter(teacher_id=teacher.id).order_by('-timestamp')
    return render(request,"distribute.html",{"message":message,"college":teacher.college,"teacher":teacher.username})

def checkissue(request,role):
    print(request.method,"method")
    try:
        student=tb_student.objects.get(login_id=request.session.get('user_id'))
    except tb_student.DoesNotExist:
        student = None
    message=tb_topic.objects.filter(timestamp__gt=datetime.now()).order_by('-timestamp')
    if request.method=="POST":
        if role==1:
            request.session['error']="只有学生才能选择课题！"
            return render(request,"checkissue.html",{"message":message})
        data=json.loads(request.body)
        topic=tb_topic.objects.get(id=int(data['title_id']))
        if(topic.scale<=0):
            request.session['error']="该课题名额已满！"
            return render(request,"checkissue.html",{"message":message})
        if(topic.profession!=student.college):
            request.session['error']="该课题不属于你的学院！"
            return render(request,"checkissue.html",{"message":message})
        try:
            tb_content.objects.create(
                content="",
                stu_id=tb_student.objects.get(login_id=request.session.get('user_id')),
                topic_id=tb_topic.objects.get(id=int(data['title_id']))
            )
            topic.scale-=1
            topic.save() 
        except Exception as e:
            request.session['error']="不能这样操作，请重试！"
            return render(request,"checkissue.html",{"message":message})
        try:
            tb_student_topic.objects.create(
                student_id=tb_student.objects.get(login_id=request.session.get('user_id')),
                topic_id=tb_topic.objects.get(id=int(data['title_id'])),
                content_id=tb_content.objects.get(
                    stu_id=tb_student.objects.get(login_id=request.session.get('user_id')),
                    topic_id=tb_topic.objects.get(id=int(data['title_id']))
                )  )
        except Exception as e:
            request.session['error']="不能重复选择！"
            return render(request,"checkissue.html",{"message":message})
        # 处理数据
    for msg in message:
        teacher_obj=tb_teacher.objects.get(id=msg.teacher_id.id)
        msg.teacher=teacher_obj.username
    error=request.session.pop('error',None)
    return render(request,"checkissue.html",{"message":message,"error":error})

def homework_update(request,role):
    message=[]
    teacher=None
    student=None
    if role==2:#学生端
        student=tb_student.objects.get(login_id=request.session.get('user_id'))
        stu_topic=tb_student_topic.objects.filter(student_id=student.id)
        for item in stu_topic:
            if item.state=="已评分" :
                message.append({
                "title":tb_topic.objects.get(id=item.topic_id.id).title,
                "evaluation":item.evaluation,
                "score":item.score,
                })
    if role==1:#教师端  
        type=="teacher"
        teacher=tb_teacher.objects.get(login_id=request.session.get('user_id'))
        topic=tb_topic.objects.filter(teacher_id=tb_teacher.objects.get(login_id=request.session.get('user_id')).id)
        for t in topic:
            counts = tb_student_topic.objects.filter(topic_id=t.id).aggregate(
            zero_19=Count('id', filter=Q(score__lte=19)),
            _20_39=Count('id', filter=Q(score__gte=20, score__lte=39)),
            _40_59=Count('id', filter=Q(score__gte=40, score__lte=59)),
            _60_69=Count('id', filter=Q(score__gte=60, score__lte=69)),
            _70_79=Count('id', filter=Q(score__gte=70, score__lte=79)),
            _80_84=Count('id', filter=Q(score__gte=80, score__lte=84)),
            _85_89=Count('id', filter=Q(score__gte=85, score__lte=89)),
            _90_94=Count('id', filter=Q(score__gte=90, score__lte=94)),
            _95_100=Count('id', filter=Q(score__gte=95, score__lte=100)),
            )
            print(counts)
            one_static = {
                "0_19": counts['zero_19'],
                "20_39": counts['_20_39'],
                "40_59": counts['_40_59'],
                "60_69": counts['_60_69'],
                "70_79": counts['_70_79'],
                "80_84": counts['_80_84'],
                "85_89": counts['_85_89'],
                "90_94": counts['_90_94'],
                "95_100": counts['_95_100'],
            }
            total_counts = sum(one_static.values())
            if total_counts == 0:
                frequency = {k: 0 for k in one_static}
            else:
                frequency = {k: ((one_static[k]*100) / total_counts) for k in one_static}
            message.append({
            "statics": one_static,
            "frequency": frequency,
            "topic_id": t.id,
            "topic_title": t.title,
            })
    return render(request,"homework_update.html",{"message":message,"teacher":teacher,"student":student})

def homeworkcheck(request):
    teacher=tb_teacher.objects.get(login_id=request.session.get('user_id'))
    if request.method=="POST":
        data=json.loads(request.body)
        stu_topic=tb_student_topic.objects.get(id=int(data['content_id']))
        stu_topic.evaluation=data['content']
        stu_topic.score=min(max(int(data['score']),0),100)
        stu_topic.state="已评分"
        stu_topic.save()
        #print("Received evaluation11111111:",data['content'],data['score'])
    stu_topic=tb_student_topic.objects.filter(topic_id__teacher_id=teacher.id).order_by('score')
    message=[]
    for item in stu_topic:
        topic=tb_topic.objects.get(id=item.topic_id.id)
        student=tb_student.objects.get(id=item.student_id.id)
        content=tb_content.objects.get(id=item.content_id.id)
        msg=type('obj', (object,), {})()  # 创建一个空对象
        msg.title=topic.title
        msg.profession=topic.profession
        msg.student=student.username
        msg.introduction=topic.introduction
        msg.write_content=content.content
        msg.write_id=item.id
        msg.timestamp=topic.timestamp
        msg.scale=topic.scale
        msg.update_time=content.timestamp.strftime("%Y-%m-%d %H:%M")
        msg.topic_id=topic.id
        msg.evaluation=item.evaluation
        msg.score=item.score
        message.append(msg)
    return render(request,"homeworkcheck.html",{"message":message})
def homeworkwrite(request):
    request.session['error']="这个页面并没有实现，直接在“我的选题”页面编写"
    return redirect("/index/")