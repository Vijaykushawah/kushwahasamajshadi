from django.forms import ModelForm
from .models import Todo,Contact,MyProfile,SendMultiMail,MyBiodata


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
        fields = '__all__'
