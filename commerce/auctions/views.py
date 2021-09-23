from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.db.models.aggregates import Count
from django.http import HttpResponse, HttpResponseRedirect, request
from django.shortcuts import redirect, render
from django.urls import reverse
from django.views.generic import ListView, DetailView, TemplateView
from django.views.generic.edit import CreateView, UpdateView, DeleteView, FormMixin
from .forms import *
from .models import *


def index(request):
    return render(request, "auctions/index.html",{
        "listac": Action.objects.all()
    })

# class ActionList(TemplateView):
#     template_name = "auctions/action_list.html"

#     def get_context_data(self, pk, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context["aclist"] = Action.objects.get(id=pk)
#         context["form"] = BidForm
#         return context
    

# class BidCreate(CreateView):
#     model = Bid
#     template_name = "auctions/bid_create.html"
#     form_class = BidForm
#     success_url = "/action" 

class DetailsView(DetailView):
    model = Action
    template_name = "auctions/action_list.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form"] = BidForm
        return context

    def post(self, request, pk):
        user = User.objects.get(username=request.user)
        listing = Action.objects.get(id=pk)
        if request.POST.get("wlbutton") == "Watchlist":
            wl = Wish()
            if not Wish.objects.filter(id=pk):
                wl.user = user
                wl.listing_id = pk
                wl.save()
            else:
                Wish.objects.get(id=pk).delete()
            return HttpResponseRedirect(reverse('actionlist', args=(pk,)))


        if not listing.is_closed:
            if request.POST.get("button") == "Close":
                listing.is_closed = True 
                listing.save()
            else:
                p = request.POST["price"]
                if float(p) <= listing.price:
                    return render(request, self.template_name, {
                        "action": listing,
                        "form" : BidForm,
                        "mess" : "ERROR!"
                    })
                listing.price = p
                listing.save()
        return render(request, self.template_name, {
            "action": listing,
            "form" : BidForm
        })


class ActionCreate(CreateView):
    model = Action
    form_class = ActionForm
    template_name = "auctions/action_create_form.html"
    success_url = "/"

class CategoryList(ListView):
    model = Category
    template_name = "auctions/category_list.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["categorylist"] = Action.objects.all().values_list("category", flat=True).distinct()
        return context

        

class CategoryTemp(TemplateView):
    template_name = "auctions/category_temp.html"

    def get_context_data(self, category, **kwargs):
        context = super().get_context_data(**kwargs)
        context["categorylist"] = Action.objects.filter(category=category)
        return context
    
    # def post(self, request, temp):
        # l = Action.objects.filter(category=temp)

class WiskList(ListView):
    model = Wish

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        list_ids = Wish.objects.values_list("listing_id", flat=True)
        wisks = Action.objects.filter(pk__in=list_ids)
        context["wish"] = wisks
        return context
    # def post(request):
    #     users = Wish.objects.filter(user=request.user)
    #     list_ids = Wish.objects.values_list("listing_id", flat=True)
    #     wid = Action.objects.filter(id=1)
    #     return render(request, "actions/wish_list.html", {
    #         "wid" : wid,
    #         "user" : request.user
    #     })



# class CategoryCreate(CreateView):
#     model = Category
#     form_class = CategoryForm
#     template_name = "auctions/category_create_form.html"
#     success_url = "/"

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
