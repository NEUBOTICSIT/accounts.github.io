from ast import Pass
from asyncio.windows_events import NULL
from email.message import EmailMessage
from django.shortcuts import render,redirect
from ..models import Organisation,User,Role,Company_book
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
from Accounting_Software_project import settings
from django.core.mail import send_mail
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode,urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.utils.encoding import force_str
from .. tokens import generate_token
from django.core.mail import EmailMessage,send_mail
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from datetime import date, datetime, timedelta
import json
from django.http import HttpResponse
#form password encrypt
from django.contrib.auth.hashers import make_password




@login_required(login_url='Accounting_Software_App:signin')    
def index(request,user_id,org_id,company_id):   
    # #pass all loggedin user organisation name to dropdown 
    # organisation_list=Organisation.objects.filter(user_id=request.user.id, enable=True).values() 
    #all company ,pass to the header organisation href tag 
    all_company_book=Company_book.objects.filter(user_id=user_id,first_company=True,enable=True,deleted_at='').values() 
    #pass corresponding_organisation comapanybook  to top header dropdown 
    company_book=Company_book.objects.filter(user_id=user_id,organisation_id=org_id, enable=True,deleted_at='').values() 
    count_company_book=len(company_book) 
    #pass selected organisation 
    selected_organisation=Organisation.objects.get(id=org_id,user_id=user_id)
    #pass selected company
    selected_company=Company_book.objects.get(id=company_id,user_id=user_id,organisation_id=org_id,deleted_at='')
    #users_count pass to the user page
    users= User.objects.filter(~Q(is_staff=True),created_by=user_id,organisation_name=org_id,deleted_at='')
    users_count=len(users)
    context={'company_book':company_book,'selected_organisation':selected_organisation,'user_id':user_id,'org_id':org_id,'company_id':company_id,'count_company_book':count_company_book,
             'users_count':users_count,'selected_company':selected_company,'all_company_book':all_company_book}
    return render(request,'Accounting_Software_App/index.html',context)



def signup(request):
  #if user is logged in then cn't open signup page
  if request.user.is_authenticated:
        #organisation_id pass to index page as 3rd argument
        org_id= Organisation.objects.get(user_id=request.user.id,first_organisation=True,enable=True) 
        #Company_id pass to index page as 4rth argument
        company_id= Company_book.objects.get(user_id=request.user.id,organisation_id=org_id.id,first_company=True,enable=True,deleted_at='') 
        return redirect('Accounting_Software_App:index',request.user.id,org_id.id,company_id.id)
  else:   
    if request.method=='POST':
        email=request.POST['email']
        psw=request.POST['psw']
        psw_repeat=request.POST['psw_repeat']
        first_name=request.POST['first_name']
        last_name=request.POST['last_name']
        organisation_name=request.POST['company']
        organisation_email=request.POST['organisation_email']
        if ((email=='') and (psw=='') and  (psw_repeat=='') and  (first_name=='') and  (last_name=='') and  (organisation_name=='') and (organisation_email=='')):
            messages.error(request,"all fields are mandatory")
            return redirect('Accounting_Software_App:signup')
        if User.objects.filter(email=email):
            messages.error(request," email already exist")
            return redirect('Accounting_Software_App:signup')  
        if len(first_name)>10:
            messages.error(request," username must be under 10 characters")
            return redirect('Accounting_Software_App:signup')
        if psw!=psw_repeat :
            messages.error(request," passwords did't match!")
            return redirect('Accounting_Software_App:signup')
        if not first_name.isalnum() :
            messages.error(request," First name mustbe alfanumaric!")
            return redirect('Accounting_Software_App:signup')
        if not last_name.isalnum() :
            messages.error(request," Last name mustbe alfanumaric!")
            return redirect('Accounting_Software_App:signup')
          
        user_role=Role.objects.get(pk=2)
        user_role=str(user_role)
        
        user=User.objects.create_user(email,psw,first_name,last_name,user_role,'','','',True)
        user.is_active= False
        user.is_staff=False
         
        user_organisation=Organisation.objects.create(user=user,organisation_name=organisation_name,email=organisation_email,enable=True,first_organisation=True)
        user_organisation.save()
        
        user_company=Company_book.objects.create(user_id =user.id,organisation_id =user_organisation.id,company=organisation_name,email=organisation_email,currency='Rupee',enable=True,first_company=True)
        user_company.save()
        
        user.save()
        messages.success(request," your account has been successfully created. we have sent you a confirmation email, please confirm email in order to activate your account")
        
        # Welcome Email
        subject="Welcome: django login"
        message= "hello"+user.first_name + "!! \n "+"thankyou for visiting our website \n we have sent you a confirmation email, please confirm your email address in order to  activate your account. \n\n  Thanking you \n admin "
        from_email= settings.EMAIL_HOST_USER
        to_list=[user.email]
        send_mail(subject,message,from_email,to_list,fail_silently=True)
        
        # Email Address confirmation email
        current_site = get_current_site(request)
        email_subject = "confirm your email @admin - django login!"
        message2 = render_to_string('Accounting_Software_App/email_confirmation.html',{
            'name': user.username,
            'domain': current_site.domain,
            'uid': urlsafe_base64_encode(force_bytes(user.pk)), 
            'token': generate_token.make_token(user)
        })      
        email=EmailMessage(
          email_subject,
          message2,
          settings.EMAIL_HOST_USER,
          [user.email]
        )
        email.fail_silently = True
        email.send()  
        return redirect('Accounting_Software_App:signin')       
    return render(request,'Accounting_Software_App/signup.html')


