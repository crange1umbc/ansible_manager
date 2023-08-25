from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.dispatch import receiver
from django.db.models.signals import pre_delete
import os

# Create your models here.

def validate_pdf_extension(value):
    if not value.name.endswith('.pdf'):
        raise ValidationError('Only Pdf files are allowed.')

class Exercise(models.Model):
    name=models.CharField(max_length=200)
    description=models.TextField(null=True)
    pdf_file=models.FileField(upload_to='exercises/',validators=[validate_pdf_extension])

    def __str__(self):
        return self.name

@receiver(pre_delete, sender=Exercise)
def delete_pdf_file(sender,instance,**kwargs):
    if instance.pdf_file:
        if os.path.isfile(instance.pdf_file.path):
            os.remove(instance.pdf_file.path)

pre_delete.connect(delete_pdf_file,sender=Exercise)

class VMRequest(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    course_number=models.CharField(max_length=200, null=True)
    course_name=models.CharField(max_length=200)
    instructor_name=models.CharField(max_length=200)
    ta_name=models.CharField(max_length=200, null=True)
    description=models.TextField(null=True)
    semester=models.CharField(max_length=200)
    year=models.PositiveSmallIntegerField()
    os=models.CharField(max_length=200)
    cpu_count=models.PositiveSmallIntegerField(null=True)
    ram=models.PositiveSmallIntegerField(null=True)
    ram_reason=models.TextField(null=True)
    hard_disk=models.PositiveSmallIntegerField(null=True)
    disk_reason=models.TextField(null=True)
    num_vm=models.PositiveSmallIntegerField()
    start_date=models.CharField(max_length=200, null=True)
    end_date=models.CharField(max_length=200, null=True)
    self_sudo=models.CharField(max_length=200, null=True)
    vm_users=models.TextField(null=True)
    vm_user_file=models.FileField(upload_to='vm_users/', null=True)
    status=models.CharField(max_length=200, null=True)

class VM(models.Model):
    vmrequest=models.ForeignKey(VMRequest,on_delete=models.CASCADE, null=True,blank=True)
    ip_addr=models.CharField(max_length=200)
    vm_name=models.CharField(max_length=200)
    folder_name=models.CharField(max_length=200, null=True)
    os=models.CharField(max_length=200)
    template=models.CharField(max_length=200, null=True)

class CryptRequest(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    technique=models.CharField(max_length=200)
    random_key=models.CharField(max_length=200)
    key=models.CharField(max_length=300,null=True)
    num_cipher=models.PositiveSmallIntegerField(null=True)
    ip_address_list=models.TextField(null=True)

class CryptText(models.Model):
    cryptreq=models.ForeignKey(CryptRequest,on_delete=models.CASCADE)
    plaintext=models.TextField()
    ciphertext=models.TextField()
    key=models.TextField()
    ip_addr=models.CharField(max_length=200, null=True)


    


        
