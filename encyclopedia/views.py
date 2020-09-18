from django.shortcuts import render

from . import util
import markdown2

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

