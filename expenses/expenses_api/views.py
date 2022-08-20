
from django.shortcuts import render, redirect
from django.http import HttpRequest, HttpResponse
from expenses_api.forms import ExpenseForm, LoginForm
from expenses_api.models import Expense
from faker import Faker
import random
import sqlite3

reverse_it=True
sort_param=""


def index(request):
    if request.session:
        return render(request,'index.html')
    else:
        return HttpResponse('Unauthorized', status=401)

def login(request):
    if request.method=='POST':
        loginform=LoginForm(request.POST)
        username=loginform.data["username"]
        password=loginform.data["password"]
        con=sqlite3.connect('users.db')
        cur=con.cursor()
        rs=cur.execute(f"select * from users where name='{username}' and password='{password}'")
        row=rs.fetchone()
        if row:
            id=row[0]
            name=row[1]
            request.session["name"]=name
            request.session["id"]=id
            return redirect('display')
        else:
            return HttpResponse('Unauthorized', status=401)
    else:
        loginform=LoginForm()
        return render(request,"login.html",{"form":loginform})

def view_item(request):
    item=Expense.objects.get(id=request.GET["id"])
    return render(request,"item.html", {'item':item})        

def sort(request):
    global reverse_it
    sort_by=request.GET["sort_by"]
    # add state:
    if not reverse_it:
        expenses=Expense.objects.all().order_by('-'+sort_by)
        reverse_it=not reverse_it
    else:
        expenses=Expense.objects.all().order_by(sort_by)
        reverse_it=not reverse_it
    return render(request,"display.html", {'expenses':expenses})

def add(request):   
    name=Faker().company()
    amount=random.randint(200,1500)
    date=Faker().date()
    category=random.choice([
        'Food',
        'Fun',
        'Car',
        'Travel'
    ]
    )
    form=ExpenseForm(initial={'name':name,'amount':amount,'date':date,'category':category})
    if request.method=="POST":
        form=ExpenseForm(request.POST)
        name=form.data["name"]
        date=form.data["date"]
        category=form.data["category"]
        amount=int(form.data["amount"])+random.randrange(1,50)
        id=request.session.get("id")
        e=Expense(user_id=id,name=name,amount=amount,date=date,category=category)
        e.save()
        return display(request, "Added Successfully!")
    else:
        return render(request,"add.html", {'form':form})

def display(request,message=''):
    if request.session.get("id"):
        expenses=Expense.objects.filter(user_id=request.session.get("id")).order_by('-date')
        return render(request,"display.html", {'expenses':expenses,'message':message, "username":request.session.get("name")})
    else:
        return HttpResponse('Unauthorized', status=401)
    
def analysis(request):
    dates=Expense.objects.all().order_by('date')
    size=len(dates)
    return render(request,"analysis.html",{'dates':dates[size-7:size]})

def search(request):
    form=ExpenseForm(request.POST)
    q=form.data["q"]
    expenses=Expense.objects.filter(name__contains=q) | Expense.objects.filter(category__contains=q)
    return render(request,"display.html", {'expenses':expenses})
    

def remove(request):
    if request.method=="POST":
        form=ExpenseForm(request.POST)
        id=form.data["id"]
        expense=Expense.objects.get(id=id)
        expense.delete()
        return display(request,f"removed expense {id}")
    else:
        return HttpResponse("remove")
