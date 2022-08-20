from django import forms
from faker import Faker
from random import randint

CATEGORIES=[
    ('Food','Food'),
    ('Fun','Fun'),
    ('Car','Car'),
    ('Travel','Travel')
]
class ExpenseForm(forms.Form):
    name=forms.CharField(initial=Faker().company())
    amount=forms.IntegerField(initial=randint(200,1500))
    date=forms.DateField(initial=Faker().date())
    category=forms.CharField(label="Category", widget=forms.Select(choices=CATEGORIES))

class LoginForm(forms.Form):
    username=forms.CharField(initial="")
    password=forms.CharField(initial="")
