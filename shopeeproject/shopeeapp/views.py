from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from .models import Product, Cart, Order


# Create your views here.


def index(req):
    allproducts = Product.objects.all()
    context = {"allproducts": allproducts}
    return render(req, "index.html", context)


def about(req):
    return render(req, "about.html")


def contact(req):
    return render(req, "contact.html")


def buy(req):
    return render(req, "buy.html")


def signup(req):
    if req.method == "POST":
        uname = req.POST["uname"]
        upass = req.POST["upass"]
        ucpass = req.POST["ucpass"]
        context = {}

        if uname == "" or upass == "" or ucpass == "":
            context["errmsg"] = "Field can't be empty"
            return render(req, "signup.html", context)
        elif upass != ucpass:
            context["errmsg"] = "Password and confirm password doesn't match"
            return render(req, "signup.html", context)
        else:
            try:
                userdata = User.objects.create(username=uname, password=upass)
                userdata.set_password(upass)
                userdata.save()
                return redirect("/signin")
            except:
                context["errmsg"] = "User Already exists"
                return render(req, "signup.html", context)
    else:
        context = {}
        context["errmsg"] = ""
        return render(req, "signup.html", context)


from django.contrib.auth import authenticate, login, logout


def signin(req):
    if req.method == "POST":
        uname = req.POST["uname"]
        upass = req.POST["upass"]
        context = {}
        if uname == "" or upass == "":
            context["errmsg"] = "Field can't be empty"
            return render(req, "signin.html", context)
        else:
            userdata = authenticate(username=uname, password=upass)
            if userdata is not None:
                login(req, userdata)
                return redirect("/")
            else:
                context["errmsg"] = "Invalid username and password"
                return render(req, "signin.html", context)
    else:
        return render(req, "signin.html")


def userlogout(req):
    logout(req)
    return redirect("/")


def mobilelist(req):
    if req.method == "GET":
        allproducts = Product.productmanager.mobile_list()
        context = {"allproducts": allproducts}
        return render(req, "index.html", context)
    else:
        allproducts = Product.objects.all()
        context = {"allproducts": allproducts}
        return render(req, "index.html", context)


def shoeslist(req):
    if req.method == "GET":
        allproducts = Product.productmanager.shoes_list()
        context = {"allproducts": allproducts}
        return render(req, "index.html", context)
    else:
        allproducts = Product.objects.all()
        context = {"allproducts": allproducts}
        return render(req, "index.html", context)


def clothlist(req):
    if req.method == "GET":
        allproducts = Product.productmanager.cloth_list()
        context = {"allproducts": allproducts}
        return render(req, "index.html", context)
    else:
        allproducts = Product.objects.all()
        context = {"allproducts": allproducts}
        return render(req, "index.html", context)


def electronicslist(req):
    if req.method == "GET":
        allproducts = Product.productmanager.electronics_list()
        context = {"allproducts": allproducts}
        return render(req, "index.html", context)
    else:
        allproducts = Product.objects.all()
        context = {"allproducts": allproducts}
        return render(req, "index.html", context)


def pricerangeview(req):
    if req.method == "GET":
        return render(req, "index.html")
    else:
        r1 = req.POST.get("min")
        r2 = req.POST.get("max")
        if r1 is not None and r2 is not None and r1.isdigit() and r2.isdigit():
            allproducts = Product.productmanager.getpricerange(r1, r2)
            context = {"allproducts": allproducts}
            return render(req, "index.html", context)
        else:
            allproducts = Product.objects.all()
            context = {"allproducts": allproducts}
            return render(req, "index.html", context)


def allsortedproducts(req):
    sortoption = req.GET.get("sort")
    if sortoption == "high_to_low":
        allproducts = Product.objects.order_by("-price")  # desc order
    elif sortoption == "low_to_high":
        allproducts = Product.objects.order_by("price")  # asc order
    else:
        allproducts = Product.objects.all()

    context = {"allproducts": allproducts}
    return render(req, "index.html", context)


from django.db.models import Q


def searchproduct(req):
    query = req.GET.get("q")
    errmsg = ""
    if query:
        allproducts = Product.objects.filter(
            Q(productname__icontains=query)
            | Q(category__icontains=query)
            | Q(desc__icontains=query)
            | Q(price__icontains=query)
        )

        if len(allproducts) == 0:
            errmsg = "NO result Found"
    else:
        allproducts = Product.objects.all()

    context = {"allproducts": allproducts, "query": query, "errmsg": errmsg}
    return render(req, "index.html", context)


def showcarts(req):
    allcarts = Cart.objects.all()
    print(allcarts)
    context = {"allcarts": allcarts}
    return render(req, "showcarts.html", context)


def addtocart(req, productid):
    allproducts = get_object_or_404(Product, productid=productid)
    cartitem, created = Cart.objects.get_or_create(productid=allproducts)
    if not created:
        cartitem.qty += 1
    else:
        cartitem.qty = 1
    cartitem.save()
    return redirect("/showcarts")


def removecart(req, productid):
    cartitem = Cart.objects.filter(productid=productid)
    cartitem.delete()
    return redirect("/showcarts")


def updateqty(req, qv, productid):
    allcarts = Cart.objects.filter(productid=productid)
    if qv == 1:
        total = allcarts[0].qty + 1
        allcarts.update(qty=total)
    else:
        if allcarts[0].qty > 1:
            total = allcarts[0].qty - 1
            allcarts.update(qty=total)
        else:
            allcarts = Cart.objects.filter(productid=productid)
            allcarts.delete()

    return redirect("/showcarts")





def buy(req):
    return render(req, "buy.html")