# Generated by Django 4.2.3 on 2023-08-25 21:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('forms', '0010_vm_folder_name_alter_vmrequest_ta_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='vmrequest',
            name='network',
            field=models.CharField(max_length=200, null=True),
        ),
    ]
