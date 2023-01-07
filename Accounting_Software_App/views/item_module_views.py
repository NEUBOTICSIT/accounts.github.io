from ast import Pass
from asyncio.windows_events import NULL
from email.message import EmailMessage
from django.shortcuts import render,redirect
from ..models import Organisation,Company_book,Items,Create_Tax,Create_Category,Module_Type
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
from django.http import JsonResponse



def items(request,user_id,org_id,company_id):
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
    #all created item pass to the table
    all_items=Items.objects.filter(deleted_at='')
    context={'company_book':company_book,'selected_organisation':selected_organisation,'user_id':user_id,'org_id':org_id,'company_id':company_id,
             'selected_company':selected_company,'all_company_book':all_company_book,'default_organisation':default_organisation,'all_items':all_items}

    return render(request,'Accounting_Software_App/items.html',context)
    
    
def create_item(request,user_id,org_id,company_id):
    if request.method=='POST':
        name=request.POST['item_name']
        tax=request.POST['tax']
        description=request.POST['description']
        sale_price=request.POST['sale_price']
        purchase_price=request.POST['purchase_price']
        category=request.POST['category']
        # picture=request.FILES['picture']
        picture=request.FILES.get('picture')
        enable=(request.POST.get('enable'))
        user_company=Items.objects.create(user_id =user_id,organisation_id =org_id,company_id=company_id,name=name,tax=tax,description=description,sale_price=sale_price,purchase_price=purchase_price,
                                                 category=category,picture=picture,enable=enable)
        user_company.save()
        messages.success(request,"your Item has been created successfully") 
        
        #all company ,pass to the header organisation href tag 
        all_company_book=Company_book.objects.filter(user_id=user_id,first_company=True,enable=True,deleted_at='').values() 
        #pass selected company
        selected_company=Company_book.objects.get(id=company_id,user_id=user_id,organisation_id=org_id,deleted_at='')
        #pass corresponding_organisation comapanybook  to top header dropdown 
        company_book=Company_book.objects.filter(user_id=user_id,organisation_id=org_id, enable=True,deleted_at='').values()   
        #pass selected organisation 
        selected_organisation=Organisation.objects.get(id=org_id,user_id=user_id)
        #all tax list pass to the tax dropdown
        all_taxes=Create_Tax.objects.filter(enable=True,deleted_at='')
        #all item category pass to the category dropdown
        all_item_category=Create_Category.objects.filter(module_type_id=3,enable=True,deleted_at='')
        context={'company_book':company_book,'selected_organisation':selected_organisation,'user_id':user_id,'org_id':org_id,'company_id':company_id,'all_company_book':all_company_book,
                 'selected_company':selected_company,'all_taxes':all_taxes,'all_item_category':all_item_category}
                
        return render(request,'Accounting_Software_App/create_item.html',context)
    
    #pass corresponding_organisation comapanybook  to top header dropdown 
    company_book=Company_book.objects.filter(user_id=user_id,organisation_id=org_id, enable=True,deleted_at='').values()   
    #all company ,pass to the header organisation href tag 
    all_company_book=Company_book.objects.filter(user_id=user_id,first_company=True,enable=True,deleted_at='').values() 
    #pass selected company
    selected_company=Company_book.objects.get(id=company_id,user_id=user_id,organisation_id=org_id,deleted_at='')
    #pass selected organisation 
    selected_organisation=Organisation.objects.get(id=org_id,user_id=user_id)
    #all tax list pass to the tax dropdown
    all_taxes=Create_Tax.objects.filter(enable=True,deleted_at='')
    #all item category pass to the category dropdown
    all_item_category=Create_Category.objects.filter(module_type_id=3,enable=True,deleted_at='')
    context={'company_book':company_book,'selected_organisation':selected_organisation,'user_id':user_id,'org_id':org_id,'company_id':company_id,'all_company_book':all_company_book,
            'selected_company':selected_company,'all_taxes':all_taxes,'all_item_category':all_item_category}

    return render(request,'Accounting_Software_App/create_item.html',context)




