from django.urls import path
from . import views

urlpatterns = [
######################### LOGIN,REGISTRATION,LOGOUT ######################
    path('login/',views.login,name='login'),
    path('register/',views.register,name='register'),
    path('logout/',views.logout,name='logout'),
    path('change_password/',views.change_password,name='change_password'),

########################## CUSTOMER ##########################
    path('',views.index,name='index'),
    path('menu/',views.menu,name='menu'),
    path('profile/',views.profile,name='profile'),
    path('cart/',views.cart,name='cart'),
    path('add_to_cart/<int:pk>/',views.add_to_cart,name='add_to_cart'),
    path('remove_from_cart/<int:pk>/',views.remove_from_cart,name='remove_from_cart'),
    path('increase_quantity/<int:pk>/', views.increase_quantity, name='increase_quantity'),
    path('decrease_quantity/<int:pk>/', views.decrease_quantity, name='decrease_quantity'),
    path('wishlist/',views.wishlist,name='wishlist'),
    path('add_to_wishlist/<int:pk>/',views.add_to_wishlist,name='add_to_wishlist'),
    path('remove_from_wishlist/<int:pk>/',views.remove_from_wishlist,name='remove_from_wishlist'),
    path('gallary/',views.gallary,name='gallary'),
    path('contact/',views.contact,name='contact'),
    path('leave_a_comment/',views.leave_a_comment,name='leave_a_comment'),
    path('checkout/',views.checkout,name='checkout'),
    path('feedback/',views.feedback,name='feedback'),
    path('reservation/',views.reservation,name='reservation'),
    path('faq/',views.faq,name='faq'),
    path('mybookings/',views.mybookings,name='mybookings'),
    path('myorders/',views.myorders,name='myorders'),
    path('<int:pk>/',views.track_order,name='track_order'),
    path('create_checkout_session/', views.create_checkout_session, name='create_checkout_session'),
    path('success/', views.success, name='success'),
    path('cancel/', views.cancel, name='cancel'),
    path('cancel_reservation/<int:pk>/', views.cancel_reservation, name='cancel_reservation'),
    path('cancle_order/<int:pk>/', views.cancle_order, name='cancle_order'),
    path('forgot_password/',views.forgot_password,name='forgot_password'),
    path('verify_otp/',views.verify_otp,name='verify_otp'),
    path('new_password/',views.new_password,name='new_password'),


########################## MANAGER ##########################
    path('user/',views.user,name='user'),
    path('delivery_persons/',views.delivery_persons,name='delivery_persons'),
    path('add_delivery_person/',views.add_delivery_person,name='add_delivery_person'),
    path('feedbacks/',views.feedbacks,name='feedbacks'),
    path('category/',views.category,name='category'),
    path('food_items/',views.food_items,name='food_items'),
    path('add_food_item/',views.add_food_item,name='add_food_item'),
    path('reservations/',views.reservations,name='reservations'),
    path('orders/',views.orders,name='orders'),
    path('delete_category/<int:pk>/', views.delete_category, name='delete_category'),
    path('delete_food_items/<int:pk>/', views.delete_food_items, name='delete_food_items'),
    path('delete_delivery_person/<int:pk>/', views.delete_delivery_person, name='delete_delivery_person'),
    path('show_user_details/<int:pk>/', views.show_user_details, name='show_user_details'),
    path('show_order_details/<int:pk>/', views.show_order_details, name='show_order_details'),
    path('edit_food_item/<int:pk>/', views.edit_food_item, name='edit_food_item'),
]
