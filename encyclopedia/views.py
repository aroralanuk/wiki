from django.shortcuts import redirect,render
from django.http import HttpResponseRedirect
from django.urls import reverse
from django import forms

from . import util
import markdown2
import random

class newEntryForm(forms.Form):
    newTitle = forms.CharField(widget=forms.TextInput(attrs={'size': '60'}),label="Title")
    newBody = forms.CharField(widget=forms.Textarea(attrs={'rows':'5', 'cols':'20','style':'height: 30em'}),label="Content")
    

def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def displayEntry(request, title):
    md = util.get_entry(title)
    if not md:
        return render(request,"encyclopedia/error.html")
    else:
        return render(request,"encyclopedia/entry.html",{
            "title":title,
            "body": markdown2.markdown(md)
        })

def search(request):
    res = request.GET['q']
    if res.lower() in map(str.lower, util.list_entries()):
        return HttpResponseRedirect(reverse("displayEntry", args=[res]))
    else:
        return render(request,"encyclopedia/search.html",{
                "results": util.search_entries(res),
                "search_term": res
        })

def create(request):
    newEntry = newEntryForm(request.POST)
    if request.method == 'POST' and newEntry.is_valid():
        title = newEntry.cleaned_data['newTitle']
        content = newEntry.cleaned_data['newBody']
        if title.lower() in map(str.lower, util.list_entries()):
            return render(request,"encyclopedia/create.html",{
                "form": newEntryForm(),
                "alert": "Duplicate title. Try again."
            })
        util.save_entry(title,content)
        return HttpResponseRedirect(reverse("displayEntry",args=[title]))
    return render(request,"encyclopedia/create.html",{
        "form": newEntryForm()
    })

def edit(request, title):
    old = util.get_entry(title)
    if old == None:
        return render(request, "encyclopedia/error.html")
    if request.method == 'POST':
        content = request.POST['newContent']
        if content == "":
            return render(request, "encyclopedia/edit.html", {
                "alert": "Content can't be empty.", 
                "title": title, 
                "content": old})
        util.save_entry(title, content)
        return HttpResponseRedirect(reverse("displayEntry",args=[title]))
    return render(request,"encyclopedia/edit.html",{
        "content": old,
        "title": title
    })

def random_page(request):
    random.seed()
    rando = random.choice(util.list_entries())
    return HttpResponseRedirect(reverse("displayEntry",args=[rando]))

