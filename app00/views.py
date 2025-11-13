from django.shortcuts import render,redirect
from django.http import HttpResponse
from DB.DB_operate import operate
# Create your views here.
params=params={# it is the database I want
    'host': 'localhost',
    'database': 'Log_base',
    'user':'postgres',
    'password':'554775861',
    'port':5432
}
def login(request):
    #return HttpResponse("success login")
    if request.method=="GET":
        return render(request,"login.html")
    elif request.method=="POST":
        #print("=================================")
        #print("=====POST METHOD=====")
        user=request.POST.get("user")
        pwd=request.POST.get("pwd")
        #print("Attention! --- following is login info:")
        #print(user,pwd)
        if operate("signin",params,None,user,pwd):
            #print("Login successful, redirecting to index page")
            return render(request,"index.html")
        else:
            return render(request,"login.html")
    return redirect("index/")
def register(request):
    if request.method=="GET":
        #print("=================================")
        #print("====GET METHOD====")
        #print("Attention! --- following is register info:")
        return render(request,"registration.html")
    elif request.method=="POST":
        #print("=====POST METHOD=====")
        mail=request.POST.get("email")
        user=request.POST.get("usr")
        pwd=request.POST.get("pwd")
        if operate("register",params,mail,user,pwd):
            #print("Registration successful, redirecting to index page")
            return redirect("/login/")
        else:
            return render(request,"registration.html")
def index(request):
    return render(request,"index.html")
  