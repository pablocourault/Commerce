from django.contrib import admin

from .models import User, Category, Auction, Oferta, Comentario

class CategoryAdmin(admin.ModelAdmin):
    list_display = ("id", "description")

class AuctionAdmin(admin.ModelAdmin):
    filter_horizontal =("followed_by",)

# Register your models here.

admin.site.register(User)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Auction, AuctionAdmin)
admin.site.register(Oferta)
admin.site.register(Comentario)

