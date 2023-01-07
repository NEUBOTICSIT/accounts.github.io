from ast import Pass
from asyncio.windows_events import NULL
from email.message import EmailMessage
from django.shortcuts import render,redirect
from ..models import Organisation,User,Role,Company_book,Module_Type,Create_Category,Create_Tax
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


def settings(request,user_id,org_id,company_id):
    #all company ,pass to the header organisation href tag 
    all_company_book=Company_book.objects.filter(user_id=user_id,first_company=True,enable=True,deleted_at='').values() 
    #pass corresponding_organisation comapanybook  to top header dropdown 
    company_book=Company_book.objects.filter(user_id=user_id,organisation_id=org_id, enable=True,deleted_at='').values()   
    #pass selected organisation 
    selected_organisation=Organisation.objects.get(id=org_id,user_id=user_id)
    #pass selected company
    selected_company=Company_book.objects.get(id=company_id,user_id=user_id,organisation_id=org_id)
    context={'company_book':company_book,'selected_organisation':selected_organisation,'user_id':user_id,'org_id':org_id,'company_id':company_id,
             'selected_company':selected_company,'all_company_book':all_company_book}

    return render(request,'Accounting_Software_App/settings.html',context)



def categories(request,user_id,org_id,company_id):
    #all company ,pass to the header organisation href tag 
    all_company_book=Company_book.objects.filter(user_id=user_id,first_company=True,enable=True,deleted_at='').values() 
    #pass corresponding_organisation comapanybook  to top header dropdown 
    company_book=Company_book.objects.filter(user_id=user_id,organisation_id=org_id, enable=True,deleted_at='').values()   
    #pass selected organisation 
    selected_organisation=Organisation.objects.get(id=org_id,user_id=user_id)
    #pass selected company
    selected_company=Company_book.objects.get(id=company_id,user_id=user_id,organisation_id=org_id)
    #pass all categories to table
    all_categories=Create_Category.objects.filter(deleted_at='').values()
    context={'company_book':company_book,'selected_organisation':selected_organisation,'user_id':user_id,'org_id':org_id,'company_id':company_id,
             'selected_company':selected_company,'all_company_book':all_company_book,'all_categories':all_categories}

    return render(request,'Accounting_Software_App/categories.html',context)




def create_categories(request,user_id,org_id,company_id):
    if request.method=='POST':
        name=request.POST['name']
        module_type_id=request.POST['module_type']
        module_type=Module_Type.objects.get(id=module_type_id)
        color=request.POST['color']
        enable=(request.POST.get('enable'))
        
        if ((name=='') and  (module_type=='') ):
            messages.error(request,"all fields are mandatory")
            return redirect('Accounting_Software_App:create_categories',user_id,org_id,company_id)
         
        user_organisation=Create_Category.objects.create(name=name,module_type=module_type,color=color,enable=enable)
        user_organisation.save()
        messages.success(request," Category Created successfully ")
     
        #pass corresponding_organisation comapanybook  to top header dropdown 
        company_book=Company_book.objects.filter(user_id=user_id,organisation_id=org_id, enable=True).values()   
        #pass selected organisation 
        selected_organisation=Organisation.objects.get(id=org_id,user_id=user_id)
        #all company ,pass to the header organisation href tag 
        all_company_book=Company_book.objects.filter(user_id=user_id,first_company=True,enable=True).values() 
        #pass selected company
        selected_company=Company_book.objects.get(id=company_id,user_id=user_id,organisation_id=org_id)
        #pass module type to dropdown
        all_module_type=Module_Type.objects.all().values()
        context={'company_book':company_book,'selected_organisation':selected_organisation,'user_id':user_id,'org_id':org_id,
                 'company_id':company_id,'selected_company':selected_company,'all_company_book':all_company_book,'all_module_type':all_module_type}
        
        return render(request,'Accounting_Software_App/create_categories.html',context)
    
    #pass corresponding_organisation comapanybook  to top header dropdown 
    company_book=Company_book.objects.filter(user_id=user_id,organisation_id=org_id, enable=True).values()   
    #pass selected organisation 
    selected_organisation=Organisation.objects.get(id=org_id,user_id=user_id)
    #all company ,pass to the header organisation href tag 
    all_company_book=Company_book.objects.filter(user_id=user_id,first_company=True,enable=True).values() 
    #pass selected company
    selected_company=Company_book.objects.get(id=company_id,user_id=user_id,organisation_id=org_id)
    #pass module type to dropdown
    all_module_type=Module_Type.objects.all().values()
    context={'company_book':company_book,'selected_organisation':selected_organisation,'user_id':user_id,'org_id':org_id,
             'company_id':company_id,'selected_company':selected_company,'all_company_book':all_company_book,'all_module_type':all_module_type}
    
    return render(request,'Accounting_Software_App/create_categories.html',context)




