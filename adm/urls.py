from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [

    path(
        "",
        views.home,
        name="home"
    ),

    path(
        "restaurants/",
        views.restaurants,
        name="restaurants"
    ),

    path(
        "restaurant/<int:restaurant_id>/",
        views.restaurant_detail,
        name="restaurant_detail"
    ),

    path(
        "menu/",
        views.menu,
        name="menu"
    ),

    path(
        "food/<int:food_id>/",
        views.food_detail,
        name="food_detail"
    ),

    path(
        "offers/",
        views.offers,
        name="offers"
    ),

    path(
        "cart/",
        views.cart,
        name="cart"
    ),

    path(
        "cart/add/<int:food_id>/",
        views.add_to_cart,
        name="add_to_cart"
    ),

    path(
        "cart/update/<int:item_id>/",
        views.update_cart,
        name="update_cart"
    ),

    path(
        "cart/remove/<int:item_id>/",
        views.remove_from_cart,
        name="remove_from_cart"
    ),

    path(
        "checkout/",
        views.checkout,
        name="checkout"
    ),

    path(
        "order-confirmation/",
        views.order_confirmation,
        name="order_confirmation"
    ),

    path(
        "orders/",
        views.orders,
        name="orders"
    ),

    path(
        "order/<int:order_id>/",
        views.order_detail,
        name="order_detail"
    ),

    path(
        "login/",
        views.login_view,
        name="login"
    ),

    path(
        "signup/",
        views.signup,
        name="signup"
    ),

    path(
        "logout/",
        views.logout_view,
        name="logout"
    ),
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)