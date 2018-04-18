from django.contrib import admin

from .models import Table
from .models import Reservation

admin.site.register(Table)
admin.site.register(Reservation)