def activate(request,uidb64,token):
      try:
        uid=force_str(urlsafe_base64_decode(uidb64))
        user= User.objects.get(pk=uid)
      except(TypeError,ValueError, OverflowError,User.DoesNotExist):
        user=None
        
      if user is not None and generate_token.check_token(user, token):
        user.is_active= True
        user.is_staff=True
        user.save()
        login(request, user)
        #organisation_id pass to index page as 3rd argument
        org_id= Organisation.objects.get(user_id=user.id,first_organisation=True,enable=True)  
        #Company_id pass to index page as 4rth argument
        company_id= Company_book.objects.get(user_id=request.user.id,organisation_id=org_id.id,first_company=True,enable=True,deleted_at='') 
        return redirect('Accounting_Software_App:index',user.id,org_id.id,company_id.id)
      else:
        return render(request, 'activation_failed.html')





def signin(request):
  
  #if user is logged in then will not open signin page
  if request.user.is_authenticated:
        #organisation_id pass to index page as 3rd argument
        org_id= Organisation.objects.get(user_id=request.user.id,first_organisation=True,enable=True) 
        #Company_id pass to index page as 4rth argument
        company_id= Company_book.objects.get(user_id=request.user.id,organisation_id=org_id.id,first_company=True,enable=True,deleted_at='') 
        #when click on signin button then pass logedin user_id and enable organisation_id to url as below
        return redirect('Accounting_Software_App:index',request.user.id,org_id.id,company_id.id)
  else:

    if request.method=='POST':
          email=request.POST['email']
          psw=request.POST['psw']
          user = authenticate(email=email,password=psw)
     
          if user is not None:
                login(request, user)    
                #organisation_id pass to index page as 3rd argument
                org_id= Organisation.objects.get(user_id=request.user.id,first_organisation=True,enable=True)    
                #Company_id pass to index page as 4rth argument
                company_id= Company_book.objects.get(user_id=request.user.id,organisation_id=org_id.id,first_company=True,enable=True,deleted_at='') 
                #when click on signin button then pass logedin user_id and enable organisation_id to url as below
                return redirect('Accounting_Software_App:index',request.user.id,org_id.id,company_id.id)
          else:
                messages.error(request,'Bad Credentials')
                return redirect('Accounting_Software_App:signin')
      
    return render(request,'Accounting_Software_App/signin.html')




def signout(request ):
    logout(request)
    messages.success(request, "Logged Out Successfully!")
    return redirect('Accounting_Software_App:signin')
  
  
      
   
@login_required(login_url='Accounting_Software_App:signin')    
def profile(request,user_id,org_id,company_id):
    # #pass all loggedin user organisation name to dropdown 
    # organisation_list=Organisation.objects.filter(user_id=request.user.id, enable=True).values()  
    #pass corresponding_organisation comapanybook  to top header dropdown 
    company_book=Company_book.objects.filter(user_id=user_id,organisation_id=org_id, enable=True,deleted_at='').values()   
    #all company ,pass to the header organisation href tag 
    all_company_book=Company_book.objects.filter(user_id=user_id,first_company=True,enable=True,deleted_at='').values() 
    #pass selected company
    selected_company=Company_book.objects.get(id=company_id,user_id=user_id,organisation_id=org_id,deleted_at='')
    #pass selected organisation 
    selected_organisation=Organisation.objects.get(id=org_id,user_id=user_id)
    context={'company_book':company_book,'selected_organisation':selected_organisation,'user_id':user_id,'org_id':org_id,'company_id':company_id,
             'selected_company':selected_company,'all_company_book':all_company_book}

    return render(request,'Accounting_Software_App/profile.html',context)



