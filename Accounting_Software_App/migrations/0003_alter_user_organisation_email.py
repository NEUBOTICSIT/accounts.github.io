# Generated by Django 4.1.1 on 2022-11-07 08:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Accounting_Software_App', '0002_company_book_first_company_user_organisation_email'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='organisation_email',
            field=models.EmailField(max_length=100),
        ),
    ]
