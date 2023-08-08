from django.contrib import admin
from .models import Exercise
from .models import VMRequest
from .models import VM
from .models import CryptRequest,CryptText
# Register your models here.

admin.site.register(Exercise)
admin.site.register(VMRequest)
admin.site.register(VM)
admin.site.register(CryptRequest)
admin.site.register(CryptText)


