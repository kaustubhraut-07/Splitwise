from django.contrib import admin

# Register your models here.
from .models import User, Group, Expense, Settlement

admin.site.register(User)
admin.site.register(Group)
admin.site.register(Expense)
admin.site.register(Settlement)
