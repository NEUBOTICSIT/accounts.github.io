# Generated by Django 4.1.1 on 2022-11-21 09:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Accounting_Software_App', '0012_create_tax'),
    ]

    operations = [
        migrations.AlterField(
            model_name='create_tax',
            name='type',
            field=models.CharField(choices=[('CD', 'Compound'), ('FD', 'Fixed'), ('IN', 'Inclusive'), ('NR', 'Normal'), ('WH', 'Withholding')], default='CD', max_length=20),
        ),
    ]
