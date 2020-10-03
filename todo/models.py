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
        Visible_To_All='pu'
        Visible_To_me='pr'
        Hidden='hi'
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
    class BodyType(models.TextChoices):
        Slim = 'sl'
        Average = 'av'
        Fit = 'ft'
        Healthy ='he'
        Chubby ='ch'
        Fatty='fa'
        Not_Specified='ns'
    class MotherToung(models.TextChoices):
        Hindi='hi'
        English='en'
        Both='bt'
        Not_Specified='ns'
    class Social(models.TextChoices):
        Religious_Background='re'
        Normal='nr'
        Both='bt'
        Not_Specified='ns'
    class Cast(models.TextChoices):
        Kushwaha='ku'
        Maurya='mr'
        Shakya='sh'
        Saini='sa'
        Not_Specified='ns'
    class ProfessionType(models.TextChoices):
        Private='pr'
        Government='go'
        Semi_Govt='sg'
        Contratual='ca'
        Others='ot'
        Not_Specified='ns'
    class MotherOccupation(models.TextChoices):
        House_wife='hw'
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



    user = models.ForeignKey(User,on_delete=models.CASCADE)
    username = models.CharField(max_length=100,blank=True)
    name = models.CharField(max_length=100,default="")
    age = models.PositiveIntegerField(default=22, validators=[MinValueValidator(18), MaxValueValidator(100)])
    created_by = models.CharField(choices=CreatedBy.choices,max_length=2,default=CreatedBy.Not_Specified)
    marital_Status = models.CharField(choices=Marital.choices,max_length=2,default=Marital.Not_Specified)
    mother_Toung = models.CharField(choices=MotherToung.choices,max_length=2,default=MotherToung.Hindi)
    social = models.CharField(choices=Social.choices,max_length=2,default=Social.Not_Specified)
    body_Type = models.CharField(choices=BodyType.choices,max_length=2,default=BodyType.Average)
    cast = models.CharField(choices=Cast.choices,max_length=2,default=Cast.Not_Specified)
    height = models.CharField(max_length=100,blank=True)
    physical_disability = models.CharField(choices=Disabiliti.choices,max_length=2,default=Disabiliti.Not_Specified)
    body_Weight=models.IntegerField(default=60)
    complexion = models.CharField(choices=Complexion.choices,max_length=2,default=Complexion.Fair)
    DOB = models.DateField(default=datetime.date.today)
    place = models.CharField(max_length=50,blank=True)
    religion = models.CharField(choices=Religion.choices,max_length=2,default=Religion.Not_Specified)
    diet =  models.CharField(choices=Diet.choices,max_length=2,default=Diet.Not_Specified)
    contact_number = models.CharField(max_length=50,blank=True)
    email_ID = models.CharField(max_length=100,blank=True)
    contact_privacy = models.CharField(choices=Contact.choices,max_length=2,default=Contact.Not_Specified)
    father_name = models.CharField(max_length=100,default="")
    father_occupation = models.CharField(choices=Profession.choices,max_length=2,default=Profession.Not_Specified)
    mother_name = models.CharField(max_length=100,default="")
    mother_occupation = models.CharField(choices=MotherOccupation.choices,max_length=2,default=MotherOccupation.House_wife)
    family_details = models.CharField(max_length=500,blank=True)
    education = models.CharField(max_length=100,blank=True)
    profession = models.CharField(choices=Profession.choices,max_length=2,default=Profession.Not_Specified)
    profession_type = models.CharField(choices=ProfessionType.choices,max_length=2,default=ProfessionType.Not_Specified)
    job_location = models.CharField(max_length=50,blank=True)
    annual_Income = models.CharField(max_length=50,blank=True)
    about = models.CharField(max_length=500,blank=True)
    photo=models.ImageField(upload_to='todo/images/',default='default.jpg')
    def __str__(self):
        return self.username
