from cmath import exp
from unicodedata import category
from django.shortcuts import render
from django.http import HttpRequest, HttpResponse
from expenses_api.forms import ExpenseForm
from expenses_api.models import Expense
from faker import Faker
import random

reverse_it=True
sort_param=""

def index(request):
    return render(request,'index.html')

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
        e=Expense(name=name,amount=amount,date=date,category=category)
        e.save()
        return display(request, "Added Successfully!")
        # add return to display
    else:
        return render(request,"add.html", {'form':form})

def display(request,message=''):
    #expenses=Expense.objects.order_by('date')
    expenses=Expense.objects.all().order_by('-date')
    return render(request,"display.html", {'expenses':expenses,'message':message})

def analysis(request):
    #prices=Expense.objects.all().order_by('-amount')
    dates=Expense.objects.all().order_by('date')
    size=len(dates)
    #dates=dates[size-10:size+1]
    #pd=zip(prices,dates)
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