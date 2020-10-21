from django.db import models
from django.contrib.auth.models import User
from django import forms
from django.core.validators import MaxValueValidator, MinValueValidator
import datetime
from django_resized import ResizedImageField
from django.utils.translation import gettext_lazy as _
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


class BiodataPrivacy(models.Model):
    class Contact(models.TextChoices):
        Visible_To_All='Visible_To_All'
        Visible_To_ME='Visible_To_ME'
        Hidden='Hidden'
        Not_Specified='Not_Specified'
    class HideBiodata(models.TextChoices):
        Hidden='Hidden'
        Show='Show'
        Not_Specified='Not_Specified'
    user = models.ForeignKey(User,on_delete=models.CASCADE,null=True)
    username = models.CharField(max_length=100,blank=True)
    biodataid = models.CharField(max_length=100,default='1')
    contact_visibility = models.CharField(choices=Contact.choices,max_length=20,default=Contact.Visible_To_ME)
    email_visibility = models.CharField(choices=Contact.choices,max_length=20,default=Contact.Visible_To_ME)
    education_detail_visibility =models.CharField(choices=Contact.choices,max_length=20,default=Contact.Visible_To_All)
    address_detail_visibility=models.CharField(choices=Contact.choices,max_length=20,default=Contact.Visible_To_All)
    hide_profile =models.CharField(choices=HideBiodata.choices,max_length=20,default=HideBiodata.Show)


class MyBiodata(models.Model):
    class Marital(models.TextChoices):
        married='married'
        Never_married='Never_married'
        Not_Specified='Not_Specified'
    class Disabiliti(models.TextChoices):
        Yes='Yes'
        No='No'
        Not_Specified='Not_Specified'
    class Complexion(models.TextChoices):
        Fair='Fair'
        Milky_Fair='Milky_Fair'
        Very_Fair ='Very_Fair'
        Brown='Brown'
        Dark = 'Dark'
        Normal = 'Normal'
        Not_Specified='Not_Specified'
    class Diet(models.TextChoices):
        Vegitarian ='Vegitarian'
        Non_Vegetaria='Non_Vegetaria'
        Eagitarian='Eagitarian'
        Not_Specified='Not_Specified'
    class Contact(models.TextChoices):
        Visible_To_All='Visible_To_All'
        Visible_To_me='Visible_To_me'
        Hidden='Hidden'
        Not_Specified='Not_Specified'
    class Profession(models.TextChoices):
        Accountant ='Accountant'
        Teacher='Teacher'
        Technician='Technician'
        Laborer='Laborer'
        Banker='Banker'
        Farmer='Farmer'
        Shop_Keeper='Shop_Keeper'
        Business_Man ='Business_Man'
        Engineer='Engineer'
        Doctor='Doctor'
        Lawyer='Lawyer'
        others='others'
        Not_Specified='Not_Specified'
    class Religion(models.TextChoices):
        Hindu='Hindu'
        Muslim='Muslim'
        Sikh='Sikh'
        Parsi='Parsi'
        Not_Specified='Not_Specified'
    class CreatedBy(models.TextChoices):
        _Self='_Self'
        Parents='Parents'
        Friedns='Friedns'
        Relatives='Relatives'
        Others='Others'
        Not_Specified='Not_Specified'
    class BodyType(models.TextChoices):
        Slim = 'Slim'
        Average = 'Average'
        Fit = 'Fit'
        Healthy ='Healthy'
        Chubby ='Chubby'
        Fatty='Fatty'
        Not_Specified='Not_Specified'
    class MotherToung(models.TextChoices):
        Hindi='Hindi'
        English='English'
        Both='Both'
        Not_Specified='Not_Specified'
    class Social(models.TextChoices):
        Religious_Background='Religious_Background'
        Normal='Normal'
        Both='Both'
        Not_Specified='Not_Specified'
    class Cast(models.TextChoices):
        Kushwaha='Kushwaha'
        Maurya='Maurya'
        Shakya='Shakya'
        Saini='Saini'
        Not_Specified='Not_Specified'
    class ProfessionType(models.TextChoices):
        Private='Private'
        Government='Government'
        Semi_Govt='Semi_Govt'
        Contratual='Contratual'
        Others='Others'
        Not_Specified='Not_Specified'
    class MotherOccupation(models.TextChoices):
        House_wife='House_wife'
        Accountant ='Accountant'
        Teacher='Teacher'
        Technician='Technician'
        Laborer='Laborer'
        Banker='Banker'
        Farmer='Farmer'
        Shop_Keeper='Shop_Keeper'
        Business_Man ='Business_Man'
        Engineer='Engineer'
        Doctor='Doctor'
        others='others'
        Not_Specified='Not_Specified'
    class Gender(models.TextChoices):
        Female = 'Female'
        Male = 'Male'
        Not_Specified='Not_Specified'
    class Manglik(models.TextChoices):
        Yes = 'Yes'
        No = 'No'
        Not_Specified='Not_Specified'
    class Contact(models.TextChoices):
        Visible_To_All='Visible_To_All'
        Visible_To_ME='Visible_To_ME'
        Hidden='Hidden'
        Not_Specified='Not_Specified'
    class HideBiodata(models.TextChoices):
        Hidden='Hidden'
        Show='Show'
        Not_Specified='Not_Specified'




    user = models.ForeignKey(User,on_delete=models.CASCADE)
    username = models.CharField(max_length=100,blank=True)
    name = models.CharField(max_length=100,default="")
    age = models.PositiveIntegerField(default=22, validators=[MinValueValidator(18), MaxValueValidator(100)])
    created_by = models.CharField(choices=CreatedBy.choices,max_length=20,default=CreatedBy.Others)
    marital_Status = models.CharField(choices=Marital.choices,max_length=20,default=Marital.Never_married)
    gender = models.CharField(choices=Gender.choices,max_length=20,default=Gender.Not_Specified)
    hobbies = models.CharField(max_length=400,blank=True)
    mother_Toung = models.CharField(choices=MotherToung.choices,max_length=20,default=MotherToung.Hindi)
    social = models.CharField(choices=Social.choices,max_length=20,default=Social.Religious_Background)
    body_Type = models.CharField(choices=BodyType.choices,max_length=20,default=BodyType.Average)
    cast = models.CharField(choices=Cast.choices,max_length=20,default=Cast.Kushwaha)
    manglik = models.CharField(choices=Manglik.choices,max_length=20,default=Manglik.No)
    height = models.CharField(max_length=100,blank=True)
    physical_disability = models.CharField(choices=Disabiliti.choices,max_length=20,default=Disabiliti.No)
    body_Weight=models.IntegerField(default=60)
    complexion = models.CharField(choices=Complexion.choices,max_length=20,default=Complexion.Fair)
    DOB = models.CharField(max_length=100,blank=True)
    place = models.CharField(max_length=500,blank=True)
    religion = models.CharField(choices=Religion.choices,max_length=20,default=Religion.Hindu)
    diet =  models.CharField(choices=Diet.choices,max_length=20,default=Diet.Vegitarian)
    contact_number = models.CharField(max_length=50,blank=True)
    email_ID = models.CharField(max_length=100,blank=True)
    contact_privacy = models.CharField(choices=Contact.choices,max_length=20,default=Contact.Visible_To_All)
    father_name = models.CharField(max_length=100,default="")
    father_occupation = models.CharField(choices=Profession.choices,max_length=20,default=Profession.Not_Specified)
    mother_name = models.CharField(max_length=100,default="")
    mother_occupation = models.CharField(choices=MotherOccupation.choices,max_length=20,default=MotherOccupation.House_wife)
    family_details = models.CharField(max_length=500,blank=True)
    education = models.CharField(max_length=500,blank=True)
    profession = models.CharField(choices=Profession.choices,max_length=20,default=Profession.Not_Specified)
    profession_type = models.CharField(choices=ProfessionType.choices,max_length=20,default=ProfessionType.Not_Specified)
    job_location = models.CharField(max_length=500,blank=True)
    annual_Income = models.CharField(max_length=100,blank=True)
    about = models.CharField(max_length=500,blank=True)
    photo=ResizedImageField(size=[400, 360],quality=100,upload_to='todo/images/',default='default.jpg')
    created_at = models.DateTimeField(auto_now_add=True)
    last_updated_at = models.DateTimeField(null=True)
    deletedrow=models.BooleanField(default=False)
    # permissions
    contact_visibility = models.CharField(choices=Contact.choices,max_length=20,default=Contact.Visible_To_ME)
    email_visibility = models.CharField(choices=Contact.choices,max_length=20,default=Contact.Visible_To_ME)
    education_detail_visibility =models.CharField(choices=Contact.choices,max_length=20,default=Contact.Visible_To_All)
    address_detail_visibility=models.CharField(choices=Contact.choices,max_length=20,default=Contact.Visible_To_All)
    hide_profile =models.CharField(choices=HideBiodata.choices,max_length=20,default=HideBiodata.Show)
    def __str__(self):
        return self.username

