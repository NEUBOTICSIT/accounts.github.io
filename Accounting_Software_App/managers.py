from django.contrib.auth.base_user import BaseUserManager
# from django.utils.translation import ugettext_lazy as _
from django.utils.translation import gettext_lazy as _


class CustomUserManager(BaseUserManager):
    use_in_migrations = True

    """
    Custom user model manager where email is the unique identifiers
    for authentication instead of usernames.
    """
    def create_user(self, email, password,first_name,last_name,role,organisation_name,company_name,created_by,enable, **extra_fields):
        """
        Create and save a User with the given email and password.
        """
        if not email:
            raise ValueError('The Email must be set')
        if not password:
            raise ValueError('The Password must be set')
        if not first_name:
            raise ValueError('The first name must be set')
        if not last_name:
            raise ValueError('The last name must be set')
        email = self.normalize_email(email)
        first_name=first_name
        last_name=last_name
        role=role
        organisation_name=organisation_name
        company_name=company_name
        created_by=created_by
        enable=enable
        user = self.model(email=email,first_name=first_name, last_name=last_name,role=role,organisation_name=organisation_name,company_name=company_name,created_by=created_by,enable=enable,**extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password,**extra_fields):
        """
        Create and save a SuperUser with the given email and password.
        """
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')
        return self.create_user(email, password,'superuser','superuser','superuser','','','',True, **extra_fields)