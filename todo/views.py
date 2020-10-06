from django.shortcuts import render,redirect,get_object_or_404,get_list_or_404
from django.contrib.auth.forms import UserCreationForm,AuthenticationForm
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.contrib.auth import login,logout,authenticate
from .forms import TodoForm,ContactForm,MyProfileForm,SendMultiMailForm,MyBiodataForm,BiodataPrivacyForm,BiodataHelpForm,RequestsForApprovalForm
from .models import Todo,Contact,MyProfile,SendMultiMail,MyBiodata,BiodataPrivacy,MyBiodataInbox,MyBiodataChatbox,BiodataHelp,RequestsForApproval
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_protect
import re,random,datetime
import csv,logging,xlwt,googletrans

from django.http import HttpResponse,JsonResponse
from googletrans import Translator
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.forms.models import model_to_dict
import json
# Create your views here.
logger = logging.getLogger(__name__)
def signupuser(request):
    if request.method == 'GET':
        return render(request,'todo/signupuser.html',{'form':UserCreationForm()})
    else:
        #create a new User
        if request.POST['password1'] == request.POST['password2']:
            if len(request.POST['password1'])<8:
                return render(request,'todo/signupuser.html',{'form':UserCreationForm(),'error':"Passowrd length is too short"})
            elif not re.findall('\d',request.POST['password1']):
                return render(request,'todo/signupuser.html',{'form':UserCreationForm(),'error':"Passowrd must conain atlease 1 digit 0-9"})
            elif not re.findall('[A-Z]',request.POST['password1']):
                return render(request,'todo/signupuser.html',{'form':UserCreationForm(),'error':"Passowrd must conain atlease 1 capital letter"})
            elif not re.findall('[a-z]',request.POST['password1']):
                return render(request,'todo/signupuser.html',{'form':UserCreationForm(),'error':"Passowrd must conain atlease 1 small letter"})
            elif not re.findall('[()[\]{}|\\`~!@#$%^&*_\-+=;:\'",<>./?]',request.POST['password1']):
                return render(request,'todo/signupuser.html',{'form':UserCreationForm(),'error':"Passowrd must conain atlease 1 special character"})




            else:
                try:
                    user=User.objects.create_user(request.POST['username'],password=request.POST['password1'])
                    user.save()
                    login(request,user)
                    return redirect(currenttodos)
                except IntegrityError:
                    return render(request,'todo/signupuser.html',{'form':UserCreationForm(),'error':"User already exists"})
        else:
            #Tell the user the password didn't match
            #println("Passoword didn't match")
            return render(request,'todo/signupuser.html',{'form':UserCreationForm(),'error':"Passwod didn't match"})
@login_required
def currenttodos(request):
    #todos=Todo.objects.all()
    #we want user specific database objects
    todos = Todo.objects.filter(user=request.user,datecompleted__isnull=True)
    return render(request,'todo/currenttodos.html',{'todos':todos})
@login_required
def completedtodos(request):
    #todos=Todo.objects.all()
    #we want user specific database objects
    todos = Todo.objects.filter(user=request.user,datecompleted__isnull=False).order_by('-datecompleted')
    return render(request,'todo/completedtodos.html',{'todos':todos})

@login_required
def viewtodo(request,todo_pk):
    todo=get_object_or_404(Todo,pk=todo_pk,user=request.user)
    if request.method == 'GET':
        form =  TodoForm(instance=todo)
        return render(request,'todo/viewtodo.html',{'todo':todo,'form':form})
    else:
        try:
            form=TodoForm(request.POST,instance=todo)
            form.save()
            return redirect(currenttodos)
        except ValueError:
            return render(request,'todo/viewtodo.html',{'todo':todo,'form':form,'error':"Bad info passed.Please try again."})

@login_required
def getassociatestatustodo(request,associateusername):
    try:
        get_list_or_404(MyProfile,user=request.user,associate=associateusername,username=request.user.username)
    except:
        currentwork=[]
        completedwork=[]
        return render(request,'todo/getassociatestatustodo.html',{'currentwork':currentwork,'completedwork':completedwork,'error':"Sorry, selected user is not your associate!!"})
    associate=get_object_or_404(User,username=associateusername)
    currentwork=Todo.objects.filter(user=associate,datecompleted__isnull=True)
    completedwork=Todo.objects.filter(user=associate,datecompleted__isnull=False).order_by('-datecompleted')
    return render(request,'todo/getassociatestatustodo.html',{'currentwork':currentwork,'completedwork':completedwork})

@login_required
def exportdatatodo(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="{}{}.csv"'.format(request.user.username,"_currentwork")
    todos = Todo.objects.filter(user=request.user,datecompleted__isnull=True)
    writer = csv.writer(response)
    writer.writerow(['Title', 'memo', 'Created', 'Datecompleted','Createdby','isImportant'])
    for row in todos:
        writer.writerow([row.title,row.memo,row.created,row.datecompleted,row.user.username,row.important,])
    return response

@login_required
def exportexceldatatodo(request):
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename="{}{}.xls"'.format(request.user.username,"_currentwork")
    wb = xlwt.Workbook(encoding='utf-8')
    ws = wb.add_sheet('CurrentWork')

    # Sheet header, first row
    row_num = 0

    font_style = xlwt.XFStyle()
    font_style.font.bold = True

    columns=['Title', 'memo', 'isImportant']
    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], font_style)
    # Sheet body, remaining rows
    font_style = xlwt.XFStyle()
    todos = Todo.objects.filter(user=request.user,datecompleted__isnull=True).values_list('title','memo','important')
    for row in todos:
        row_num += 1
        for col_num in range(len(row)):
            ws.write(row_num, col_num, row[col_num], font_style)

    wb.save(response)
    return response