@login_required(login_url='Accounting_Software_App:signin')    
def users(request,user_id,org_id,company_id):
    #user pass to the users page
    users= User.objects.filter(~Q(is_staff=True),created_by=user_id,organisation_name=org_id,deleted_at='')
    # #pass all loggedin user organisation name to dropdown 
    # organisation_list=Organisation.objects.filter(user_id=request.user.id, enable=True).values()  
    #all company ,pass to the header organisation href tag 
    all_company_book=Company_book.objects.filter(user_id=user_id,first_company=True,enable=True,deleted_at='').values() 
    #pass selected company
    selected_company=Company_book.objects.get(id=company_id,user_id=user_id,organisation_id=org_id,deleted_at='')
    #pass corresponding_organisation comapanybook  to top header dropdown 
    company_book=Company_book.objects.filter(user_id=user_id,organisation_id=org_id, enable=True,deleted_at='').values()   
    #pass selected organisation 
    selected_organisation=Organisation.objects.get(id=org_id,user_id=user_id)
    context={'users':users,'company_book':company_book,'selected_organisation':selected_organisation,'user_id':user_id,'org_id':org_id,'company_id':company_id,
             'all_company_book':all_company_book,'selected_company':selected_company}
      
    return render(request,'Accounting_Software_App/users.html',context)




@login_required(login_url='Accounting_Software_App:signin')    
def create_user(request,user_id,org_id,company_id): 
    if request.method=='POST':
        email=request.POST['email']
        psw=request.POST['psw']
        psw_repeat=request.POST['psw_repeat']
        first_name=request.POST['first_name']
        last_name=request.POST['last_name']
        company=request.POST.getlist('company')
        role= request.POST['role']
        enable=(request.POST.get('enable'))
        created_by=request.user.id
        
        if ((email=='') and (psw=='') and  (psw_repeat=='') and  (first_name=='') and  (last_name=='') and  (company=='') and (role=='')):
            messages.error(request,"all fields are mandatory")
            return redirect('Accounting_Software_App:create_user',user_id,org_id,company_id)
        if User.objects.filter(email=email):
            messages.error(request,"email already exist")
            return redirect('Accounting_Software_App:create_user',user_id,org_id,company_id)  
        if len(first_name)>10:
            messages.error(request,"username must be under 10 characters")
            return redirect('Accounting_Software_App:create_user',user_id,org_id,company_id)
        if psw!=psw_repeat :
            messages.error(request,"passwords did't match!")
            return redirect('Accounting_Software_App:create_user',user_id,org_id,company_id)
        if not first_name.isalnum() :
            messages.error(request,"First name mustbe alfanumaric!")
            return redirect('Accounting_Software_App:create_user',user_id,org_id,company_id)
        if not last_name.isalnum() :
            messages.error(request,"Last name mustbe alfanumaric!")
            return redirect('Accounting_Software_App:create_user',user_id,org_id,company_id)
          
        user=User.objects.create_user(email,psw,first_name,last_name,role,org_id,company,created_by,enable)
        user.is_active= False
        user.save()
        messages.success(request,"your account has been successfully created. we have sent you  a confirmation email, please confirm email in order to activate your account")
        
        # Welcome Email
        subject="Welcome: django login"
        message= "hello"+user.first_name + "!! \n "+"thankyou for visiting our website \n we have sent you a confirmation email, please confirm your email addressin order to  activate your account. \n\n  Thanking you \n admin "
        from_email= settings.EMAIL_HOST_USER
        to_list=[user.email]
        send_mail(subject,message,from_email,to_list,fail_silently=True)
        
        # Email Address confirmation email
        current_site = get_current_site(request)
        email_subject = "confirm your email @admin - django login!"
        message2 = render_to_string('Accounting_Software_App/organisation_user_email_conformation.html',{
            'name': user.username,
            'domain': current_site.domain,
            'uid': urlsafe_base64_encode(force_bytes(user.pk)), 
            'token': generate_token.make_token(user)
        })      
        email=EmailMessage(
          email_subject,
          message2,
          settings.EMAIL_HOST_USER,
          [user.email]
        )
        email.fail_silently = True
        email.send()

        # #pass all loggedin user organisation name to dropdown 
        # organisation_list=Organisation.objects.filter(user_id=request.user.id, enable=True).values()  
        #all company ,pass to the header organisation href tag 
        all_company_book=Company_book.objects.filter(user_id=user_id,first_company=True,enable=True,deleted_at='').values() 
        #pass selected company
        selected_company=Company_book.objects.get(id=company_id,user_id=user_id,organisation_id=org_id,deleted_at='')
        #pass corresponding_organisation comapanybook  to top header dropdown 
        company_book=Company_book.objects.filter(user_id=user_id,organisation_id=org_id, enable=True,deleted_at='').values()   
        #pass selected organisation 
        selected_organisation=Organisation.objects.get(id=org_id,user_id=user_id)
        context={'users':users,'company_book':company_book,'selected_organisation':selected_organisation,'user_id':user_id,'org_id':org_id,'company_id':company_id,
                 'all_company_book':all_company_book,'selected_company':selected_company}
        return render(request,'Accounting_Software_App/create_user.html',context)
    else:
        # #pass all loggedin user organisation name to dropdown 
        # organisation_list=Organisation.objects.filter(user_id=request.user.id, enable=True).values()  
        #all company ,pass to the header organisation href tag 
        all_company_book=Company_book.objects.filter(user_id=user_id,first_company=True,enable=True,deleted_at='').values() 
        #pass selected company
        selected_company=Company_book.objects.get(id=company_id,user_id=user_id,organisation_id=org_id,deleted_at='')
        #pass corresponding_organisation comapanybook  to top header dropdown 
        company_book=Company_book.objects.filter(user_id=user_id,organisation_id=org_id, enable=True,deleted_at='').values()   
        #pass selected organisation 
        selected_organisation=Organisation.objects.get(id=org_id,user_id=user_id)
        context={'users':users,'company_book':company_book,'selected_organisation':selected_organisation,'user_id':user_id,'org_id':org_id,'company_id':company_id,
                 'all_company_book':all_company_book,'selected_company':selected_company}

        return render(request,'Accounting_Software_App/create_user.html',context)