def edit_category(request,user_id,org_id,company_id,edit_category_id):
    if request.method=='POST':
        name=request.POST['name']
        module_type_id=request.POST['module_type']
        module_type=Module_Type.objects.get(id=module_type_id)
        color=request.POST['color']
        enable=(request.POST.get('enable'))
        
        if ((name=='') and  (module_type=='') ):
            messages.error(request,"all fields are mandatory")
            return redirect('Accounting_Software_App:edit_category',user_id,org_id,company_id)
         
        category=Create_Category.objects.filter(pk=edit_category_id).update(name=name,module_type=module_type,color=color,enable=enable,updated_at=datetime.today()) 
        # category.save()
        messages.success(request," Category Updated successfully ")
     
        #pass corresponding_organisation comapanybook  to top header dropdown 
        company_book=Company_book.objects.filter(user_id=user_id,organisation_id=org_id, enable=True).values()   
        #pass selected organisation 
        selected_organisation=Organisation.objects.get(id=org_id,user_id=user_id)
        #all company ,pass to the header organisation href tag 
        all_company_book=Company_book.objects.filter(user_id=user_id,first_company=True,enable=True).values() 
        #pass selected company
        selected_company=Company_book.objects.get(id=company_id,user_id=user_id,organisation_id=org_id)
        #pass module type to dropdown
        all_module_type=Module_Type.objects.all().values()
        #clicked user information pass to the edit_user_page
        edit_info=Create_Category.objects.get(pk=edit_category_id)
        context={'company_book':company_book,'selected_organisation':selected_organisation,'user_id':user_id,'org_id':org_id,
                 'company_id':company_id,'selected_company':selected_company,'all_company_book':all_company_book,'all_module_type':all_module_type,
                 'edit_info':edit_info}
        
        return render(request,'Accounting_Software_App/edit_category.html',context)
    
    #pass corresponding_organisation comapanybook  to top header dropdown 
    company_book=Company_book.objects.filter(user_id=user_id,organisation_id=org_id, enable=True).values()   
    #pass selected organisation 
    selected_organisation=Organisation.objects.get(id=org_id,user_id=user_id)
    #all company ,pass to the header organisation href tag 
    all_company_book=Company_book.objects.filter(user_id=user_id,first_company=True,enable=True).values() 
    #pass selected company
    selected_company=Company_book.objects.get(id=company_id,user_id=user_id,organisation_id=org_id)
    #pass module type to dropdown
    all_module_type=Module_Type.objects.all().values()
    #clicked user information pass to the edit_user_page
    edit_info=Create_Category.objects.get(pk=edit_category_id)
    context={'company_book':company_book,'selected_organisation':selected_organisation,'user_id':user_id,'org_id':org_id,
             'company_id':company_id,'selected_company':selected_company,'all_company_book':all_company_book,'all_module_type':all_module_type,
             'edit_info':edit_info}
    
    return render(request,'Accounting_Software_App/edit_category.html',context)



#this function will delete user
def delete_category(request,user_id,org_id,company_id,delete_category_id):
    if request.method=="POST":
        Create_Category.objects.filter(pk=delete_category_id).update(deleted_at=datetime.today())  
        
        messages.success(request,"Deleted successfully.")
        return redirect('Accounting_Software_App:categories',user_id,org_id,company_id)














def taxes(request,user_id,org_id,company_id):
    #all company ,pass to the header organisation href tag 
    all_company_book=Company_book.objects.filter(user_id=user_id,first_company=True,enable=True,deleted_at='').values() 
    #pass corresponding_organisation comapanybook  to top header dropdown 
    company_book=Company_book.objects.filter(user_id=user_id,organisation_id=org_id, enable=True,deleted_at='').values()   
    #pass selected organisation 
    selected_organisation=Organisation.objects.get(id=org_id,user_id=user_id)
    #pass selected company
    selected_company=Company_book.objects.get(id=company_id,user_id=user_id,organisation_id=org_id)
    #pass all categories to table
    all_taxes=Create_Tax.objects.filter(deleted_at='').values()
    context={'company_book':company_book,'selected_organisation':selected_organisation,'user_id':user_id,'org_id':org_id,'company_id':company_id,
             'selected_company':selected_company,'all_company_book':all_company_book,'all_taxes':all_taxes}

    return render(request,'Accounting_Software_App/taxes.html',context)




