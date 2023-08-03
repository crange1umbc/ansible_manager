from django.contrib import admin
from .models import Exercise
from .models import VMRequest
from .models import VM
# Register your models here.

admin.site.register(Exercise)
admin.site.register(VMRequest)
admin.site.register(VM)