def organisation_user_activate(request,uidb64,token):
      try:
        uid=force_str(urlsafe_base64_decode(uidb64))
        user= User.objects.get(pk=uid)
      except(TypeError,ValueError, OverflowError,User.DoesNotExist):
        user=None
        
      if user is not None and generate_token.check_token(user, token):
        user.is_active= True
        user.save()
        login(request, user)
        return redirect('Accounting_Software_App:index')
      else:
        return render(request, 'activation_failed.html')


#this function will edit user
@login_required(login_url='Accounting_Software_App:signin')    
def edit_user(request,user_id,org_id,company_id,edit_user_id):
    if request.method=="POST":             
            email=request.POST['email']
            psw=request.POST['psw']
            psw_repeat=request.POST['psw_repeat']
            first_name=request.POST['first_name']
            last_name=request.POST['last_name']
            company=request.POST.getlist('company')
            role= request.POST['role']
            enable=(request.POST.get('enable'))
            if ((email=='') and (psw=='') and  (first_name=='') and  (last_name=='') and (role=='')):
                messages.error(request,"all fields are mandatory")
                return render(request,'Accounting_Software_App/edit_user.html',context)
            elif len(first_name)>10:
                messages.error(request,"username must be under 10 characters")
                return render(request,'Accounting_Software_App/edit_user.html',context)
            elif not first_name.isalnum() :
                messages.error(request,"First name mustbe alfanumaric!")
                return render(request,'Accounting_Software_App/edit_user.html',context)
            elif not last_name.isalnum() :
                messages.error(request,"Last name mustbe alfanumaric!")
                return render(request,'Accounting_Software_App/edit_user.html',context)
            elif psw!=psw_repeat :
                messages.error(request,"passwords did't match!")
                return render(request,'Accounting_Software_App/edit_user.html',context)
            else:
                User.objects.filter(pk=edit_user_id).update(email=email,password=make_password(psw),first_name=first_name,last_name=last_name,role=role,company_name=company,enable=enable,updated_at=datetime.today())
                messages.success(request,"your account has been updated successfully.")
                
                # #pass all loggedin user organisation name to dropdown 
                # organisation_list=Organisation.objects.filter(user_id=request.user.id, enable=True).values()  
                #all company ,pass to the header organisation href tag 
                all_company_book=Company_book.objects.filter(user_id=user_id,first_company=True,enable=True,deleted_at='').values() 
                #pass selected company
                selected_company=Company_book.objects.get(id=company_id,user_id=user_id,organisation_id=org_id,deleted_at='')
                #pass corresponding_organisation comapanybook  to top header dropdown 
                company_book=Company_book.objects.filter(user_id=user_id,organisation_id=org_id, enable=True,deleted_at='').values()  
                #pass selected organisation 
                selected_organisation=Organisation.objects.get(id=org_id,user_id=user_id)
                #clicked user information pass to the edit_user_page
                edit_info=User.objects.get(pk=edit_user_id)
                #for get distict value from selected_company list and all company list,(render to edit_user page company dropdown)
                #selected_company list
                user_selected_company=edit_info.company_name
                #non selected company list
                all_org_company=Company_book.objects.filter(user_id=user_id,organisation_id=org_id, enable=True,deleted_at  ='').values_list('company')   
                all_company_list=list(all_org_company)
                company_list = [item for i in all_company_list for item in i]
                #distinct list from above two list
                distinct_list =list(set(user_selected_company) ^ set(company_list))            
            
                # noselected_companybook=Company_book.objects.filter(user_id=user_id,organisation_id=org_id, enable=True).values() 
                context={'users':users,'company_book':company_book,'selected_organisation':selected_organisation,'user_id':user_id,'org_id':org_id,'edit_info':edit_info
                         ,'company_id':company_id,'all_company_book':all_company_book,'selected_company':selected_company,'distinct_list':distinct_list,'edit_user_id':edit_user_id}
                return render(request,'Accounting_Software_App/edit_user.html',context)
    else:
            # #pass all loggedin user organisation name to dropdown 
            # organisation_list=Organisation.objects.filter(user_id=request.user.id, enable=True).values()  
            #company pass to the header organisation href tag 
            all_company_book=Company_book.objects.filter(user_id=user_id,first_company=True,enable=True,deleted_at='').values() 
            #pass selected company to button
            selected_company=Company_book.objects.get(id=company_id,user_id=user_id,organisation_id=org_id,deleted_at='')
            #pass corresponding_organisation comapanybook  to top header dropdown 
            company_book=Company_book.objects.filter(user_id=user_id,organisation_id=org_id, enable=True,deleted_at='').values()   
            #pass selected organisation 
            selected_organisation=Organisation.objects.get(id=org_id,user_id=user_id)
            #clicked user information pass to the edit_user_page
            edit_info=User.objects.get(pk=edit_user_id)
            
            #for get distict value from selected_company list and all company list,(render to edit_user page company dropdown)
            #selected_company list
            user_selected_company=edit_info.company_name
            print(user_selected_company)
            #non selected company list
            all_org_company=Company_book.objects.filter(user_id=user_id,organisation_id=org_id, enable=True,deleted_at='').values_list('company')   
            all_company_list=list(all_org_company)
            company_list = [item for i in all_company_list for item in i]
            print(company_list)
            #distinct list from above two list
            distinct_list =list(set(user_selected_company) ^ set(company_list))            
            print(distinct_list)
            
            context={'users':users,'company_book':company_book,'selected_organisation':selected_organisation,'user_id':user_id,'org_id':org_id,'edit_info':edit_info
                     ,'company_id':company_id,'all_company_book':all_company_book,'selected_company':selected_company,'distinct_list':distinct_list,'edit_user_id':edit_user_id}
            return render(request,'Accounting_Software_App/edit_user.html',context)



