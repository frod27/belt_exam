from django.shortcuts import render, redirect
from django.contrib import messages
from .models import *

def preindex(request):
    return redirect("/main")

def index(request):
    return render(request, "trytryagain/index.html")

def register(request):
    response = User.objects.register(
        request.POST["name"],
        request.POST["username"],
        request.POST["password"],
        request.POST["password_confirm"]
    )
    print (response)
    if response["valid"]:
        request.session["user_id"] = response["user"].id
        return redirect("/landing")
    else:
        for error_message in response["errors"]:
            messages.add_message(request, messages.ERROR, error_message)
        return redirect("/main")

def login(request):
    response = User.objects.login(
        request.POST["username"],
        request.POST["password"]
    )
    if response["valid"]:
        request.session["user_id"] = response["user"].id
        return redirect("/landing")
    else:
        for error_message in response["errors"]:
            messages.add_message(request, messages.ERROR, error_message)
        return redirect("/main")

def landing(request):
    if "user_id" not in request.session:
        return redirect("/main")

    context = {
        "user": User.objects.get(id = request.session["user_id"]),
        "users": User.objects.all().exclude(id = request.session["user_id"]),
        "my_landing": Item.objects.all().filter(wish_user = User.objects.get(id = request.session["user_id"])),
        "all_landings": Item.objects.all().exclude(wish_user = User.objects.get(id = request.session["user_id"]))
    }
    return render(request, "trytryagain/dashboard.html", context)

def logout(request):
    request.session.clear()
    return redirect("/main")

def join(request, id):
    response = Item.objects.joinItem(id, request.session['user_id'])
    if response['valid']:
        messages.add_message(request, messages.SUCCESS, "Added item to wish list")
    else:
        for error_message in response['errors']:
            messages.add_message(request, messages.ERROR, error_message)
    return redirect('/landing')

def remove(request, id):
    response = Item.objects.removeItem(id, request.session['user_id'])
    if response['valid']:
        messages.add_message(request, messages.SUCCESS, "Removed item from wish list")
    else:
        for error_message in response['errors']:
            messages.add_message(request, messages.ERROR, error_message)
    return redirect('/landing')

def add(request):
    return render(request, 'trytryagain/create.html')

def addItem(request):
    response = Item.objects.addItem(
        request.POST["name"],
        # request.POST["creator"],
        request.session["user_id"],
        )

    if response["valid"]:
        messages.add_message(request, messages.SUCCESS, "Your item has been added!")
        return redirect("/landing")
    else:
        for error_message in response["errors"]:
            messages.add_message(request, messages.ERROR, error_message)
        return redirect("landing/add")

def item(request, id):
    print("In items")
    context = {
        "Items": Item.objects.get(id = id),
        "joined": Item.objects.get(id = id).wish_user.all().exclude(id = Item.objects.get(id = id).creator.id)
    }
    return render(request, "trytryagain/item.html", context)