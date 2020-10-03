from django.db import models
from django.contrib.auth.models import User
from django import forms
from django.core.validators import MaxValueValidator, MinValueValidator
import datetime
# Create your models here.


class Todo(models.Model):
    title=models.CharField(max_length=100)
    memo=models.TextField(blank=True)
    created = models.DateTimeField(auto_now_add=True)
    datecompleted = models.DateTimeField(null=True)
    important = models.BooleanField(default=False)
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    def __str__(self):
        return self.title

def clean_password1(self):
  password1 = self.cleaned_data['password1']
  if len(password1) < 4:
      raise forms.ValidationError("password is too short")
  return password

class Contact(models.Model):
    contact_name = models.CharField(max_length=100,default="name")
    contact_email = models.EmailField(blank=True)
    contact_content = models.TextField(blank=True)

class MyProfile(models.Model):
    username = models.CharField(max_length=100,default="username")
    lead= models.CharField(max_length=100,null=True,blank=True)
    associate= models.CharField(max_length=100,null=True,blank=True)
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    def __str__(self):
        return self.username
class SendMultiMail(models.Model):
    sender= models.EmailField(blank=True)
    receivers = models.TextField(max_length=200,blank=True)
    subject = models.TextField(max_length=200,blank=True)
    body =  models.TextField(blank=True)
    created = models.DateTimeField(auto_now_add=True)
    schedule = models.DateTimeField(null=True)





class MyBiodata(models.Model):
    class Marital(models.TextChoices):
        married='yy'
        Not_married='nn'
        Not_Specified='ns'
    class Disabiliti(models.TextChoices):
        Yes='yy'
        No='nn'
        Not_Specified='ns'
    class Complexion(models.TextChoices):
        Fair='ff'
        Milky_Fair='mm'
        Very_Fair ='vf'
        Brown='br'
        Dark = 'dd'
        Normal = 'nn'
        Not_Specified='ns'
    class Diet(models.TextChoices):
        Vegitarian ='ve'
        Non_Vegetaria='nv'
        Eagitarian='eg'
        Not_Specified='ns'
    class Contact(models.TextChoices):
        Yes='yy'
        No='nn'
        Not_Specified='ns'
    class Profession(models.TextChoices):
        Accountant ='ac'
        Teacher='te'
        Technician='tc'
        Laborer='la'
        Banker='ba'
        Farmer='fa'
        Shop_Keeper='sh'
        Business_Man ='bm'
        Engineer='en'
        Doctor='do'
        others='ot'
        Not_Specified='ns'
    class Religion(models.TextChoices):
        Hindu='hi'
        Muslim='mu'
        Sikh='si'
        Parsi='pa'
        Not_Specified='ns'
    class CreatedBy(models.TextChoices):
        _Self='se'
        Parents='pa'
        Friedns='fr'
        Relatives='re'
        Others='ot'
        Not_Specified='ns'



    user = models.ForeignKey(User,on_delete=models.CASCADE)
    username = models.CharField(max_length=100,blank=True)
    name = models.CharField(max_length=100,default="")
    age = models.PositiveIntegerField(default=22, validators=[MinValueValidator(18), MaxValueValidator(100)])
    created_by = models.CharField(choices=CreatedBy.choices,max_length=2,default=CreatedBy.Not_Specified)
    marital_Status = models.CharField(choices=Marital.choices,max_length=2,default=Marital.Not_Specified)
    height = models.CharField(max_length=100,blank=True)
    physical_disability = models.CharField(choices=Disabiliti.choices,max_length=2,default=Disabiliti.Not_Specified)
    body_Weight=models.IntegerField(default=60)
    complexion = models.CharField(choices=Complexion.choices,max_length=2,default=Complexion.Not_Specified)
    DOB = models.DateField(default=datetime.date.today)
    Lives_in = models.CharField(max_length=50,blank=True)
    religion = models.CharField(choices=Religion.choices,max_length=2,default=Religion.Not_Specified)
    diet =  models.CharField(choices=Diet.choices,max_length=2,default=Diet.Not_Specified)
    contact_number = models.CharField(max_length=50,blank=True)
    email_ID = models.CharField(max_length=100,default="")
    is_Contact_visible = models.CharField(choices=Contact.choices,max_length=2,default=Contact.Not_Specified)
    Father_name = models.CharField(max_length=100,default="")
    Mother_name = models.CharField(max_length=100,default="")
    Family_details = models.CharField(max_length=500,blank=True)
    Education = models.CharField(max_length=100,blank=True)
    profession = models.CharField(choices=Profession.choices,max_length=2,default=Profession.Not_Specified)
    Income = models.CharField(max_length=100,default="30k",blank=True)
    About = models.CharField(max_length=500,blank=True)
    Photo=models.ImageField(upload_to='todo/images/',default='default.jpg')
    def __str__(self):
        return self.username