def edit_item(request,user_id,org_id,company_id,edit_item_id):
    if request.method=='POST':
        name=request.POST['name']
        tax=request.POST['tax']
        description=request.POST['description']
        sale_price=request.POST['sale_price']
        purchase_price=request.POST['purchase_price']
        category=request.POST['category']
        picture=request.FILES['picture']
        enable=(request.POST.get('enable'))
        
        if ((name=='') and  (sale_price=='') and  (purchase_price=='')):
            messages.error(request,"all fields are mandatory")
            return redirect('Accounting_Software_App:items',user_id,org_id,company_id)
         
        edit_item=Items.objects.filter(pk=edit_item_id).update(name=name,tax=tax,description=description,sale_price=sale_price,purchase_price=purchase_price,category=category,enable=enable,picture=picture,updated_at=datetime.today()) 
        messages.success(request," Item Updated successfully ")
     
        #all company ,pass to the header organisation href tag 
        all_company_book=Company_book.objects.filter(user_id=user_id,first_company=True,enable=True,deleted_at='').values() 
        #pass selected company
        selected_company=Company_book.objects.get(id=company_id,user_id=user_id,organisation_id=org_id,deleted_at='')
        #pass corresponding_organisation comapanybook  to top header dropdown 
        company_book=Company_book.objects.filter(user_id=user_id,organisation_id=org_id, enable=True,deleted_at='').values()   
        #pass selected organisation 
        selected_organisation=Organisation.objects.get(id=org_id,user_id=user_id)
        #all tax list pass to the tax dropdown
        all_taxes=Create_Tax.objects.filter(enable=True,deleted_at='')
        #all item category pass to the category dropdown
        all_item_category=Create_Category.objects.filter(module_type_id=3,enable=True,deleted_at='')
        context={'company_book':company_book,'selected_organisation':selected_organisation,'user_id':user_id,'org_id':org_id,'company_id':company_id,'all_company_book':all_company_book,
                 'selected_company':selected_company,'all_taxes':all_taxes,'all_item_category':all_item_category}
                
        return render(request,'Accounting_Software_App/create_item.html',context)
    
    #pass corresponding_organisation comapanybook  to top header dropdown 
    company_book=Company_book.objects.filter(user_id=user_id,organisation_id=org_id, enable=True).values()   
    #pass selected organisation 
    selected_organisation=Organisation.objects.get(id=org_id,user_id=user_id)
    #all company ,pass to the header organisation href tag 
    all_company_book=Company_book.objects.filter(user_id=user_id,first_company=True,enable=True).values() 
    #pass selected company
    selected_company=Company_book.objects.get(id=company_id,user_id=user_id,organisation_id=org_id)
    #all tax list pass to the tax dropdown
    all_taxes=Create_Tax.objects.filter(enable=True,deleted_at='')
    #all item category pass to the category dropdown
    all_item_category=Create_Category.objects.filter(module_type_id=3,enable=True,deleted_at='')
    #clicked user information pass to the edit_user_page
    edit_info=Items.objects.get(pk=edit_item_id)
    context={'company_book':company_book,'selected_organisation':selected_organisation,'user_id':user_id,'org_id':org_id,
             'company_id':company_id,'selected_company':selected_company,'all_company_book':all_company_book,'edit_info':edit_info
             ,'all_taxes':all_taxes,'all_item_category':all_item_category}
    
    return render(request,'Accounting_Software_App/edit_item.html',context)



#this function will delete user
def delete_item(request,user_id,org_id,company_id,delete_item_id):
    if request.method=="POST":
        Items.objects.filter(pk=delete_item_id).update(deleted_at=datetime.today())  
        
        messages.success(request,"Deleted successfully.")
        return redirect('Accounting_Software_App:items',user_id,org_id,company_id)


        
                        
