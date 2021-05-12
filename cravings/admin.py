from django.contrib import admin
from .models import User, Pic, Restaurant, Review, DineList

class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'pk')
    filter_horizontal = ('cravings', 'recommendations', 'history', 'follows')

class RestaurantAdmin(admin.ModelAdmin):
    list_display = ('name', 'clean_name', 'pk', 'mean_rating', 'setting', 'cuisine', 'price_range')
    filter_horizontal = ('images',)

class DineListAdmin(admin.ModelAdmin):
    list_display = ('name', 'pk', 'user')
    filter_horizontal = ('restaurants', 'followers')

admin.site.register(User, UserAdmin)
admin.site.register(Pic)
admin.site.register(Restaurant, RestaurantAdmin)
admin.site.register(Review)
admin.site.register(DineList, DineListAdmin)