@login_required
def exportcompledatatodo(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="{}{}.csv"'.format(request.user.username,"_completedWork")
    todos = Todo.objects.filter(user=request.user,datecompleted__isnull=False)
    writer = csv.writer(response)
    writer.writerow(['Title', 'memo', 'Created', 'Datecompleted','Createdby','isImportant'])
    for row in todos:
        writer.writerow([row.title,row.memo,row.created,row.datecompleted,row.user.username,row.important,])
    return response

@login_required
def exportexcelcompledatatodo(request):
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename="{}{}.xls"'.format(request.user.username,"_completedWork")
    wb = xlwt.Workbook(encoding='utf-8')
    ws = wb.add_sheet('CompletedWork')

    # Sheet header, first row
    row_num = 0

    font_style = xlwt.XFStyle()
    font_style.font.bold = True

    columns=['Title', 'memo', 'isImportant']
    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], font_style)
    # Sheet body, remaining rows
    font_style = xlwt.XFStyle()
    todos = Todo.objects.filter(user=request.user,datecompleted__isnull=False).values_list('title','memo','important')
    for row in todos:
        row_num += 1
        for col_num in range(len(row)):
            ws.write(row_num, col_num, row[col_num], font_style)

    wb.save(response)
    return response






@login_required
def myprofiletodo(request):
    user = request.user
    if request.method == 'GET':
        try:
            myprofiles=get_list_or_404(MyProfile,user=request.user)
            try:
                leadprofiles=get_list_or_404(MyProfile,lead__isnull=False,user=request.user)
            except:
                leadprofiles=[]
            try:
                associateprofiles=get_list_or_404(MyProfile,associate__isnull=False,user=request.user)
            except:
                associateprofiles=[]
        except:
            leadprofiles=[]
            associateprofiles=[]
            myprofiles=[]
        form =  MyProfileForm()
        return  render(request,'todo/myprofiletodo.html',{'myprofiles':myprofiles,'leadprofiles':leadprofiles,'associateprofiles':associateprofiles,'form':form})
    else:
        lead=get_object_or_404(User,pk=request.POST['user'])
        try:
            try:
                get_list_or_404(MyProfile,user=request.user,username=request.user.username,lead=lead.username)
                error="Selected User is already your lead!!"
                notduplicateuser=False
            except:
                notduplicateuser=True
            try:
                #get_list_or_404(MyProfile,user=lead,username=lead.username,associate=request.user.username)
                get_list_or_404(MyProfile,user=request.user,username=request.user.username,associate=lead.username)
                error="Selected user is your associate!!"
                notduplicateuser=False
            except:
                logger.error('do nothing')
            if request.user == lead:
                error="You can't add yourself as a lead!!"
                notduplicateuser=False

            if  not (notduplicateuser):
                form=MyProfileForm(request.POST)
                try:
                    myprofiles=get_list_or_404(MyProfile,user=request.user)
                    try:
                        leadprofiles=get_list_or_404(MyProfile,lead__isnull=False,user=request.user)
                    except:
                        leadprofiles=[]
                    try:
                        associateprofiles=get_list_or_404(MyProfile,associate__isnull=False,user=request.user)
                    except:
                        associateprofiles=[]
                except:
                    myprofiles =[]
                    leadprofiles=[]
                    associateprofiles=[]
                return render(request,'todo/myprofiletodo.html',{'myprofiles':myprofiles,'leadprofiles':leadprofiles,'associateprofiles':associateprofiles,'form':form,'error':error})
            form=MyProfileForm(request.POST)
            form2=MyProfileForm(request.POST)
            newtodo = form.save(commit=False)
            newtodo.user = user
            newtodo.username=user.username
            newtodo.lead=lead.username
            newtodo.save()

            newtodo2 = form2.save(commit=False)
            newtodo2.user = lead
            newtodo2.username=lead.username
            newtodo2.associate=request.user.username
            newtodo2.save()
            try:
                myprofiles=get_list_or_404(MyProfile,user=request.user)
                try:
                    leadprofiles=get_list_or_404(MyProfile,lead__isnull=False,user=request.user)
                except:
                    leadprofiles=[]
                try:
                    associateprofiles=get_list_or_404(MyProfile,associate__isnull=False,user=request.user)
                except:
                    associateprofiles=[]
            except:
                myprofiles =[]
                associateprofiles=[]
                leadprofiles=[]
            return  render(request,'todo/myprofiletodo.html',{'myprofiles':myprofiles,'leadprofiles':leadprofiles,'associateprofiles':associateprofiles,'form':form,'success':"User added successfuly"})
        except ValueError:
            return render(request,'todo/myprofiletodo.html',{'myprofiles':myprofiles,'leadprofiles':leadprofiles,'associateprofiles':associateprofiles,'form':form,'error':"Bad info passed.Please try again."})


