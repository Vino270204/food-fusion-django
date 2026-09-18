from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages
from django.db.models import Q
from django.db import transaction
from django.utils import timezone

from .models import (
    Restaurant,
    Food,
    Cart,
    CartItem,
    Offer,
    Order,
    OrderItem,
    Payment,
)


# =========================
# HOME
# =========================

def home(request):

    restaurants = Restaurant.objects.filter(
        is_active=True
    )

    foods = Food.objects.filter(
        is_available=True
    )[:6]

    today = timezone.now().date()

    offers = Offer.objects.filter(
        is_active=True,
        start_date__lte=today,
        end_date__gte=today
    )

    context = {
        "restaurants": restaurants,
        "foods": foods,
        "offers": offers,
    }

    return render(
        request,
        "pages/home.html",
        context
    )


# =========================
# RESTAURANTS
# =========================

def restaurants(request):

    restaurant_list = Restaurant.objects.filter(
        is_active=True
    )

    return render(
        request,
        "pages/restaurants.html",
        {
            "restaurants": restaurant_list
        }
    )


def restaurant_detail(request, restaurant_id):

    restaurant = get_object_or_404(
        Restaurant,
        id=restaurant_id,
        is_active=True
    )

    foods = Food.objects.filter(
        restaurant=restaurant,
        is_available=True
    )

    return render(
        request,
        "pages/restaurant_detail.html",
        {
            "restaurant": restaurant,
            "foods": foods
        }
    )


# =========================
# MENU
# =========================

def menu(request):

    search = request.GET.get(
        "search",
        ""
    ).strip()

    foods = Food.objects.filter(
        is_available=True
    )

    if search:

        foods = foods.filter(
            Q(name__icontains=search) |
            Q(category__icontains=search) |
            Q(restaurant__name__icontains=search)
        )

    return render(
        request,
        "pages/menu.html",
        {
            "foods": foods,
            "search": search
        }
    )


def food_detail(request, food_id):

    foods = get_object_or_404(
        Food,
        id=food_id,
        is_available=True
    )

    return render(
        request,
        "pages/food_detail.html",
        {
            "foods": foods
        }
    )


# =========================
# OFFERS
# =========================

# def offers(request):

#     today = timezone.now().date()

#     offer_list = Offer.objects.filter(
#         is_active=True,
#         start_date__lte=today,
#         end_date__gte=today
#     )

#     return render(
#         request,
#         "pages/offers.html",
#         {
#             "offers": offer_list
#         }
#     )
def offers(request):

    offers = Offer.objects.filter(
        is_active=True
    )

    return render(request, "pages/offers.html", {
        "offers": offers
    })

# =========================
# LOGIN
# =========================

def login_view(request):

    if request.method == "POST":

        email = request.POST.get(
            "email"
        ).strip()

        password = request.POST.get(
            "password"
        )

        user = authenticate(
            request,
            username=email,
            password=password
        )

        if user is not None:

            login(
                request,
                user
            )

            messages.success(
                request,
                "Login successful!"
            )

            return redirect("home")

        messages.error(
            request,
            "Invalid email or password."
        )

    return render(
        request,
        "pages/login.html"
    )


# =========================
# SIGNUP
# =========================

def signup(request):

    if request.method == "POST":

        full_name = request.POST.get(
            "full_name"
        ).strip()

        email = request.POST.get(
            "email"
        ).strip()

        password = request.POST.get(
            "password"
        )

        if User.objects.filter(
            username=email
        ).exists():

            messages.error(
                request,
                "Email already registered."
            )

            return redirect("signup")

        User.objects.create_user(
            username=email,
            email=email,
            password=password,
            first_name=full_name
        )

        messages.success(
            request,
            "Account created successfully!"
        )

        return redirect("login")

    return render(
        request,
        "pages/signup.html"
    )


# =========================
# LOGOUT
# =========================

@login_required
def logout_view(request):

    logout(request)

    return redirect("home")


# =========================
# ADD TO CART
# =========================

@login_required
def add_to_cart(request, food_id):

    food = get_object_or_404(
        Food,
        id=food_id,
        is_available=True
    )

    cart, cart_created = Cart.objects.get_or_create(
        user=request.user
    )

    cart_item, item_created = CartItem.objects.get_or_create(
        cart=cart,
        food=food,
        defaults={
            "quantity": 1
        }
    )

    if not item_created:
        cart_item.quantity += 1

    cart_item.save()

    print("================================")
    print("USER:", request.user)
    print("CART ID:", cart.id)
    print("FOOD:", food.name)
    print("CART ITEM ID:", cart_item.id)
    print("QUANTITY:", cart_item.quantity)
    print(
        "TOTAL CART ITEMS:",
        CartItem.objects.filter(cart=cart).count()
    )
    print("================================")

    return redirect("cart")


# =========================
# CART
# =========================

