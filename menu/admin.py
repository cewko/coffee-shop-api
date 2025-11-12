from django.contrib import admin
from .models import Component, MenuItem, Menu

admin.site.register(Menu)
admin.site.register(MenuItem)
admin.site.register(Component)
