from django.contrib import admin

# Register your models here.
from .models import Mail, ErrorLog

admin.site.register(Mail)
admin.site.register(ErrorLog)