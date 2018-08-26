from django.contrib import admin
from app_network.models.models import Activity, Connection

# Register your models here.
admin.site.register(Connection)
admin.site.register(Activity)