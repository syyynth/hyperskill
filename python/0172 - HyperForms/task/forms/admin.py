from django.contrib import admin

from .models import FormModel, FormField, FormRecord, FormData

admin.site.register([FormModel, FormField, FormRecord, FormData])