@login_required
def removeassociatetodo(request):
    user = request.user
    if request.method == 'GET':
        try:
            myprofiles=get_list_or_404(MyProfile,user=request.user)
            try:
                leadprofiles=get_list_or_404(MyProfile,lead__isnull=False,user=request.user)
            except:
                leadprofiles=[]
            try:
                associateprofiles=get_list_or_404(MyProfile,associate__isnull=False,user=request.user)
            except:
                associateprofiles=[]
        except:
            leadprofiles=[]
            associateprofiles=[]
            myprofiles=[]
        form =  MyProfileForm()
        return  render(request,'todo/myprofiletodo.html',{'myprofiles':myprofiles,'leadprofiles':leadprofiles,'associateprofiles':associateprofiles,'form':form})
    else:
        try:
            associate=get_object_or_404(User,pk=request.POST['user'])
            myprofiles =get_list_or_404(MyProfile,user=request.user,associate=associate.username)
            try:
                form =  MyProfileForm()
                associatedelete=[]
                #associatedelete=get_object_or_404(MyProfile,associate=associate.username,username=request.user.username,user=request.user)
                associatedelete=get_list_or_404(MyProfile,user=request.user,associate=associate.username,username=request.user.username)
                associateleaddelete=get_list_or_404(MyProfile,user=associate,lead=request.user.username,username=associate.username)
                associatedelete[0].delete()
                associateleaddelete[0].delete()
                try:
                    myprofiles=get_list_or_404(MyProfile,user=request.user)
                    try:
                        leadprofiles=get_list_or_404(MyProfile,lead__isnull=False,user=request.user)
                    except:
                        leadprofiles=[]
                    try:
                        associateprofiles=get_list_or_404(MyProfile,associate__isnull=False,user=request.user)
                    except:
                        associateprofiles=[]
                except:
                    myprofiles =[]
                    leadprofiles=[]
                    associateprofiles=[]

                return  render(request,'todo/myprofiletodo.html',{'myprofiles':myprofiles,'leadprofiles':leadprofiles,'associateprofiles':associateprofiles,'form':form,'success':"Associate deleted successfuly"})
            except:
                try:
                    myprofiles=get_list_or_404(MyProfile,user=request.user)
                    try:
                        leadprofiles=get_list_or_404(MyProfile,lead__isnull=False,user=request.user)
                    except:
                        leadprofiles=[]
                    try:
                        associateprofiles=get_list_or_404(MyProfile,associate__isnull=False,user=request.user)
                    except:
                        associateprofiles=[]
                except:
                    myprofiles =[]
                    associateprofiles=[]
                    leadprofiles=[]
                return  render(request,'todo/myprofiletodo.html',{'myprofiles':myprofiles,'leadprofiles':leadprofiles,'associateprofiles':associateprofiles,'form':form,'error':"Some error occoured during delettion !"})
        except:
            try:
                myprofiles=get_list_or_404(MyProfile,user=request.user)
                try:
                    leadprofiles=get_list_or_404(MyProfile,lead__isnull=False,user=request.user)
                except:
                    leadprofiles=[]
                try:
                    associateprofiles=get_list_or_404(MyProfile,associate__isnull=False,user=request.user)
                except:
                    associateprofiles=[]
            except:
                myprofiles =[]
                leadprofiles=[]
                associateprofiles=[]
            form =  MyProfileForm()
            return render(request,'todo/myprofiletodo.html',{'myprofiles':myprofiles,'leadprofiles':leadprofiles,'associateprofiles':associateprofiles,'form':form,'error':"Selected user is not your associate!!"})

@login_required
def exportassociatedatatodo(request):
    user = request.user
    if request.method == 'GET':
        try:
            myprofiles=get_list_or_404(MyProfile,user=request.user)
            try:
                leadprofiles=get_list_or_404(MyProfile,lead__isnull=False,user=request.user)
            except:
                leadprofiles=[]
            try:
                associateprofiles=get_list_or_404(MyProfile,associate__isnull=False,user=request.user)
            except:
                associateprofiles=[]
        except:
            leadprofiles=[]
            associateprofiles=[]
            myprofiles=[]
        form =  MyProfileForm()
        return  render(request,'todo/myprofiletodo.html',{'myprofiles':myprofiles,'leadprofiles':leadprofiles,'associateprofiles':associateprofiles,'form':form})
    else:
        try:
            associate=get_object_or_404(User,pk=request.POST['user'])
            myprofiles =get_list_or_404(MyProfile,user=request.user)
            try:
                form =  MyProfileForm()
                associatedelete=[]
                associatedeletes=get_list_or_404(MyProfile,user=request.user,associate=associate.username,username=request.user.username)
                associatedelete=associatedeletes[0]
                response = HttpResponse(content_type='text/csv')
                response['Content-Disposition'] = 'attachment; filename="{}{}.csv"'.format(associatedelete.user.username,"_completedWork")
                todos = Todo.objects.filter(user=associatedelete.user)
                writer = csv.writer(response)
                writer.writerow(['Title', 'memo', 'Created', 'Datecompleted','Createdby','isImportant'])
                for row in todos:
                    writer.writerow([row.title,row.memo,row.created,row.datecompleted,row.user.username,row.important,])
                return response
            except:
                try:
                    myprofiles =myprofiles=get_list_or_404(MyProfile,user=request.user)
                    try:
                        leadprofiles=get_list_or_404(MyProfile,lead__isnull=False,user=request.user)
                    except:
                        leadprofiles=[]
                    try:
                        associateprofiles=get_list_or_404(MyProfile,associate__isnull=False,user=request.user)
                    except:
                        associateprofiles=[]
                except:
                    myprofiles =[]
                return  render(request,'todo/myprofiletodo.html',{'myprofiles':myprofiles,'leadprofiles':leadprofiles,'associateprofiles':associateprofiles,'form':form,'error':"Selected user is not your associate !"})
        except:
            myprofiles =[]
            form =  MyProfileForm()
            return render(request,'todo/myprofiletodo.html',{'myprofiles':myprofiles,'form':form,'error':"Bad info passed or no user mapped .Please try again."})








