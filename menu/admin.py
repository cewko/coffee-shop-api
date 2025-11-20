from django.contrib import admin
from .models import Component, MenuItem, Menu
from django.contrib.admin.models import LogEntry

admin.site.register(Menu)
admin.site.register(MenuItem)
admin.site.register(Component)
admin.site.register(LogEntry)