#this function will delete user
def delete_user(request,user_id,org_id,company_id,delete_user_id):
    if request.method=="POST":
        # pi=User.objects.get(pk=delete_user_id)
        # pi.delete()
        User.objects.filter(pk=delete_user_id).update(deleted_at=datetime.today())  
        
        messages.success(request,"Deleted successfully.")
        return redirect('Accounting_Software_App:users',user_id,org_id,company_id)



@login_required(login_url='Accounting_Software_App:signin')    
def manage_company(request,user_id,org_id,company_id): 
    
    #all company ,pass to the header organisation href tag 
    all_company_book=Company_book.objects.filter(user_id=user_id,first_company=True,enable=True,deleted_at='').values() 
    #pass corresponding_organisation comapanybook  to top header dropdown 
    company_book=Company_book.objects.filter(user_id=user_id,organisation_id=org_id,enable=True,deleted_at='').values()   
    #pass selected organisation 
    selected_organisation=Organisation.objects.get(id=org_id,user_id=user_id)
    #pass selected company
    selected_company=Company_book.objects.get(id=company_id,user_id=user_id,organisation_id=org_id,deleted_at='')
    #pass corresponding_organisation comapanybook  to manage_company page
    manage_company_book=Company_book.objects.filter(~Q(first_company=True),~Q(id=company_id),user_id=user_id,organisation_id=org_id,deleted_at='').values()   
    #default company pass to the table 1st row(can not delete).
    default_company_book=Company_book.objects.get(user_id=user_id,organisation_id=org_id,first_company=True,enable=True,deleted_at='')
    
    context={'company_book':company_book,'selected_organisation':selected_organisation,'user_id':user_id,'org_id':org_id,'company_id':company_id,'manage_company_book':manage_company_book,
             'selected_company':selected_company,'all_company_book':all_company_book,'default_company_book':default_company_book}
    return render(request,'Accounting_Software_App/manage_company.html',context)