@login_required
def completetodo(request,todo_pk):
    todo=get_object_or_404(Todo,pk=todo_pk,user=request.user)
    if request.method == 'POST':
        todo.datecompleted = timezone.now()
        todo.save()
        return redirect(currenttodos)

@login_required
def deletetodo(request,todo_pk):
    todo=get_object_or_404(Todo,pk=todo_pk,user=request.user)
    if request.method == 'POST':
        todo.datecompleted = timezone.now()
        todo.delete()
        return redirect(currenttodos)

@login_required
def logoutuser(request):
    if request.method == 'POST':
        logout(request)
        return render(request,'todo/logout.html')
    else:
        return render(request,'todo/signupuser.html',{'form':UserCreationForm()})


def loginuser(request):
    if request.method == 'GET':
        return render(request,'todo/loginuser.html',{'form':AuthenticationForm()})
    else:
        #authenticate function
        user=authenticate(request,username=request.POST['username'],password=request.POST['password'])
        if user is None:
            return render(request,'todo/loginuser.html',{'form':AuthenticationForm(),'error':"Username and Password do not match"})
        else:
            login(request,user)
            return redirect(mybiodatahometodo)



def home(request):
    return render(request,'todo/home.html')




def sendmailtodo(request):
    if request.method == 'GET':
        form = SendMultiMailForm()
        return render(request,'todo/sendmailtodo.html',{'form':form})
    else:
        error=None
        msg = MIMEMultipart()
        if bool(request.POST['pass']!='') & bool(request.POST['from'] != ''):
            passw=request.POST['pass']
            msg['From']=request.POST['from']
        else:
            msg['From']='kushwahasamajshadi@gmail.com'
            passw="Ksamaj@#123"
        msg['Subject']=request.POST['subject']
        body=request.POST['body']
        msg.attach(MIMEText(body, 'plain'))
        tolist=list(request.POST['to'].split(','))
        for to in tolist:
            logger.error(to)
            msg['To'] = to
            message = msg.as_string()
            s = smtplib.SMTP('smtp.gmail.com', 587)
            s.starttls()
            try:
                s.login(msg['From'], passw)
            except smtplib.SMTPAuthenticationError:
                return render(request,'todo/sendmailtodo.html',{'error':'Email and password not accepted,Please enter correct details!'})
            try:
                s.sendmail(msg['From'], msg['To'], message)
                msgdict={'sender':msg['From'],'receivers':msg['To'],'subject':msg['Subject'],'body':body}
                form=SendMultiMailForm(data=msgdict)
                form.save()
                logger.error('till not error')
                if form.is_valid():
                    logger.error('saved in db')
                    form.save()
            except smtplib.SMTPRecipientsRefused:
                return render(request,'todo/sendmailtodo.html',{'error':'Receiver mail field is empty!'})
            logger.error("email sent")
            s.quit()
            # open the file to be sent
            # filename = "File_name_with_extension"
            # attachment = open("Path of the file", "rb")
            #
            # # instance of MIMEBase and named as p
            # p = MIMEBase('application', 'octet-stream')
            #
            # # To change the payload into encoded form
            # p.set_payload((attachment).read())
            #
            # # encode into base64
            # encoders.encode_base64(p)
            #
            # p.add_header('Content-Disposition', "attachment; filename= %s" % filename)
            #
            # # attach the instance 'p' to instance 'msg'
            # msg.attach(p)
        return render(request,'todo/sendmailtodo.html',{'success':'success','error':error})



def abouttodo(request):
    logger.error(request.method)
    return render(request,'todo/abouttodo.html')
def portfoliotodo(request):
    return render(request,'todo/portfoliotodo.html')
def contacttodo(request):

    if request.method == 'GET':
        return render(request,'todo/contacttodo.html',{'form':ContactForm()})
    else:
        try:
            form=ContactForm(request.POST)
            form.save()
            todos = Contact.objects.latest('id')
            return render(request,'todo/contacttodo.html',{'form':ContactForm(),'contact':todos})
        except ValueError:
            return render(request,'todo/contacttodo.html',{'form':ContactForm(),'error':"Bad data Passed! Try again."})

    return render(request,'todo/contacttodo.html')

def contacttodos(request):
    #todos=Todo.objects.all()
    #we want user specific database objects
    todos = Contact.objects.latest('id')
    return render(request,'todo/contacttodo.html',{'form':ContactForm(),'contact':todos})


