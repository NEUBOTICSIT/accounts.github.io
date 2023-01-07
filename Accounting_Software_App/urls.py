from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from . views import setting_module_views,user_module_views,item_module_views



app_name = "Accounting_Software_App"

urlpatterns = [
#uer Module
    path('',user_module_views.signup,name='signup'),
    path('activate/<uidb64>/<token>', user_module_views.activate, name='activate'),
    path('signin',user_module_views.signin,name='signin'),
    path('signout',user_module_views.signout,name='signout'),
    path('index/<int:user_id>/<int:org_id>/<int:company_id>', user_module_views.index, name='index'),
    path('profile/<int:user_id>/<int:org_id>/<int:company_id>', user_module_views.profile, name='profile'),
    
    path('users/<int:user_id>/<int:org_id>/<int:company_id>', user_module_views.users, name='users'),
    path('create_user/<int:user_id>/<int:org_id>/<int:company_id>', user_module_views.create_user, name='create_user'),
    path('organisation_user_activate/<uidb64>/<token>', user_module_views.organisation_user_activate, name='organisation_user_activate'),
    path('edit_user/<int:user_id>/<int:org_id>/<int:company_id>/<int:edit_user_id>', user_module_views.edit_user, name='edit_user'),
    path('delete_user/<int:user_id>/<int:org_id>/<int:company_id>/<int:delete_user_id>', user_module_views.delete_user, name='delete_user'),
    
    path('manage_company/<int:user_id>/<int:org_id>/<int:company_id>', user_module_views.manage_company, name='manage_company'),
    path('create_company_book/<int:user_id>/<int:org_id>/<int:company_id>', user_module_views.create_company_book, name='create_company_book'),
    path('edit_company/<int:user_id>/<int:org_id>/<int:company_id>/<int:edit_company_id>', user_module_views.edit_company, name='edit_company'),
    path('delete_company/<int:user_id>/<int:org_id>/<int:company_id>/<int:delete_company_id>', user_module_views.delete_company, name='delete_company'),

    path('manage_organisation/<int:user_id>/<int:org_id>/<int:company_id>',user_module_views.manage_organisation,name="manage_organisation"),
    path('create_organisation/<int:user_id>/<int:org_id>/<int:company_id>',user_module_views.create_organisation,name="create_organisation"),
    path('edit_organisation/<int:user_id>/<int:org_id>/<int:company_id>/<int:edit_organisation_id>', user_module_views.edit_organisation, name='edit_organisation'),
#Item Module
    path('items/<int:user_id>/<int:org_id>/<int:company_id>',item_module_views.items,name="items"),
    path('create_item/<int:user_id>/<int:org_id>/<int:company_id>',item_module_views.create_item,name="create_item"),
    path('edit_item/<int:user_id>/<int:org_id>/<int:company_id>/<int:edit_item_id>',item_module_views.edit_item,name="edit_item"),
    path('delete_item/<int:user_id>/<int:org_id>/<int:company_id>/<int:delete_item_id>', item_module_views.delete_item, name='delete_item'),
    #add new caregory 
    path('add_new_category/<int:user_id>/<int:org_id>/<int:company_id>', item_module_views.add_new_category, name='add_new_category'),
    #add new tax 
    path('add_new_tax/<int:user_id>/<int:org_id>/<int:company_id>', item_module_views.add_new_tax, name='add_new_tax'),
#setting Module
    path('settings/<int:user_id>/<int:org_id>/<int:company_id>',setting_module_views.settings,name="settings"),
    path('categories/<int:user_id>/<int:org_id>/<int:company_id>',setting_module_views.categories,name="categories"),
    path('create_categories/<int:user_id>/<int:org_id>/<int:company_id>',setting_module_views.create_categories,name="create_categories"),
    path('edit_category/<int:user_id>/<int:org_id>/<int:company_id>/<int:edit_category_id>',setting_module_views.edit_category,name="edit_category"),
    path('delete_category/<int:user_id>/<int:org_id>/<int:company_id>/<int:delete_category_id>', setting_module_views.delete_category, name='delete_category'),

    path('taxes/<int:user_id>/<int:org_id>/<int:company_id>',setting_module_views.taxes,name="taxes"),
    path('create_tax/<int:user_id>/<int:org_id>/<int:company_id>',setting_module_views.create_tax,name="create_tax"),
    path('edit_tax/<int:user_id>/<int:org_id>/<int:company_id>/<int:edit_tax_id>',setting_module_views.edit_tax,name="edit_tax"),
    path('delete_tax/<int:user_id>/<int:org_id>/<int:company_id>/<int:delete_tax_id>', setting_module_views.delete_tax, name='delete_tax'),



] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
#  +static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
