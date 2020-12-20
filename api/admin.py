from django.contrib import admin
from django.contrib.auth.models import User
from .models import Favourite

class FavouriteAdmin(admin.ModelAdmin):
    fieldsets = [
        ("user", {'fields': ["user"]}),
        ("favourites", {'fields': ["favourites"]}),
    ]
    list_display = ('user','favourites')

admin.site.register(Favourite, FavouriteAdmin)