@login_required
def cart(request):

    cart, created = Cart.objects.get_or_create(
        user=request.user
    )

    cart_items = cart.items.select_related(
        "food"
    )

    subtotal = 0

    for item in cart_items:

        item.total = (
            item.food.price *
            item.quantity
        )

        subtotal += item.total

    delivery_charge = (
        30 if cart_items.exists()
        else 0
    )

    total = (
        subtotal +
        delivery_charge
    )

    context = {
        "cart_items": cart_items,
        "subtotal": subtotal,
        "delivery_charge": delivery_charge,
        "total": total,
    }

    return render(
        request,
        "pages/cart.html",
        context
    )


# =========================
# UPDATE CART
# =========================

@login_required
def update_cart(request, item_id):

    item = get_object_or_404(
        CartItem,
        id=item_id,
        cart__user=request.user
    )

    if request.method == "POST":

        try:

            quantity = int(
                request.POST.get(
                    "quantity",
                    1
                )
            )

            if quantity > 0:

                item.quantity = quantity
                item.save()

            else:

                item.delete()

        except (ValueError, TypeError):

            pass

    return redirect("cart")


# =========================
# REMOVE CART ITEM
# =========================

@login_required
def remove_from_cart(request, item_id):

    item = get_object_or_404(
        CartItem,
        id=item_id,
        cart__user=request.user
    )

    if request.method == "POST":

        item.delete()

    return redirect("cart")


# =========================
# CHECKOUT
# =========================

@login_required
def checkout(request):

    cart, created = Cart.objects.get_or_create(
        user=request.user
    )

    cart_items = cart.items.select_related(
        "food"
    )

    if not cart_items.exists():

        return redirect("cart")

    subtotal = 0

    for item in cart_items:

        subtotal += (
            item.food.price *
            item.quantity
        )

    delivery_charge = 30

    total = (
        subtotal +
        delivery_charge
    )

    if request.method == "POST":

        name = request.POST.get(
            "name"
        ).strip()

        email = request.POST.get(
            "email"
        ).strip()

        phone = request.POST.get(
            "phone"
        ).strip()

        address = request.POST.get(
            "address"
        ).strip()

        city = request.POST.get(
            "city"
        ).strip()

        pincode = request.POST.get(
            "pincode"
        ).strip()

        payment_method = request.POST.get(
            "payment_method"
        )

        if not all([
            name,
            email,
            phone,
            address,
            city,
            pincode,
            payment_method
        ]):

            messages.error(
                request,
                "Please fill all required fields."
            )

            return render(
                request,
                "pages/checkout.html",
                {
                    "cart_items": cart_items,
                    "subtotal": subtotal,
                    "delivery_charge": delivery_charge,
                    "total": total,
                }
            )

        if payment_method not in [
            "cod",
            "upi",
            "card"
        ]:

            messages.error(
                request,
                "Please select a valid payment method."
            )

            return redirect("checkout")

        # =========================
        # CREATE ORDER
        # =========================

        with transaction.atomic():

            order = Order.objects.create(

                user=request.user,

                name=name,
                email=email,
                phone=phone,

                address=address,
                city=city,
                pincode=pincode,

                subtotal=subtotal,

                delivery_charge=delivery_charge,

                discount=0,

                total_amount=total,

                status="confirmed"
            )

            # =========================
            # CREATE ORDER ITEMS
            # =========================

            for item in cart_items:

                OrderItem.objects.create(

                    order=order,

                    food=item.food,

                    quantity=item.quantity,

                    price=item.food.price
                )

            # =========================
            # CREATE PAYMENT
            # =========================

            Payment.objects.create(

                order=order,

                payment_method=payment_method,

                amount=total,

                status="pending"
            )

            # =========================
            # CLEAR CART
            # =========================

            cart.items.all().delete()

        # Save order ID in session

        request.session["order_id"] = order.id

        return redirect(
            "order_confirmation"
        )

    return render(
        request,
        "pages/checkout.html",
        {
            "cart_items": cart_items,
            "subtotal": subtotal,
            "delivery_charge": delivery_charge,
            "total": total,
        }
    )


# =========================
# ORDER CONFIRMATION
# =========================

@login_required
def order_confirmation(request):

    order_id = request.session.get(
        "order_id"
    )

    if not order_id:

        return redirect("orders")

    order = get_object_or_404(
        Order,
        id=order_id,
        user=request.user
    )

    order_items = order.items.select_related(
        "food"
    )

    # Remove session after reading

    request.session.pop(
        "order_id",
        None
    )

    return render(
        request,
        "pages/order_confirmation.html",
        {
            "order": order,
            "order_items": order_items,
        }
    )


# =========================
# ORDERS
# =========================

@login_required
def orders(request):

    order_list = Order.objects.filter(
        user=request.user
    ).order_by(
        "-created_at"
    )

    return render(
        request,
        "pages/orders.html",
        {
            "orders": order_list
        }
    )


# =========================
# ORDER DETAIL
# =========================

@login_required
def order_detail(request, order_id):

    order = get_object_or_404(
        Order,
        id=order_id,
        user=request.user
    )

    order_items = order.items.select_related(
        "food"
    )

    return render(
        request,
        "pages/order_detail.html",
        {
            "order": order,
            "order_items": order_items
        }
    )