def create_tax(request,user_id,org_id,company_id):
    if request.method=='POST':
        name=request.POST['name']
        rate=request.POST['rate']
        type=request.POST['type']
        enable=(request.POST.get('enable'))
        
        if ((name=='') and  (rate=='') and (type=='')):
            messages.error(request,"all fields are mandatory")
            return redirect('Accounting_Software_App:edit_',user_id,org_id,company_id)
         
        create_tax=Create_Tax.objects.create(name=name,rate=rate,type=type,enable=enable)
        create_tax.save()
        messages.success(request," Taxes Created successfully ")
     
        #pass corresponding_organisation comapanybook  to top header dropdown 
        company_book=Company_book.objects.filter(user_id=user_id,organisation_id=org_id, enable=True).values()   
        #pass selected organisation 
        selected_organisation=Organisation.objects.get(id=org_id,user_id=user_id)
        #all company ,pass to the header organisation href tag 
        all_company_book=Company_book.objects.filter(user_id=user_id,first_company=True,enable=True).values() 
        #pass selected company
        selected_company=Company_book.objects.get(id=company_id,user_id=user_id,organisation_id=org_id)
        context={'company_book':company_book,'selected_organisation':selected_organisation,'user_id':user_id,'org_id':org_id,
                 'company_id':company_id,'selected_company':selected_company,'all_company_book':all_company_book}
        
        return render(request,'Accounting_Software_App/create_tax.html',context)
    
    #pass corresponding_organisation comapanybook  to top header dropdown 
    company_book=Company_book.objects.filter(user_id=user_id,organisation_id=org_id, enable=True).values()   
    #pass selected organisation 
    selected_organisation=Organisation.objects.get(id=org_id,user_id=user_id)
    #all company ,pass to the header organisation href tag 
    all_company_book=Company_book.objects.filter(user_id=user_id,first_company=True,enable=True).values() 
    #pass selected company
    selected_company=Company_book.objects.get(id=company_id,user_id=user_id,organisation_id=org_id)
    context={'company_book':company_book,'selected_organisation':selected_organisation,'user_id':user_id,'org_id':org_id,
             'company_id':company_id,'selected_company':selected_company,'all_company_book':all_company_book}
    
    return render(request,'Accounting_Software_App/create_tax.html',context)




def edit_tax(request,user_id,org_id,company_id,edit_tax_id):
    if request.method=='POST':
        name=request.POST['name']
        rate=request.POST['rate']
        type=request.POST['type']
        enable=(request.POST.get('enable'))
        
        if ((name=='') and  (rate=='') and (type=='')):
            messages.error(request,"all fields are mandatory")
            return redirect('Accounting_Software_App:edit_',user_id,org_id,company_id)
         
        update_tax=Create_Tax.objects.filter(pk=edit_tax_id).update(name=name,rate=rate,type=type,enable=enable,updated_at=datetime.today()) 
        messages.success(request," Tax Updated successfully ")
     
        #pass corresponding_organisation comapanybook  to top header dropdown 
        company_book=Company_book.objects.filter(user_id=user_id,organisation_id=org_id, enable=True).values()   
        #pass selected organisation 
        selected_organisation=Organisation.objects.get(id=org_id,user_id=user_id)
        #all company ,pass to the header organisation href tag 
        all_company_book=Company_book.objects.filter(user_id=user_id,first_company=True,enable=True).values() 
        #pass selected company
        selected_company=Company_book.objects.get(id=company_id,user_id=user_id,organisation_id=org_id)
        #pass module type to dropdown
        all_module_type=Module_Type.objects.all().values()
        #clicked user information pass to the edit_user_page
        edit_info=Create_Tax.objects.get(pk=edit_tax_id)
        context={'company_book':company_book,'selected_organisation':selected_organisation,'user_id':user_id,'org_id':org_id,
                 'company_id':company_id,'selected_company':selected_company,'all_company_book':all_company_book,'all_module_type':all_module_type,
                 'edit_info':edit_info}
        
        return render(request,'Accounting_Software_App/edit_tax.html',context)
    
    #pass corresponding_organisation comapanybook  to top header dropdown 
    company_book=Company_book.objects.filter(user_id=user_id,organisation_id=org_id, enable=True).values()   
    #pass selected organisation 
    selected_organisation=Organisation.objects.get(id=org_id,user_id=user_id)
    #all company ,pass to the header organisation href tag 
    all_company_book=Company_book.objects.filter(user_id=user_id,first_company=True,enable=True).values() 
    #pass selected company
    selected_company=Company_book.objects.get(id=company_id,user_id=user_id,organisation_id=org_id)
    #pass module type to dropdown
    all_module_type=Module_Type.objects.all().values()
    #clicked user information pass to the edit_user_page
    edit_info=Create_Tax.objects.get(pk=edit_tax_id)
    context={'company_book':company_book,'selected_organisation':selected_organisation,'user_id':user_id,'org_id':org_id,
             'company_id':company_id,'selected_company':selected_company,'all_company_book':all_company_book,'all_module_type':all_module_type,
             'edit_info':edit_info}
    
    return render(request,'Accounting_Software_App/edit_tax.html',context)



#this function will delete user
def delete_tax(request,user_id,org_id,company_id,delete_tax_id):
    if request.method=="POST":
        Create_Tax.objects.filter(pk=delete_tax_id).update(deleted_at=datetime.today())  
        
        messages.success(request,"Deleted successfully.")
        return redirect('Accounting_Software_App:taxes',user_id,org_id,company_id)