def add_new_category(request,user_id,org_id,company_id):
    if request.method=='POST':
        cat_name=request.POST['cat_name']
        color=request.POST['color']
        module_type=Module_Type.objects.get(id=3)
        add_category=Create_Category.objects.create(name=cat_name,module_type=module_type,color=color,enable=True)
        add_category.save()
        messages.success(request," Add New Category successfully ")
     
        #pass corresponding_organisation comapanybook  to top header dropdown 
        company_book=Company_book.objects.filter(user_id=user_id,organisation_id=org_id, enable=True).values()   
        #pass selected organisation 
        selected_organisation=Organisation.objects.get(id=org_id,user_id=user_id)
        #all company ,pass to the header organisation href tag 
        all_company_book=Company_book.objects.filter(user_id=user_id,first_company=True,enable=True).values() 
        #pass selected company
        selected_company=Company_book.objects.get(id=company_id,user_id=user_id,organisation_id=org_id)
        #pass all category to category dropdown
        all_item_category=Create_Category.objects.filter(module_type_id=3,enable=True,deleted_at='')
        #all tax list pass to the tax dropdown
        all_taxes=Create_Tax.objects.filter(enable=True,deleted_at='')
        context={'company_book':company_book,'selected_organisation':selected_organisation,'user_id':user_id,'org_id':org_id,
                 'company_id':company_id,'selected_company':selected_company,'all_company_book':all_company_book,'all_item_category':all_item_category,'all_taxes':all_taxes}
        
        return render(request,'Accounting_Software_App/create_item.html',context)
    #pass corresponding_organisation comapanybook  to top header dropdown 
    company_book=Company_book.objects.filter(user_id=user_id,organisation_id=org_id, enable=True,deleted_at='').values()   
    #all company ,pass to the header organisation href tag 
    all_company_book=Company_book.objects.filter(user_id=user_id,first_company=True,enable=True,deleted_at='').values() 
    #pass selected company
    selected_company=Company_book.objects.get(id=company_id,user_id=user_id,organisation_id=org_id,deleted_at='')
    #pass selected organisation 
    selected_organisation=Organisation.objects.get(id=org_id,user_id=user_id)
    #pass all category to category dropdown
    all_item_category=Create_Category.objects.filter(module_type_id=3,enable=True,deleted_at='')
    #all tax list pass to the tax dropdown
    all_taxes=Create_Tax.objects.filter(enable=True,deleted_at='')
    context={'company_book':company_book,'selected_organisation':selected_organisation,'user_id':user_id,'org_id':org_id,
                 'company_id':company_id,'selected_company':selected_company,'all_company_book':all_company_book,'all_item_category':all_item_category,'all_taxes':all_taxes}

    return render(request,'Accounting_Software_App/create_item.html',context)



def add_new_tax(request,user_id,org_id,company_id):
    if request.method=='POST':
        tax_name=request.POST['tax_name']
        rate=request.POST['rate']
        tax_type=request.POST['tax_type']
        add_category=Create_Tax.objects.create(name=tax_name,rate=rate,type=tax_type,enable=True)
        add_category.save()
        messages.success(request," create New Tax successfully ")
     
        #pass corresponding_organisation comapanybook  to top header dropdown 
        company_book=Company_book.objects.filter(user_id=user_id,organisation_id=org_id, enable=True).values()   
        #pass selected organisation 
        selected_organisation=Organisation.objects.get(id=org_id,user_id=user_id)
        #all company ,pass to the header organisation href tag 
        all_company_book=Company_book.objects.filter(user_id=user_id,first_company=True,enable=True).values() 
        #pass selected company
        selected_company=Company_book.objects.get(id=company_id,user_id=user_id,organisation_id=org_id)
        #pass all category to category dropdown
        all_item_category=Create_Category.objects.filter(module_type_id=3,enable=True,deleted_at='')
        #all tax list pass to the tax dropdown
        all_taxes=Create_Tax.objects.filter(enable=True,deleted_at='')
        context={'company_book':company_book,'selected_organisation':selected_organisation,'user_id':user_id,'org_id':org_id,
                 'company_id':company_id,'selected_company':selected_company,'all_company_book':all_company_book,'all_item_category':all_item_category,'all_taxes':all_taxes}
        
        return render(request,'Accounting_Software_App/create_item.html',context)
    #pass corresponding_organisation comapanybook  to top header dropdown 
    company_book=Company_book.objects.filter(user_id=user_id,organisation_id=org_id, enable=True,deleted_at='').values()   
    #all company ,pass to the header organisation href tag 
    all_company_book=Company_book.objects.filter(user_id=user_id,first_company=True,enable=True,deleted_at='').values() 
    #pass selected company
    selected_company=Company_book.objects.get(id=company_id,user_id=user_id,organisation_id=org_id,deleted_at='')
    #pass selected organisation 
    selected_organisation=Organisation.objects.get(id=org_id,user_id=user_id)
    #pass all category to category dropdown
    all_item_category=Create_Category.objects.filter(module_type_id=3,enable=True,deleted_at='')
    #all tax list pass to the tax dropdown
    all_taxes=Create_Tax.objects.filter(enable=True,deleted_at='')
    context={'company_book':company_book,'selected_organisation':selected_organisation,'user_id':user_id,'org_id':org_id,
                 'company_id':company_id,'selected_company':selected_company,'all_company_book':all_company_book,'all_item_category':all_item_category,'all_taxes':all_taxes}

    return render(request,'Accounting_Software_App/create_item.html',context)