@login_required(login_url='Accounting_Software_App:signin')    
def create_company_book(request,user_id,org_id,company_id): 
    if request.method=='POST':
        company=request.POST['company']
        email=request.POST['email']
        currency=request.POST['currency']
        tax_num=request.POST['tax_num']
        company_address=request.POST['company_address']
        phone_number=request.POST['phone_number']
        zip_code=request.POST['zip_code']
        city=request.POST['city']
        state=request.POST['state']
        enable=(request.POST.get('enable'))
        user_company=Company_book.objects.create(user_id =user_id,organisation_id =org_id,company=company,email=email,currency=currency,tax_num=tax_num,company_address=company_address,phone_number=phone_number,zip_code=zip_code,
                                                 city=city,state=state,enable=enable)
        user_company.save()
        messages.success(request,"your Company has been created successfully") 
        
        # #pass all loggedin user organisation name to dropdown 
        # organisation_list=Organisation.objects.filter(user_id=request.user.id, enable=True).values()  
        #all company ,pass to the header organisation href tag 
        all_company_book=Company_book.objects.filter(user_id=user_id,first_company=True,enable=True,deleted_at='').values() 
        #pass selected company
        selected_company=Company_book.objects.get(id=company_id,user_id=user_id,organisation_id=org_id,deleted_at='')
        #pass corresponding_organisation comapanybook  to top header dropdown 
        company_book=Company_book.objects.filter(user_id=user_id,organisation_id=org_id, enable=True,deleted_at='').values()   
        #pass selected organisation 
        selected_organisation=Organisation.objects.get(id=org_id,user_id=user_id)
        context={'company_book':company_book,'selected_organisation':selected_organisation,'user_id':user_id,'org_id':org_id,'company_id':company_id,'all_company_book':all_company_book,
                 'selected_company':selected_company}
                
        return render(request,'Accounting_Software_App/create_company_book.html',context)
    
    # #pass all loggedin user organisation name to dropdown 
    # organisation_list=Organisation.objects.filter(user_id=request.user.id, enable=True).values()  
    #pass corresponding_organisation comapanybook  to top header dropdown 
    company_book=Company_book.objects.filter(user_id=user_id,organisation_id=org_id, enable=True,deleted_at='').values()   
    #all company ,pass to the header organisation href tag 
    all_company_book=Company_book.objects.filter(user_id=user_id,first_company=True,enable=True,deleted_at='').values() 
    #pass selected company
    selected_company=Company_book.objects.get(id=company_id,user_id=user_id,organisation_id=org_id,deleted_at='')
    #pass selected organisation 
    selected_organisation=Organisation.objects.get(id=org_id,user_id=user_id)
    context={'company_book':company_book,'selected_organisation':selected_organisation,'user_id':user_id,'org_id':org_id,'company_id':company_id,'all_company_book':all_company_book,
            'selected_company':selected_company}
    return render(request,'Accounting_Software_App/create_company_book.html' ,context)


#this function will edit user
@login_required(login_url='Accounting_Software_App:signin')    
def edit_company(request,user_id,org_id,company_id,edit_company_id):
        if request.method=='POST':
            company=request.POST['company']
            email=request.POST['email']
            currency=request.POST['currency']
            tax_num=request.POST['tax_num']
            company_address=request.POST['company_address']
            phone_number=request.POST['phone_number']
            zip_code=request.POST['zip_code']
            city=request.POST['city']
            state=request.POST['state']
            enable=(request.POST.get('enable'))
            Company_book.objects.filter(pk=edit_company_id).update(company=company,email=email,currency=currency,tax_num=tax_num,company_address=company_address,phone_number=phone_number,zip_code=zip_code,
                                                 city=city,state=state,enable=enable,updated_at=datetime.today())
            messages.success(request,"your account has been updated successfully.")
            
            #pass all loggedin user organisation name to dropdown 
            # organisation_list=Organisation.objects.filter(user_id=request.user.id, enable=True).values()  
            #pass corresponding_organisation comapanybook  to top header dropdown 
            company_book=Company_book.objects.filter(user_id=user_id,organisation_id=org_id, enable=True,deleted_at='').values()   
            #all company ,pass to the header organisation href tag 
            all_company_book=Company_book.objects.filter(user_id=user_id,first_company=True,enable=True,deleted_at='').values() 
            #pass selected company
            selected_company=Company_book.objects.get(id=company_id,user_id=user_id,organisation_id=org_id,deleted_at='')
            #pass selected organisation 
            selected_organisation=Organisation.objects.get(id=org_id,user_id=user_id)
            #clicked user information pass to the edit_user_page
            edit_info=Company_book.objects.get(pk=edit_company_id)
            context={'users':users,'company_book':company_book,'selected_organisation':selected_organisation,'user_id':user_id,'org_id':org_id,'company_id':company_id,'edit_info':edit_info,
                     'all_company_book':all_company_book,'selected_company':selected_company}
            return render(request,'Accounting_Software_App/edit_company.html',context)
        else:
            #  #pass all loggedin user organisation name to dropdown 
            # organisation_list=Organisation.objects.filter(user_id=request.user.id, enable=True).values()  
            #pass corresponding_organisation comapanybook  to top header dropdown 
            company_book=Company_book.objects.filter(user_id=user_id,organisation_id=org_id, enable=True,deleted_at='').values()   
            #all company ,pass to the header organisation href tag 
            all_company_book=Company_book.objects.filter(user_id=user_id,first_company=True,enable=True,deleted_at='').values() 
            #pass selected company
            selected_company=Company_book.objects.get(id=company_id,user_id=user_id,organisation_id=org_id,deleted_at='')
            #pass selected organisation 
            selected_organisation=Organisation.objects.get(id=org_id,user_id=user_id)
            #clicked user information pass to the edit_user_page
            edit_info=Company_book.objects.get(pk=edit_company_id)
            context={'users':users,'company_book':company_book,'selected_organisation':selected_organisation,'user_id':user_id,'org_id':org_id,'company_id':company_id,'edit_info':edit_info,
                     'all_company_book':all_company_book,'selected_company':selected_company}

            return render(request,'Accounting_Software_App/edit_company.html',context)


