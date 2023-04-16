from django.contrib import admin

from .models import Collection, Comic

admin.site.register(Comic)
admin.site.register(Collection)
