from django.urls import path
from . import views


urlpatterns = [

    # Home
    path("", views.home, name="home"),

    # Restaurants
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

    # Food
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

    # Offers
    path(
        "offers/",
        views.offers,
        name="offers"
    ),

    # Cart
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

    # Checkout
    path(
        "checkout/",
        views.checkout,
        name="checkout"
    ),

    # Order
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

    # Authentication
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