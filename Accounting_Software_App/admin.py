from django import forms
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from .forms import CustomUserChangeForm,CustomUserCreationForm

from .models import User,Role,Organisation,Company_book,Items,Module_Type,Create_Category,Create_Tax


# class AddUserForm(forms.ModelForm):
#     """
#     New User Form. Requires password confirmation.
#     """
#     password1 = forms.CharField(
#         label='Password', widget=forms.PasswordInput
#     )
#     password2 = forms.CharField(
#         label='Confirm password', widget=forms.PasswordInput
#     )

#     class Meta:
#         model = User
#         fields = ('email', 'first_name', 'last_name', 'role', )

#     def clean_password2(self):
#         # Check that the two password entries match
#         password1 = self.cleaned_data.get("password1")
#         password2 = self.cleaned_data.get("password2")
#         if password1 and password2 and password1 != password2:
#             raise forms.ValidationError("Passwords do not match")
#         return password2

#     def save(self, commit=True):
#         # Save the provided password in hashed format
#         user = super().save(commit=False)
#         user.set_password(self.cleaned_data["password1"])
#         if commit:
#             user.save()
#         return user


# class UpdateUserForm(forms.ModelForm):
#     """
#     Update User Form. Doesn't allow changing password in the Admin.
#     """
#     password = ReadOnlyPasswordHashField()

#     class Meta:
#         model = User
#         fields = (
#             'email', 'password', 'first_name', 'role', 'last_name', 'is_active',
#             'is_staff'
#         )

#     def clean_password(self):
# # Password can't be changed in the admin
#         return self.initial["password"]


class UserAdmin(BaseUserAdmin):
    form = CustomUserCreationForm
    add_form = CustomUserChangeForm
    model: User

    list_display = ('email', 'first_name', 'last_name', 'is_staff')
    list_filter = ('is_staff', )
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name', 'role', 'organisation_name','created_by','enable')}),
        ('Permissions', {'fields': ('is_active', 'is_staff','is_superuser')}),
    )
    add_fieldsets = (
        (
            None,
            {
                'classes': ('wide',),
                'fields': (
                    'email', 'first_name', 'last_name','role', 'password1',
                    'password2','organisation_name','created_by'
                )
            }
        ),
    )
    search_fields = ('email', 'first_name', 'last_name')
    ordering = ('email', 'first_name', 'last_name')
    filter_horizontal = ()

# admin.site.unregister(User)
admin.site.register(User, UserAdmin)
admin.site.register(Role)
admin.site.register(Organisation)
admin.site.register(Company_book)
admin.site.register(Items)
admin.site.register(Module_Type)
admin.site.register(Create_Category)
admin.site.register(Create_Tax)