@login_required
def createbiodatatodo(request):
    if request.method == 'GET':
        return render(request,'todo/createbiodatatodo.html',{'form':MyBiodataForm()})
    else:
        form=MyBiodataForm(request.POST, request.FILES)
        newtodo = form.save(commit=False)
        newtodo.user = request.user
        newtodo.username = request.user.username
        try:

            if form.is_valid():
                newtodo.save()
                todos = MyBiodata.objects.filter(user=request.user,deletedrow=False).order_by('-id')
                logger.error(todos[0].id)
                privacymodel=BiodataPrivacy()
                privacymodel.user=request.user
                privacymodel.username=request.user.username
                privacymodel.biodataid=todos[0].id
                privacymodel.save()
                return render(request,'todo/mybiodatatodos.html',{'todos':todos,'msg':'BIODATA Created Successfully.'})
            else:
                return render(request,'todo/createbiodatatodo.html',{'form':MyBiodataForm(),'error':"Bad data Passed!Please Try again."})
        except ValueError:
            return render(request,'todo/createtodo.html',{'form':MyBiodataForm(),'error':"Bad data Passed! Try again."})

@login_required
def mybiodatatodo(request):
    todos = MyBiodata.objects.filter(user=request.user,deletedrow=False).order_by('-id')
    return render(request,'todo/mybiodatatodos.html',{'todos':todos})
@login_required
def viewmybiodatatodo(request,todo_pk):
    todo=get_object_or_404(MyBiodata,pk=todo_pk,user=request.user,deletedrow=False)
    if request.method == 'GET':
        form =  MyBiodataForm(instance=todo)
        return render(request,'todo/viewmybiodatatodo.html',{'todo':todo,'form':form})
    else:
        try:
            form=MyBiodataForm(request.POST,instance=todo)
            form.save()
            todos = MyBiodata.objects.filter(user=request.user).order_by('-id')
            return render(request,'todo/mybiodatatodos.html',{'todos':todos,'msg':'BIODATA updated Successfully.'})
        except ValueError:
            return render(request,'todo/viewmybiodatatodo.html',{'todo':todo,'form':form,'error':"Bad info passed.Please try again."})
@login_required
def mybiodatahometodo(request):
    user_list = MyBiodata.objects.filter(deletedrow=False).order_by('-id')
    page = request.GET.get('page', 1)
    paginator = Paginator(user_list, 3)
    try:
        todos = paginator.page(page)
    except PageNotAnInteger:
        todos = paginator.page(1)
    except EmptyPage:
        todos = paginator.page(paginator.num_pages)
    return render(request,'todo/mybiodatahometodo.html',{'todos':todos})

@login_required
def mybiodatadeletetodo(request,todo_pk):
    todo=get_object_or_404(MyBiodata,pk=todo_pk,user=request.user,deletedrow=False)
    if request.method == 'GET':
        form =  MyBiodataForm(instance=todo)
        return render(request,'todo/viewmybiodatatodo.html',{'todo':todo,'form':form})
    else:
        try:
            todo.deletedrow=True
            todo.last_updated_at=datetime.datetime.now()
            todo.save()
            todos = MyBiodata.objects.filter(user=request.user,deletedrow=False).order_by('-id')
            return render(request,'todo/mybiodatatodos.html',{'todos':todos,'msg':'Biodata deleted Successfully.'})
        except ValueError:
            return render(request,'todo/viewmybiodatatodo.html',{'todo':todo,'form':form,'error':"Bad info passed.Please try again."})

@login_required
def mybiodataprivacytodo(request):
    if request.method == 'GET':
        return render(request,'todo/mybiodataprivacytodo.html',{'form':BiodataPrivacyForm()})
    else:
        try:
            todo=get_object_or_404(BiodataPrivacy,biodataid=request.POST['biodataid'],user=request.user)
            todo.contact_visibility=request.POST['contact_visibility']
            todo.email_visibility=request.POST['email_visibility']
            todo.education_detail_visibility=request.POST['education_detail_visibility']
            todo.address_detail_visibility=request.POST['address_detail_visibility']
            todo.hide_profile=request.POST['hide_profile']
            todo.save()
            todo1=get_object_or_404(MyBiodata,pk=request.POST['biodataid'],user=request.user)
            todo1.contact_visibility=request.POST['contact_visibility']
            todo1.email_visibility=request.POST['email_visibility']
            todo1.education_detail_visibility=request.POST['education_detail_visibility']
            todo1.address_detail_visibility=request.POST['address_detail_visibility']
            todo1.hide_profile=request.POST['hide_profile']
            todo1.save()
            return render(request,'todo/mybiodataprivacytodo.html',{'form':BiodataPrivacyForm(),'msg':'Privacy updated Successfully.'})
        except :
            return render(request,'todo/mybiodataprivacytodo.html',{'form':BiodataPrivacyForm(),'error':"Incorrect biodataID ! Please try again."})

@login_required
def mybiodatadownloadtodo(request):
    if request.method == 'GET':
        return render(request,'todo/mybiodatadownloadtodo.html',{'msg':'PLEASE ENTER YOUR BIODATA ID'})
    else:
        try:
            todo=get_object_or_404(MyBiodata,pk=request.POST['biodataid'],user=request.user,deletedrow=False)
            logger.error(todo.id)
            return render(request,'todo/mybiodatadownloadtodo.html',{'todo':todo,'found':'found'})
        except :
            return render(request,'todo/mybiodatadownloadtodo.html',{'error':"It's not your biodata ID, Please try again."})


