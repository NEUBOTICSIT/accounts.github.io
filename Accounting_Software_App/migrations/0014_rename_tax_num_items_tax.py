# Generated by Django 4.1.1 on 2022-11-21 12:07

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Accounting_Software_App', '0013_alter_create_tax_type'),
    ]

    operations = [
        migrations.RenameField(
            model_name='items',
            old_name='tax_num',
            new_name='tax',
        ),
    ]
