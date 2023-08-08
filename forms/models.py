from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Exercise(models.Model):
    name=models.CharField(max_length=200)
    description=models.TextField(null=True)
    pdf_file=models.FileField(upload_to='exercises/')

    def __str__(self):
        return self.name

class VMRequest(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    course_number=models.CharField(max_length=200)
    course_name=models.CharField(max_length=200)
    instructor_name=models.CharField(max_length=200)
    ta_name=models.CharField(max_length=200)
    description=models.TextField(null=True)
    semester=models.CharField(max_length=200)
    year=models.PositiveSmallIntegerField()
    os=models.CharField(max_length=200)
    cpu_count=models.PositiveSmallIntegerField()
    ram=models.PositiveSmallIntegerField()
    ram_reason=models.TextField()
    hard_disk=models.PositiveSmallIntegerField()
    disk_reason=models.TextField()
    num_vm=models.PositiveSmallIntegerField()
    start_date=models.CharField(max_length=200)
    end_date=models.CharField(max_length=200)
    self_sudo=models.CharField(max_length=200)
    vm_users=models.TextField()
    vm_user_file=models.FileField(upload_to='vm_users/')
    status=models.CharField(max_length=200)

    def __str__(self):
        return course_number+'_'+instructor_name+'_'+semester+year

class VM(models.Model):
    vmrequest=models.ForeignKey(VMRequest,on_delete=models.CASCADE, null=True,blank=True)
    ip_addr=models.CharField(max_length=200)
    vm_name=models.CharField(max_length=200)
    os=models.CharField(max_length=200)
    template=models.CharField(max_length=200)

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


    


        