@login_required
def viewcontacttodo(request):
    try:
        requestto=get_object_or_404(MyBiodata,pk=request.POST['biodataid'],deletedrow=False)
        if request.POST['requesttype'] == 'contact':
            todos=get_list_or_404(RequestsForApproval,user=request.user,contact_view_request='yes',requesttobiodataid=requestto.id)
            result="CONTACT NUMBER: {}".format(requestto.contact_number)
        else:
            todos=get_list_or_404(RequestsForApproval,user=request.user,connect_request='yes',requesttobiodataid=requestto.id)
            result="YOU ARE ALREADY CONNECTED TO: {}".format(requestto.user.username)
        return JsonResponse({'msg':result})
    except:
        try:
            if request.POST['requesttype'] == 'contact':
                todo1=get_list_or_404(RequestsForApproval,user=request.user,requesttobiodataid=requestto.id,request_type='contact')
                result="YOU HAVE ALREADY RAISED REQUEST TO : {} ,PLEASE WAIT FOR APPROVAL ".format(requestto.user.username)
            else:
                todo1=get_list_or_404(RequestsForApproval,user=request.user,requesttobiodataid=requestto.id,request_type='connect')
                result="YOU HAVE ALREADY RAISED REQUEST TO : {} ,PLEASE WAIT FOR APPROVAL ".format(requestto.user.username)
            return JsonResponse({'msg':result})
        except:
            logger.error('raise new view req')
        try:
            try:
                requesfrom=get_list_or_404(MyBiodata,user=request.user,deletedrow=False)
                requefrombiodataid=requesfrom[0].id
            except:
                requesfrom=[]
                requefrombiodataid=''
            requestmodel=RequestsForApproval()
            requestmodel.user=request.user
            requestmodel.requestfromusername=request.user.username
            requestmodel.userbiodataid=requefrombiodataid
            requestmodel.requesttousername=requestto.user.username
            requestmodel.requesttoemailid=requestto.email_ID
            requestmodel.requesttobiodataid=requestto.id
            if request.POST['requesttype'] == 'contact':
                requestmodel.request_type='contact'
            else:
                requestmodel.request_type='connect'
            requestmodel.save()
            msg = MIMEMultipart()
            msg['From'] = 'kushwahasamajshadi@gmail.com'
            msg['To'] = requestto.email_ID
            logger.error(requestto.email_ID)
            if request.POST['requesttype'] == 'contact':
                msg['Subject'] = " VIEW CONTACT REQUEST"
                body = " {} : WANTS TO VIEW YOUR CONTACT NUMBER ON KUSHWAHA SAMAJ SHADI WEBSITE,KINDLY CHECK YOUR NOTIFICATIONS AND SHARE DETAILS IF INTERESTED ".format(request.user.username)
            else:
                msg['Subject'] = " CONNECT REQUEST"
                body = " {} : WANTS TO   CONTECT YOU ON KUSHWAHA SAMAJ SHADI WEBSITE,KINDLY CHECK YOUR NOTIFICATIONS AND ACCEPT REQUEST IF INTERESTED ".format(request.user.username)
            msg.attach(MIMEText(body, 'plain'))
            try:
                s = smtplib.SMTP('smtp.gmail.com', 587)
                s.starttls()
                s.login(msg['From'], "Ksamaj@#123")
                text = msg.as_string()
                s.sendmail(msg['From'], msg['To'], text)
                s.quit()
            except:
                result='YOUR VIEW CONTACT REQUEST RAISED  '
            logger.error('not error ttls')
            result='YOUR VIEW CONTACT REQUEST RAISED AND HAVE SENT MAIL TO USER '
        except:
            result='SORRY,SELECTED BIODATA USER HAS NOT UPLOADED EMAIL ID'
        return JsonResponse({'msg':result})