#this function will delete company
def delete_company(request,user_id,org_id,company_id,delete_company_id):
   if request.method=="POST":
    #pi=Company_book.objects.get(pk=delete_company_id)
    # pi.delete()
    Company_book.objects.filter(pk=delete_company_id).update(deleted_at=datetime.today())  
    #default company id (when deleted selected_company then page redirect to default company page)
    default_company_book=Company_book.objects.get(user_id=user_id,organisation_id=org_id,first_company=True,enable=True,deleted_at='')
    messages.success(request,"Deleted successfully.")
    return redirect('Accounting_Software_App:manage_company',user_id,org_id,default_company_book.id)


@login_required(login_url='Accounting_Software_App:signin')    
def manage_organisation(request,user_id,org_id,company_id): 
    #pass all loggedin user organisation name table 
    organisation_list=Organisation.objects.filter(~Q(id=org_id),~Q(first_organisation=True),user_id=user_id, enable=True).values() 
    #all company ,pass to the header organisation href tag 
    all_company_book=Company_book.objects.filter(user_id=user_id,first_company=True,enable=True,deleted_at='').values() 
    #pass corresponding_organisation comapanybook  to top header dropdown 
    company_book=Company_book.objects.filter(user_id=user_id,organisation_id=org_id, enable=True,deleted_at='').values()   
    #pass selected organisation 
    selected_organisation=Organisation.objects.get(id=org_id,user_id=user_id)
    #pass selected company
    selected_company=Company_book.objects.get(id=company_id,user_id=user_id,organisation_id=org_id)
    #default organisation(can't delete)
    default_organisation=Organisation.objects.get(user_id=user_id,first_organisation=True, enable=True) 
    context={'organisation_list':organisation_list,'company_book':company_book,'selected_organisation':selected_organisation,'user_id':user_id,'org_id':org_id,'company_id':company_id,
             'selected_company':selected_company,'all_company_book':all_company_book,'default_organisation':default_organisation}
    return render(request,'Accounting_Software_App/manage_organisation.html',context)



