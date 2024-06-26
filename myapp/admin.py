from django.contrib import admin
from .models import *
from django.utils.html import format_html

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('display_profile_pic', 'fname', 'lname', 'email', 'mobile', 'address', 'city', 'state')

    def display_profile_pic(self, obj):
        return format_html('<img src="{}" width="35" />', obj.profile_pic.url)

    display_profile_pic.short_description = 'Profile Picture'

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id','name',)

@admin.register(Menu)
class MenuAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'display_image', 'price1', 'price2')

    def display_image(self, obj):
        return format_html('<img src="{}" width="60" />', obj.image.url)
    display_image.short_description = 'Image'

@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ('food_item', 'user', 'date', 'time', 'quantity')

@admin.register(Leave_A_Comment)
class LeaveACommentAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'message')

@admin.register(Reservation)
class ReservationAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'mobile', 'person', 'date', 'time', 'message')

@admin.register(Feedback)
class FeedbackAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'rating', 'message')

@admin.register(Wishlist)
class WishlistAdmin(admin.ModelAdmin):
    list_display = ('food_item', 'user', 'date', 'time')

@admin.register(DeliveryPerson)
class DeliveryPersonAdmin(admin.ModelAdmin):
    list_display = ('name', 'vehicle_number', 'display_profile_pic')

    def display_profile_pic(self, obj):
        return format_html('<img src="{}" width="50" />', obj.profile_pic.url)

    display_profile_pic.short_description = 'Profile Picture'

@admin.register(MyOrder)
class MyOrderAdmin(admin.ModelAdmin):
    list_display = ('fname','phone', 'address','food_item_name', 'price', 'quantity', 'total_price', 'payment_method', 'date', 'time', 'delivery_person', 'status')
    # list_filter = ('date', 'time')