@login_required
def biodatachatstodo(request):
    if request.method == 'GET':
        try:
            logger.error('before inbox')
            inbox=get_list_or_404(MyBiodataInbox,user=request.user)
            logger.error('after inbox')
        except:
            inbox=[]
        try:
            chats=get_list_or_404(MyBiodataChatbox,user=request.user)
        except:
            chats=[]
        try:
            requser=get_list_or_404(MyBiodata,user=request.user)
            logger.error(requser[0].email_ID)
            reqapproval=get_list_or_404(RequestsForApproval,requesttoemailid=requser[0].email_ID)
        except:
            reqapproval=[]
        return render(request,'todo/biodatachatstodo.html',{'inbox':inbox,'chats':chats,'reqapproval':reqapproval})
    else:
        if request.method == 'POST':
            if request.POST['sentboxview'] == 'sentboxview':
                logger.error(' sentbox request')
                try:
                    outbox =get_list_or_404(MyBiodataChatbox,user=request.user)
                except:
                    outbox=[]
                mydict={}
                for row in outbox:
                    localdict={}
                    for row1 in mydict:
                        localdict['msgtousername']=row.msgtousername
                        localdict['subject']=row.subject
                        localdict['msg']=row.msg
                    mydict[row.msgtousername]=localdict
                return JsonResponse({'result':'success','msgs':mydict})

            elif request.POST['sentboxview'] == 'pendingrequests':
                logger.error('Peding requests')
                try:
                    requser=get_list_or_404(MyBiodata,user=request.user)
                    logger.error(requser[0].email_ID)
                    reqapproval=get_list_or_404(RequestsForApproval,requesttoemailid=requser[0].email_ID)
                except:
                    reqapproval=[]
                mydict={}
                for row in reqapproval:
                    localdict={}
                    localdict['request_from']=row.user.username
                    localdict['contact_view_request']=row.contact_view_request
                    localdict['connect_request']=row.connect_request
                    localdict['request_type']=row.request_type
                    localdict['biodataid']=row.userbiodataid
                    localdict['rowid']=row.id
                    mydict[row.id]=localdict
                logger.error(mydict)
                return JsonResponse({'result':'success','msgs':mydict})
            elif request.POST['sentboxview'] == 'getmychatusers':
                try:
                    myusers=get_list_or_404(RequestsForApproval,user=request.user,request_type='connect',connect_request='yes')
                except:
                    myusers=[]
                mydict={}
                for row in myusers:
                    localdict={}
                    localdict['request_from']=row.user.username
                    localdict['requesttousername']=row.requesttousername
                    localdict['requesttobiodataid']=row.requesttobiodataid
                    localdict['requesttoemailid']=row.requesttoemailid
                    localdict['biodataid']=row.userbiodataid
                    localdict['rowid']=row.id
                    mydict[row.requesttousername]=localdict
                logger.error(mydict)
                return JsonResponse({'result':'success','msgs':mydict})
            elif request.POST['sentboxview'] == 'sendmymsg':
                try:
                    myusers=get_list_or_404(RequestsForApproval,user=request.user,request_type='connect',connect_request='yes',requesttobiodataid=request.POST['tobiodataid'])
                    touser = get_object_or_404(MyBiodata,pk=request.POST['tobiodataid'])
                    sentbox=MyBiodataChatbox()
                    sentbox.user=request.user
                    sentbox.msgtousername=touser.user.username
                    sentbox.msg=request.POST['msg']
                    sentbox.save()
                    toinbox=MyBiodataInbox()
                    toinbox.user=touser.user
                    toinbox.mybiodataid=touser.id
                    toinbox.msgfromusername=request.user.username
                    toinbox.msg=request.POST['msg']
                    toinbox.save()
                    return JsonResponse({'result':'MESSAGE HAS BEEN SENT SUCCESSFULLY.'})

                except:
                    return JsonResponse({'result':'SORRY,YOU ARE NOT AUTHORIZED TO SEND MESSAGE TO SELECTED USER'})

                return JsonResponse({'result':'success'})
            elif request.POST['sentboxview'] == 'approvereq':
                logger.error('app requests')
                try:
                    reqapproval=get_object_or_404(RequestsForApproval,pk=request.POST['rowid'])
                    logger.error(request.POST['reqtype'])
                    if request.POST['reqtype'] == 1:
                        reqapproval.contact_view_request='yes'
                    else:
                        reqapproval.connect_request='yes'
                    reqapproval.save()
                    return JsonResponse({'result':'REQUEST APPROVED SUCCESSFULLY'})
                except:
                    return JsonResponse({'result':'BAD DATA PASSED, PLEASE TRY AGAIN!'})
            elif request.POST['sentboxview'] == 'rejectreq':
                logger.error('rej requests')
                try:
                    reqapproval=get_object_or_404(RequestsForApproval,pk=request.POST['rowid'])
                    if request.POST['reqtype'] == 1:
                        reqapproval.contact_view_request='no'
                    else:
                        reqapproval.connect_request='no'
                    reqapproval.save()
                    return JsonResponse({'result':'REQUEST REJECTED FOR NOW!'})
                except:
                    return JsonResponse({'result':'BAD DATA PASSED, PLEASE TRY AGAIN!'})
            elif request.POST['sentboxview'] == 'deletereq':
                logger.error('del requests')
                try:
                    reqapproval=get_object_or_404(RequestsForApproval,pk=request.POST['rowid'])
                    reqapproval.delete()
                    return JsonResponse({'result':'REQUEST DELETED SUCCESSFULLY'})
                except:
                    return JsonResponse({'result':'BAD DATA PASSED, PLEASE TRY AGAIN!'})
            elif request.POST['sentboxview'] == 'unblockreq':
                logger.error('unblock requests')
                try:
                    reqapproval=get_list_or_404(RequestsForApproval,requesttobiodataid=request.POST['biodataid'],requesttousername=request.user.username,requestfromusername=request.POST['msgfromusername'])
                    for row in reqapproval:
                        row.connect_request='yes'
                        row.save()
                    return JsonResponse({'result':'USER HAS BEEN UNBLOCKED'})
                except:
                    return JsonResponse({'result':'BAD DATA PASSED, PLEASE TRY AGAIN!'})
            elif request.POST['sentboxview'] == 'blockreq':
                try:
                    reqapproval=get_list_or_404(RequestsForApproval,requesttobiodataid=request.POST['biodataid'],requesttousername=request.user.username,requestfromusername=request.POST['msgfromusername'])
                    for row in reqapproval:
                        row.connect_request='no'
                        row.save()
                    return JsonResponse({'result':'USER HAS BEEN BLOCKED SUCCESSFULLY'})
                except:
                    return JsonResponse({'result':'BAD DATA PASSED, PLEASE TRY AGAIN!'})
            elif request.POST['sentboxview'] == 'userspecific':
                logger.error('sentbox user specific request')
                try:
                    inbox=get_list_or_404(MyBiodataChatbox,user=request.user,msgtousername=request.POST['msgfromusername'])
                except:
                    inbox=[]
                mydict={}
                for row in inbox:
                    localdict={}
                    localdict['msg']=row.msg
                    localdict['msgfromusername']=row.msgtousername
                    mydict[row.id]=localdict
                logger.error(mydict)
                return JsonResponse({'result':request.POST['msgfromusername'],'msgs':mydict})

            try:
                logger.error('inbox request')
                inbox=get_list_or_404(MyBiodataInbox,user=request.user,msgfromusername=request.POST['msgfromusername'])
            except:
                inbox=[]
            mydict={}
            for row in inbox:
                localdict={}
                localdict['msg']=row.msg
                localdict['msgfromusername']=row.msgfromusername
                mydict[row.id]=localdict
            logger.error(mydict)
            return JsonResponse({'result':request.POST['msgfromusername'],'msgs':mydict})
        try:
            todo=get_object_or_404(MyBiodata,pk=request.POST['biodataid'],user=request.user,deletedrow=False)
            logger.error(todo.id)
            return render(request,'todo/mybiodatadownloadtodo.html',{'todo':todo,'found':'found'})
        except :
            return render(request,'todo/mybiodatadownloadtodo.html',{'error':"It's not your biodata ID, Please try again."})


