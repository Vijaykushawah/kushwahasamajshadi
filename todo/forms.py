from django.forms import ModelForm
from .models import Todo,Contact,MyProfile,SendMultiMail,MyBiodata,BiodataPrivacy


class TodoForm(ModelForm):
    class Meta:
        model=Todo
        fields=['title','memo','important']

class ContactForm(ModelForm):
    class Meta:
        model=Contact
        fields = '__all__'

class MyProfileForm(ModelForm):
    class Meta:
        model=MyProfile
        fields = {'user'}
class SendMultiMailForm(ModelForm):
    class Meta:
        model=SendMultiMail
        fields = {'receivers','subject','sender','body'}
class MyBiodataForm(ModelForm):
    class Meta:
        model=MyBiodata
        fields = {'name','age','gender','height','body_Type','complexion','mother_Toung',
        'social','religion','cast','manglik','hobbies','education','profession','profession_type','job_location','annual_Income',
        'father_name','father_occupation','mother_name','mother_occupation','family_details','about',
        'contact_number','contact_privacy','email_ID','place','created_by','photo'}
    field_order=['name','age','gender','height','body_Type','complexion','mother_Toung',
        'social','religion','cast','manglik','hobbies','education','profession','profession_type','job_location','annual_Income',
        'father_name','father_occupation','mother_name','mother_occupation','family_details','about',
        'contact_number','contact_privacy','email_ID','place','created_by','photo']

class BiodataPrivacyForm(ModelForm):
    class Meta:
        model=BiodataPrivacy
        fields = {'biodataid','contact_visibility','email_visibility','education_detail_visibility','address_detail_visibility',
        'hide_profile'}
    field_order=['biodataid','contact_visibility','email_visibility','education_detail_visibility','address_detail_visibility',
    'hide_profile']
