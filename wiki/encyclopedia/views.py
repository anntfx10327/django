from django.shortcuts import render
from markdown2 import Markdown
from . import util
from .forms import SearchesForm, NewPageForm
import random

def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries(),
        "forms" : SearchesForm()
    })

def entry(request, title):
    ut = util.get_entry(title)
    if ut != None:
        markdowner = Markdown()
        tit = markdowner.convert(ut)
        return render(request, "encyclopedia/entry.html",{
            "title" : title,
            "entry" : tit,
            "forms" : SearchesForm()
        })
    else:
        return render(request, "encyclopedia/error.html")


def searches(request):
    # keyword = request.POST
    # if keyword["keywork"] in util.list_entries():
    #     return entry(request, keyword["keywork"])
    # return index(request)
    sear_list = []
    if request.method == "POST":
        form = SearchesForm(request.POST)
        if form.is_valid():
            keywork = form.cleaned_data["keywork"]
            if keywork in util.list_entries():
                return entry(request, keywork)
            for i in util.list_entries():
                if keywork.lower() in i.lower():
                    sear_list.append(i)
            return render(request, "encyclopedia/index.html", {
                "entries": sear_list,
                "forms" : SearchesForm()
            })
    return index(request)


def newpage(request):
    if request.method == "POST":
        form_new = NewPageForm(request.POST)
        if form_new.is_valid():
            title = form_new.cleaned_data["title"]
            dcument = form_new.cleaned_data["dcument"]
            if title in util.list_entries():
                return render(request, "encyclopedia/error.html")
            util.save_entry(title, dcument)
            return entry(request, title)

    return render(request, "encyclopedia/newpage.html", {
        "formnew": NewPageForm(),        
    })


def editpage(request, title):
    if request.method == "GET":
        ut = util.get_entry(title)
        return render(request, "encyclopedia/editpage.html",{
        "formnew" : NewPageForm(initial={'title':title, 'dcument':ut}),
        "title": title
    })
    else:
        form_new = NewPageForm(request.POST)
        if form_new.is_valid():
            title = form_new.cleaned_data["title"]
            dcument = form_new.cleaned_data["dcument"]
            util.save_entry(title, dcument)
            return entry(request, title)

def randompage(request):
    title = random.choice(util.list_entries())
    return entry(request, title)