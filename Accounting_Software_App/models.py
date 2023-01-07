# from email.policy import default
# from enum import unique
# from tabnanny import verbose
# from django.db import models
# # from django.contrib.auth.models import User
# from django.contrib.auth.models import AbstractUser
# from Accounting_Software_App.managers import CustomUserManager
# import jsonfield



# class User(AbstractUser):
#     username = None
#     email = models.EmailField(unique=True, blank=False,
#                               error_messages={
#                                   'unique': "A user with that email already exists.",
#                               })
#     organisation_name = models.CharField(max_length=100)
#     # organisation_email = models.EmailField(max_length=100)
#     company_name = jsonfield.JSONField()
#     role = models.CharField(max_length=100,null=True)
#     created_by = models.CharField(max_length=30)
#     enable=models.BooleanField(default=True,null=True)  
#     updated_at = models.DateTimeField(null=True, blank=True)
#     deleted_at = models.CharField(max_length=100,blank=True)

#     USERNAME_FIELD = "email"
#     REQUIRED_FIELDS = []

#     def __str__(self):
#         return self.email

#     def get_full_name(self):
#         return self.first_name+ ' ' + self.last_name
#     objects = CustomUserManager()
    
    
    
# class Organisation(models.Model):
#     id=models.AutoField(primary_key=True)
#     user = models.ForeignKey(User, on_delete=models.CASCADE)
#     email = models.EmailField(unique=True, blank=False,
#                               error_messages={
#                                   'unique': "A user with that email already exists.",
#                               })
#     organisation_name = models.CharField(max_length=100)
#     first_organisation=models.BooleanField(default=False,null=False)
#     enable=models.BooleanField(default=True,null=True) 
#     created_at = models.DateTimeField(auto_now_add=True,null=True, blank=True)
#     updated_at = models.DateTimeField(null=True, blank=True)
#     deleted_at = models.CharField(max_length=100,blank=True)

#     def __str__(self):
#         return self.organisation_name


# class Company_book(models.Model):
#     user = models.ForeignKey(User, on_delete=models.CASCADE)
#     organisation = models.ForeignKey(Organisation, on_delete=models.CASCADE)
#     company = models.CharField(max_length=100)
#     email = models.EmailField(max_length=100)
#     currency = models.CharField(max_length=100,default='')
#     tax_num = models.CharField(max_length=100,default='')
#     company_address = models.CharField(max_length=100,default='')
#     phone_number = models.CharField(max_length=100,default='')
#     zip_code = models.CharField(max_length=100,default='')
#     city = models.CharField(max_length=100,default='')
#     state = models.CharField(max_length=100,default='')  
#     enable=models.BooleanField(default=True,null=True)  
#     first_company=models.BooleanField(default=False,null=False)
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(null=True, blank=True)
#     deleted_at = models.CharField(max_length=100,blank=True)
#     # delete_status=models.BooleanField(default=False,null=False)
#     def __str__(self):
#         return self. company
    
# class Role(models.Model):
#     role_name = models.CharField(max_length=100)
    
#     def __str__(self):
#         return self.role_name
    
    
# class Items(models.Model):
#     user = models.ForeignKey(User, on_delete=models.CASCADE)
#     organisation = models.ForeignKey(Organisation, on_delete=models.CASCADE)
#     company = models.ForeignKey(Company_book, on_delete=models.CASCADE)
#     name = models.CharField(max_length=100)
#     tax = models.CharField(max_length=100,default='')
#     description = models.CharField(max_length=100,default='')
#     sale_price = models.CharField(max_length=100,default='')
#     purchase_price = models.CharField(max_length=100,default='')  
#     category = models.CharField(max_length=100,default='')
#     picture=models.ImageField(blank=True, null=True, upload_to='Account_Software_App/images/',default='')  
#     # picture=models.ImageField(blank=True, null=True, upload_to='Account_Software_App/images/%Y/%m/%d/')  
#     enable=models.BooleanField(default=True,null=True)  
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(null=True, blank=True)
#     deleted_at = models.CharField(max_length=100,blank=True)
#     def __str__(self):
#         return self. name
    

# class Module_Type(models.Model):
#     type = models.CharField(max_length=100)
    
#     def __str__(self):
#         return self.type
    

# #create category
# class Create_Category(models.Model):
#     id=models.AutoField(primary_key=True)
#     name = models.CharField(max_length=100)
#     module_type = models.ForeignKey(Module_Type, on_delete=models.CASCADE)
#     color=models.CharField(max_length=7)
#     enable=models.BooleanField(default=True,null=True) 
#     created_at = models.DateTimeField(auto_now_add=True,null=True, blank=True)
#     updated_at = models.DateTimeField(null=True, blank=True)
#     deleted_at = models.CharField(max_length=100,blank=True)

#     def __str__(self):
#         return self.name


# #create category
# class Create_Tax(models.Model):
#     COMPOUND = 'CD'
#     FIXED = 'FD'
#     INCLUSIVE = 'IN'
#     NORMAL = 'NR'
#     WITHHOLDING = 'WH'
#     TYPE = [
#         (COMPOUND, 'Compound'),
#         (FIXED, 'Fixed'),
#         (INCLUSIVE, 'Inclusive'),
#         (NORMAL, 'Normal'),
#         (WITHHOLDING, 'Withholding'),
#     ]
#     id=models.AutoField(primary_key=True)
#     name = models.CharField(max_length=100)
#     rate = models.CharField(max_length=100)
#     type = models.CharField(max_length=20,choices=TYPE,default=COMPOUND,)
#     enable = models.BooleanField(default=True,null=True) 
#     created_at = models.DateTimeField(auto_now_add=True,null=True, blank=True)
#     updated_at = models.DateTimeField(null=True, blank=True)
#     deleted_at = models.CharField(max_length=100,blank=True)

#     def __str__(self):
#         return self.name
