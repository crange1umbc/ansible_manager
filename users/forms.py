from django import forms
from django.contrib.auth.models import User 
from django.contrib.auth.forms import UserCreationForm

class UserRegisterForm(UserCreationForm):
    email=forms.EmailField()
    # aff_choices=(
    #     ('TA/Grader','TA/Grader'),
    #     ('Instructor','Instructor'),
    # )
    # umbc_affiliation=forms.ChoiceField(choices=aff_choices)

    class Meta:
        model=User
        fields=['username','email','password1','password2']