class MyBiodataInbox(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE,null=True)
    mybiodataid=models.CharField(max_length=200,blank=True)
    msgfromusername = models.CharField(max_length=200,blank=True)
    subject = models.CharField(max_length=200,null=True)
    msg =  models.TextField(null=True)
    created = models.DateTimeField(auto_now_add=True)
class MyBiodataChatbox(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE,null=True)
    msgtousername = models.CharField(max_length=200,blank=True)
    subject = models.CharField(max_length=200,null=True)
    msg =  models.TextField(null=True)
    created = models.DateTimeField(auto_now_add=True)
class BiodataHelp(models.Model):
    name = models.CharField(max_length=100,default="")
    email_id = models.EmailField(default="")
    contact_number = models.CharField(max_length=100,default="")
    subject=models.CharField(max_length=100,default="")
    query = models.TextField(blank=True)
class RequestsForApproval(models.Model):
    class ContactView(models.TextChoices):
        yes='yes'
        no='no'
        Not_Specified='Not_Specified'
    class RequestType(models.TextChoices):
        contact='contact'
        connect='connect'
        Not_Specified='Not_Specified'
    user = models.ForeignKey(User,on_delete=models.CASCADE,null=True)
    userbiodataid = models.CharField(max_length=200,null=True)
    requestfromusername = models.CharField(max_length=200,blank=True)
    requesttousername = models.CharField(max_length=200,blank=True)
    requesttobiodataid = models.CharField(max_length=200,null=True)
    requesttoemailid=models.CharField(max_length=200,blank=True)
    request_type = models.CharField(choices=RequestType.choices,max_length=20,default=RequestType.Not_Specified)
    contact_view_request = models.CharField(choices=ContactView.choices,max_length=20,default=ContactView.Not_Specified)
    connect_request = models.CharField(choices=ContactView.choices,max_length=20,default=ContactView.Not_Specified)
    created = models.DateTimeField(auto_now_add=True)
