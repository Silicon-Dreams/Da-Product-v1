from django  import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import User, AdditionalUserInfo


class CustomUserForm(UserCreationForm):
    first_name = forms.CharField(max_length=100,required=True,widget=forms.TextInput(attrs={'placeholder': 'First Name','class': 'form-control',}))
    last_name = forms.CharField(max_length=100,required=True, widget=forms.TextInput(attrs={'placeholder': 'Last Name','class': 'form-control',}))
    username = forms.CharField(max_length=100,required=False,widget=forms.TextInput(attrs={"class":"form-control", "placeholder":"Enter username"}))
    email = forms.EmailField(required=True,widget=forms.TextInput(attrs={"class":"form-control", "placeholder":"Enter email"}))
    password1 = forms.CharField(max_length=50,required=True,widget=forms.PasswordInput(attrs={"class":"form-control",'data-toggle': 'password','id': 'password', "placeholder":"Enter password"}))
    password2 = forms.CharField(max_length=50,required=True,widget=forms.PasswordInput(attrs={"class":"form-control",'data-toggle': 'password','id': 'password', "placeholder":"Confirm password"}))
    
    phoneNumber = forms.CharField(max_length=50,required=True,widget=forms.TextInput(attrs={"class":"form-control", "placeholder":"Phone Number"}))
    country = forms.CharField(max_length=50,required=True,widget=forms.TextInput(attrs={"class":"form-control", "placeholder":"Country"}))
    
    
    FILTER_CHOICES = (
        ('male', 'male'),
        ('female', 'female'),
    )

    gender = forms.ChoiceField(choices = FILTER_CHOICES)

    class Meta:
        model = User
        fields = ["first_name","last_name","username","email", "password1", "password2", "country", "phoneNumber", "gender"]
        
        
        
class UserForm(forms.ModelForm):
    class Meta:
        model = AdditionalUserInfo
        fields = '__all__'
        exclude = ['user']
    
    
class EditProfileForm(UserChangeForm):
    first_name = forms.CharField(max_length=100,required=True,widget=forms.TextInput(attrs={'placeholder': 'First Name','class': 'form-control',}))
    last_name = forms.CharField(max_length=100,required=True, widget=forms.TextInput(attrs={'placeholder': 'Last Name','class': 'form-control',}))
    username = forms.CharField(max_length=100,required=True,widget=forms.TextInput(attrs={"class":"form-control", "placeholder":"Enter username"}))
    email = forms.EmailField(required=True,widget=forms.TextInput(attrs={"class":"form-control", "placeholder":"Enter email"}))
    password = None
    
    class Meta:
        model = User
        fields = ('username','email', 'first_name','last_name')