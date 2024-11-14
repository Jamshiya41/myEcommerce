from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from . import views

urlpatterns = [
    # path('', views.base, name="base"),
    path('', views.home, name="home"),
    path('signup/', views.signup, name="signup"),
    path('signin/', views.signin, name="signin"),
    path('product/<int:product_id>/', views.product_detail, name='product_detail'),
    path('category/<int:category_id>/', views.category_detail, name='category_detail'),
    path('signout/', views.SignOut, name="signout"),
    path('cart/', views.cart_detail, name='cart_detail'),
    path('add-to-cart/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('product_list/', views.product_list, name='product_list'),
    path('about/', views.about_details, name='about'),
    path('cart/increment/<int:item_id>/', views.increment_cart_item, name='increment_cart_item'),
    path('cart/decrement/<int:item_id>/', views.decrement_cart_item, name='decrement_cart_item'),
    path('cart_detail/', views.cart_detail, name='cart_detail'),
    path('cart/remove/<int:item_id>/', views.remove_cart_item, name='remove_cart_item'),
    path('checkout/', views.checkout, name='checkout'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)