def biodatahelptodo(request):

    if request.method == 'GET':
        return render(request,'todo/biodatahelptodo.html',{'form':BiodataHelpForm()})
    else:
        try:
            form=BiodataHelpForm(request.POST)
            form.save()
            try:
                msg = MIMEMultipart()
                msg['From'] = 'kushwahasamajshadi@gmail.com'
                msg['To'] = 'rohitkushwah9527@gmail.com'
                msg['Subject'] = request.POST['subject']
                body = "{} & contact number {} & emailid {}".format(request.POST['query'],request.POST['contact_number'],request.POST['email_id'])
                msg.attach(MIMEText(body, 'plain'))
                s = smtplib.SMTP('smtp.gmail.com', 587)
                s.starttls()
                s.login(msg['From'], "Ksamaj@#123")
                text = msg.as_string()
                s.sendmail(msg['From'], msg['To'], text)
                s.quit()

                msg = MIMEMultipart()
                msg['From'] = 'kushwahasamajshadi@gmail.com'
                msg['To'] = request.POST['email_id']
                msg['Subject'] = request.POST['subject']
                body = "You send us this query {}  .We will help you on priority Thanks".format(request.POST['query'])
                msg.attach(MIMEText(body, 'plain'))
                s = smtplib.SMTP('smtp.gmail.com', 587)
                s.starttls()
                s.login(msg['From'], "Ksamaj@#123")
                text = msg.as_string()
                s.sendmail(msg['From'], msg['To'], text)
                s.quit()
            except:
                logger.error('error occured in biodata help')



            todos = BiodataHelp.objects.latest('id')
            return render(request,'todo/biodatahelptodo.html',{'form':BiodataHelpForm(),'contact':todos})
        except ValueError:
            return render(request,'todo/biodatahelptodo.html',{'form':BiodataHelpForm(),'error':"Bad data Passed! Try again."})

    return render(request,'todo/biodatahelptodo.html')

@login_required
def createtodo(request):
    if request.method == 'GET':
        return render(request,'todo/createtodo.html',{'form':TodoForm()})
    else:
        try:
            form=TodoForm(request.POST)
            newtodo = form.save(commit=False)
            newtodo.user = request.user
            newtodo.save()
            return redirect(currenttodos)
        except ValueError:
            return render(request,'todo/createtodo.html',{'form':TodoForm(),'error':"Bad data Passed! Try again."})


def translatortodo(request):
    translator = Translator()
    available_langugages=googletrans.LANGUAGES
    if request.method == 'POST':
        return render(request,'todo/translatortodo.html',{'available_langugages':available_langugages})
    else:
        return render(request,'todo/translatortodo.html',{'available_langugages':available_langugages})


@csrf_protect
def translatetodo(request):
    fromlangval = request.POST['fromlangval']
    tolangval = request.POST['tolangval']
    lefttext = request.POST['lefttext']
    righttext = request.POST['righttext']
    resulttype = request.POST['resulttype']
    translator = Translator()
    #result = translator.translate(lefttext,src='en',dest=tolangval)
    langsrc = fromlangval
    langdetected = translator.detect(lefttext)
    if(langdetected.lang != fromlangval):
        langsrc=langdetected.lang
    result = translator.translate(lefttext, src=langsrc, dest=tolangval)

    if(resulttype == 'pronunciation'):
        return JsonResponse({'result':result.pronunciation,'langdetected':langdetected.lang})
    else:
        return JsonResponse({'result':result.text,'langdetected':langdetected.lang})

def passwordgeneratortodo(request):
    thestring=""
    Characters=list('abcdefghijklmnopqrstuvwxyz')
    if request.GET.get("uppercase"):
        Characters.extend(list('ABCDEFGHIJKLMNOPQRSTUVWXYZ'))
    if request.GET.get("special"):
        Characters.extend(list('!@#$%^&*()_+'))
    if request.GET.get("number"):
        Characters.extend(list('1234567890'))

    length=int(request.GET.get("length",8))
    for x in range(length):
        thestring += random.choice(Characters)

    return render(request,'todo/passwordgeneratortodo.html',{"password":thestring})