@login_required(login_url='Accounting_Software_App:signin')    
def create_organisation(request,user_id,org_id,company_id): 
    if request.method=='POST':
        email=request.POST['email']
        organisation=request.POST['organisation']
        enable=(request.POST.get('enable'))
        if ((email=='') and  (organisation=='')):
            messages.error(request,"all fields are mandatory")
            return redirect('Accounting_Software_App:create_organisation',user_id,org_id,company_id)
        if Organisation.objects.filter(email=email):
            messages.error(request,"email already exist")
            return redirect('Accounting_Software_App:create_organisation',user_id,org_id,company_id)
          
        user_organisation=Organisation.objects.create(user=request.user,email=email,organisation_name=organisation,enable=enable)
        
        user_company=Company_book.objects.create(user_id=user_id,organisation_id=user_organisation.id,company=organisation,email=email,currency='Rupee',enable=True,first_company=True)
        user_company.save()
        
        user_organisation.save()      
        messages.success(request," Organisation Registered successfully ")
     
        # #pass all loggedin user organisation name to dropdown 
        # organisation_list=Organisation.objects.filter(user_id=request.user.id, enable=True).values()  
        #pass corresponding_organisation comapanybook  to top header dropdown 
        company_book=Company_book.objects.filter(user_id=user_id,organisation_id=org_id, enable=True).values()   
        #pass selected organisation 
        selected_organisation=Organisation.objects.get(id=org_id,user_id=user_id)
        #all company ,pass to the header organisation href tag 
        all_company_book=Company_book.objects.filter(user_id=user_id,first_company=True,enable=True).values() 
        #pass selected company
        selected_company=Company_book.objects.get(id=company_id,user_id=user_id,organisation_id=org_id)
        
        context={'users':users,'company_book':company_book,'selected_organisation':selected_organisation,'user_id':user_id,'org_id':org_id,
                 'company_id':company_id,'selected_company':selected_company,'all_company_book':all_company_book}
        
        return render(request,'Accounting_Software_App/create_organisation.html',context)
    
    # #pass all loggedin user organisation name to dropdown 
    # organisation_list=Organisation.objects.filter(user_id=request.user.id, enable=True).values()  
    #pass corresponding_organisation comapanybook  to top header dropdown 
    company_book=Company_book.objects.filter(user_id=user_id,organisation_id=org_id, enable=True).values()   
    #pass selected organisation 
    selected_organisation=Organisation.objects.get(id=org_id,user_id=user_id)
    #all company ,pass to the header organisation href tag 
    all_company_book=Company_book.objects.filter(user_id=user_id,first_company=True,enable=True).values() 
    #pass selected company
    selected_company=Company_book.objects.get(id=company_id,user_id=user_id,organisation_id=org_id)
    context={'users':users,'company_book':company_book,'selected_organisation':selected_organisation,'user_id':user_id,'org_id':org_id,
             'company_id':company_id,'selected_company':selected_company,'all_company_book':all_company_book}
    
    return render(request,'Accounting_Software_App/create_organisation.html',context)





@login_required(login_url='Accounting_Software_App:signin')    
def edit_organisation(request,user_id,org_id,company_id,edit_organisation_id):
        if request.method=='POST':
            email=request.POST['email']
            organisation=request.POST['organisation']
            enable=(request.POST.get('enable'))
            Organisation.objects.filter(pk=edit_organisation_id).update(email=email,organisation_name=organisation,enable=enable,updated_at=datetime.today())
            messages.success(request,"your Organisation updated successfully.")
            
            #pass corresponding_organisation comapanybook  to top header dropdown 
            company_book=Company_book.objects.filter(user_id=user_id,organisation_id=org_id, enable=True,deleted_at='').values()   
            #pass selected organisation 
            selected_organisation=Organisation.objects.get(id=org_id,user_id=user_id)
            #all company ,pass to the header organisation href tag 
            all_company_book=Company_book.objects.filter(user_id=user_id,first_company=True,enable=True,deleted_at='').values() 
            #pass selected company
            selected_company=Company_book.objects.get(id=company_id,user_id=user_id,organisation_id=org_id,deleted_at='')
            #clicked user information pass to the edit_user_page
            edit_info=Organisation.objects.get(pk=edit_organisation_id)
            context={'users':users,'company_book':company_book,'selected_organisation':selected_organisation,'user_id':user_id,'org_id':org_id,'company_id':company_id,
                     'edit_info':edit_info,'all_company_book':all_company_book,'selected_company':selected_company}
            return render(request,'Accounting_Software_App/edit_organisation.html',context)
        else:
            #pass corresponding_organisation comapanybook  to top header dropdown 
            company_book=Company_book.objects.filter(user_id=user_id,organisation_id=org_id, enable=True,deleted_at='').values()   
            #pass selected organisation 
            selected_organisation=Organisation.objects.get(id=org_id,user_id=user_id)
            #all company ,pass to the header organisation href tag 
            all_company_book=Company_book.objects.filter(user_id=user_id,first_company=True,enable=True,deleted_at='').values() 
            #pass selected company
            selected_company=Company_book.objects.get(id=company_id,user_id=user_id,organisation_id=org_id,deleted_at='')
            #clicked user information pass to the edit_user_page
            edit_info=Organisation.objects.get(pk=edit_organisation_id)
            context={'users':users,'company_book':company_book,'selected_organisation':selected_organisation,'user_id':user_id,'org_id':org_id,'company_id':company_id,
                     'edit_info':edit_info,'all_company_book':all_company_book,'selected_company':selected_company}

            return render(request,'Accounting_Software_App/edit_organisation.html',context)


