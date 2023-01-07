from django.db import models


class Module_Type(models.Model):
    type = models.CharField(max_length=100)
    
    def __str__(self):
        return self.type


#create category
class Create_Category(models.Model):
    id=models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    module_type = models.ForeignKey(Module_Type, on_delete=models.CASCADE)
    color=models.CharField(max_length=7)
    enable=models.BooleanField(default=True,null=True) 
    created_at = models.DateTimeField(auto_now_add=True,null=True, blank=True)
    updated_at = models.DateTimeField(null=True, blank=True)
    deleted_at = models.CharField(max_length=100,blank=True)

    def __str__(self):
        return self.name


#create category
class Create_Tax(models.Model):
    COMPOUND = 'CD'
    FIXED = 'FD'
    INCLUSIVE = 'IN'
    NORMAL = 'NR'
    WITHHOLDING = 'WH'
    TYPE = [
        (COMPOUND, 'Compound'),
        (FIXED, 'Fixed'),
        (INCLUSIVE, 'Inclusive'),
        (NORMAL, 'Normal'),
        (WITHHOLDING, 'Withholding'),
    ]
    id=models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    rate = models.CharField(max_length=100)
    type = models.CharField(max_length=20,choices=TYPE,default=COMPOUND,)
    enable = models.BooleanField(default=True,null=True) 
    created_at = models.DateTimeField(auto_now_add=True,null=True, blank=True)
    updated_at = models.DateTimeField(null=True, blank=True)
    deleted_at = models.CharField(max_length=100,blank=True)

    def __str__(self):
        return self.name
