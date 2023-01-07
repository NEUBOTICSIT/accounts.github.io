from django.db import models
from . user_module_models import Organisation,User,Company_book
from . setting_module_models import Create_Tax,Create_Category

class Items(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    organisation = models.ForeignKey(Organisation, on_delete=models.CASCADE)
    company = models.ForeignKey(Company_book, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    tax = models.ForeignKey(Create_Tax, on_delete=models.CASCADE)
    description = models.CharField(max_length=100,default='')
    sale_price = models.CharField(max_length=100,default='')
    purchase_price = models.CharField(max_length=100,default='')  
    category = models.ForeignKey(Create_Category, on_delete=models.CASCADE)
    picture=models.ImageField(upload_to='Account_Software_App/images/',default='')  
    enable=models.BooleanField(default=True,null=True)  
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(null=True, blank=True)
    deleted_at = models.CharField(max_length=100,blank=True)
    def __str__(self):
        return self. name
    

