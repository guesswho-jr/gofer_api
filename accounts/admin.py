from django.contrib import admin
from .models import UserProfile, Provider, Social

# Register your models here.
admin.site.register(UserProfile)
admin.site.register(Provider)
admin.site.register(Social)