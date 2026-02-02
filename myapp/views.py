from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login, authenticate
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.http import HttpResponse, HttpResponseNotFound
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout as auth_logout
from .models import Addproduct, Addcart, Payment, Wishlist


def index(request):
    men = Addproduct.objects.filter(category="Men")
    women = Addproduct.objects.filter(category="Women")
    kids = Addproduct.objects.filter(category="Kids")

    if request.user.is_authenticated:
        username = request.user.username
        data = Addcart.objects.filter(username=username)
        context = {
            "women": women,
            "men": men,
            "Kids": kids,
            "number": len(data),
        }
    else:
        context = {
            "women": women,
            "men": men,
            "Kids": kids,
        }

    return render(request, "myapp/index.html", context)



def sign(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]
        password = request.POST["password"]
        confirmpassword = request.POST["confirmpassword"]

        if User.objects.filter(username=username).exists():
            return render(request, "signup.html", {"msg": "Username already taken"})

        if User.objects.filter(email=email).exists():
            return render(request, "signup.html", {"msg": "Email already registered"})

        if password != confirmpassword:
            return render(request, "signup.html", {"msg": "Passwords do not match"})

        user = User.objects.create_user(username=username, email=email, password=password)
        user.save()

        subject = "🎉 Welcome to Hexacloth!"
        msg = "Your account has been created successfully!"
        send_mail(subject, msg, "Himanshu393700@gamil.com", [email])

        return render(request, "login.html", {"msg": "Account created successfully"})

    else:
        form = UserCreationForm()
        return render(request, "signup.html", {"form": form})

def submit(request):
    return sign(request)  # Avoid duplicate logic


def log(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect("/")
        else:
            return render(request, "login.html", {"msg": "Invalid credentials"})
    else:
        return render(request, "login.html")

def logout(request):
    auth_logout(request)
    return redirect('/')

def adm(request):
    arr = ["Admin2005"]
    if request.method == "POST":
        username = request.POST["username"]
        if username in arr:
            return redirect("/dash")
        else:
            return render(request, "admin.html", {"msg": "Password not matched"})
    return render(request, "admin.html")


def abt(request):
    return render(request, "about.html")


def pro(request):
    return render(request, "products.html")


@login_required(login_url='/log')
def order(request, id):
    username = request.user.username
    data = Addcart.objects.filter(username=username)
    product = Addproduct.objects.get(id=id)
    return render(request, "single-product.html", {"data": product, "number": len(data)})


def dash(request):
    products = Addproduct.objects.all()
    orders = Payment.objects.all()
    total_amount = sum(int(order.amount) for order in orders)
    return render(request, "dashboard.html", {
        "totalamount": total_amount,
        "totalproduct": len(products),
        "totalorder": len(orders)
    })


def add(request):
    if request.method == "POST":
        product = Addproduct(
            product_name=request.POST["product_name"],
            product_description=request.POST["product_description"],
            product_price=request.POST["product_price"],
            product_offerprice=request.POST["product_offerprice"],
            category=request.POST["category"],
            image=request.FILES["image"]
        )
        product.save()
        return redirect("/view")
    return render(request, "add_product.html")


def view(request):
    data = Addproduct.objects.all()
    return render(request, 'view_product.html', {"data": data})


def delete_product(request, id):
    Addproduct.objects.get(id=id).delete()
    return redirect("/view")


def edit(request, id):
    ch = Addproduct.objects.get(id=id)
    if request.method == "POST":
        ch.product_name = request.POST['product_name']
        ch.product_description = request.POST['product_description']
        ch.product_price = request.POST['product_price']
        ch.product_offerprice = request.POST['product_offerprice']
        ch.save()
        return redirect("/view")
    return render(request, "add_product.html", {"data": ch})


@login_required(login_url='/log')
def cart(request, id):
    if request.method == "POST":
        username = request.user.username
        quantity = request.POST["quantity"]
        product = Addproduct.objects.get(id=id)
        total = int(product.product_offerprice) * int(quantity)
        Addcart.objects.create(
            producti_id=id,
            producti_name=product.product_name,
            producti_price=product.product_offerprice,
            producti_category=product.category,
            image=product.image,
            producti_qty=quantity,
            totalprice=total,
            username=username
        )
    return redirect("/bag")


def delete_cart_item(request, id):
    try:
        Addcart.objects.get(id=id).delete()
    except Addcart.DoesNotExist:
        return HttpResponseNotFound("Cart item not found.")
    return redirect("/bag")


@login_required(login_url='/log')
def placeorder(request):
    username = request.user.username
    cart_items = Addcart.objects.filter(username=username)
    total = sum(int(item.totalprice) for item in cart_items)
    unique_products = list(set(item.producti_name for item in cart_items))

    if request.method == "POST":
        order = Payment(
            firstname=request.POST.get("firstname"),
            lastname=request.POST.get("lastname"),
            email=request.POST.get("email"),
            phone=request.POST.get("phone"),
            address=request.POST.get("address"),
            payment_mode=request.POST.get("payment_mode"),
            product=unique_products,
            amount=total
        )
        order.save()
        return redirect("/page")
    return render(request, "payment.html", {"total": total, "pro": unique_products})


def delete(request, id):
    try:
        Addcart.objects.get(id=id).delete()
    except Addcart.DoesNotExist:
        return HttpResponseNotFound("Cart item not found.")
    return redirect("/bag")


def mng(request, id):
    return HttpResponse(f"Managing ID: {id}")
def bag(request):
    if request.user.is_authenticated:
        username = request.user.username
        data = Addcart.objects.filter(username=username)
        total = sum(int(item.totalprice) for item in data)
        return render(request, "bag.html", {"data": data, "total": total, "number": len(data)})
    else:
        return redirect("/log")

def page(request):
    return render(request, "page.html")

def wish(request, id):
    if request.user.is_authenticated:
        username = request.user.username
        product = Addproduct.objects.get(id=id)
        Wishlist.objects.create(product_id=id, product_name=product.product_name, product_price=product.product_offerprice, product_image=product.image, username=username)
        return redirect("/")
    else:
        return redirect("/log")

def showwish(request):
    if request.user.is_authenticated:
        username = request.user.username
        data = Wishlist.objects.filter(username=username)
        return render(request, "wishlist.html", {"wish": data})
    else:
        return redirect("/log")
    
def delete2(request, id):
    try:
        Wishlist.objects.get(id=id).delete()
    except Wishlist.DoesNotExist:
        return HttpResponseNotFound("Wishlist item not found.")
    return redirect("/showwishlist")
