from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.forms import ModelForm
from django import forms
from decimal import Decimal
import datetime

from .models import User, Auction, Oferta, Category, Comentario


def index(request):

    # el filtro es como el where de sql
    # ver cómo ordenar un resultado, el signo - lo ordena en forma inversa
    auctions = Auction.objects.filter(condition="active").order_by('posted_date')
    return render(request, "auctions/index.html", {"auctions": auctions })


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")


@login_required
def publish(request):

    class AuctionForm(ModelForm):

        class Meta:
            model = Auction
            fields = ['title','description','starting_bid','category','image_url']

    if request.method == "GET":
            
        form = AuctionForm()

        return render(request, "auctions/publish.html", {"formulario": form})

    if request.method == "POST":

        formulario = AuctionForm(request.POST)

        if formulario.is_valid():

            publicacion=Auction(title=formulario.cleaned_data["title"],
            description=formulario.cleaned_data["description"],
            starting_bid=formulario.cleaned_data["starting_bid"],
            maxim_bid=formulario.cleaned_data["starting_bid"],
            category=formulario.cleaned_data["category"],
            image_url=formulario.cleaned_data["image_url"],
            condition='active',
            posted_by=request.user)

            publicacion.save()

        return HttpResponseRedirect(reverse("index"))


def oferta(request, numero):

    auction = Auction.objects.get(id=numero)

    class Makebid(forms.Form):

        bid = forms.DecimalField ( widget= forms.NumberInput,
                                   required="True",
                                   label=False,
                                   max_digits=6,
                                   decimal_places=2,
                                   min_value= (auction.maxim_bid + Decimal(0.01)))

    class Makecomment(forms.Form):

        comment = forms.CharField ( widget=forms.Textarea(attrs={'rows':2, 'cols':104}),
                                    required="True",
                                    label=False,
                                    max_length=640)


    # ofertas ordenadas con las más recientes primero, el valor entre corchetes limita la cantidad
    # de filas devueltas
    bidhistory = Oferta.objects.filter(oferta=auction).order_by('-posted_date').order_by('-bid')[:6]

    if request.method == "POST":

        if request.POST.get('form_type') == "remove":
            auction.followed_by.remove(request.user)
            auction.save()

        if request.POST.get('form_type') == "add":
            auction.followed_by.add(request.user)
            auction.save()

        if request.POST.get('form_type') == "bid":

           auction.maxim_bid = request.POST.get('bid')
           auction.won_by = request.user
           auction.save()

           oferta=Oferta(oferta=auction,offeror=request.user,bid=request.POST.get('bid'))
           oferta.save()

        if request.POST.get('form_type') == "comment":

            comment=Comentario(said_by=request.user,
                               auction=auction,
                               comment=request.POST.get('comment'))

            comment.save()

        # close auction 
        if request.POST.get('form_type') == 'close':
            auction.condition = 'inactive'
            auction.save()
        
 # comentarios ordenados por los más recientes primero, el valor entre corchetes 
 # limita la cantidad de filas devueltas
    commenthistory = Comentario.objects.filter(auction=auction).order_by('-posted_date')[:8]


    return render(request, "auctions/auction.html", {"auction": auction, 
                                                     "formbid": Makebid(),
                                                     "bidhistory": bidhistory,
                                                     "formcomments": Makecomment(),
                                                     "commenthistory":commenthistory })


def categories(request):

    # traigo los id de las categorías "activas", es decir las que hay artículos publicados
    active_categories = Auction.objects.values('category').filter(condition="active").distinct()

    #busco la descripción para las categorías que obtuve en el paso anterior
    categories =  Category.objects.filter(pk__in=active_categories).order_by('description')

    return render(request, "auctions/categories.html", {"categories": categories })


def categoryselected(request, category):

    # busco la clave para poder buscar las ofertas, ya que Auction tiene el id.
    # ¡ver si hay otra forma más directa!

    clave = Category.objects.get(description=category)

    auctions = Auction.objects.filter(category=clave.id).filter(condition="active")

    return render(request, "auctions/index.html", {"auctions": auctions })


@login_required
def watchlist(request):

    auctions = Auction.objects.filter(followed_by=request.user).filter(condition="active").order_by('-posted_date')
    return render(request, "auctions/index.html", {"auctions": auctions })



    





        



