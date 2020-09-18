from django.shortcuts import redirect,render
from django.http import HttpResponseRedirect
from django.urls import reverse

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

def search(request):
    res = request.GET.get('q').strip()
    if res.lower() in map(str.lower, util.list_entries()):
        return HttpResponseRedirect(reverse("displayEntry", args=[res]))
    else:
        return render(request,"encyclopedia/search.html",{
                "results": util.search(res),
                "search_term": res
        })

# def search(request):
#     q = request.GET.get('q').strip()
#     if q in util.list_entries():
#         return redirect("displayEntry", title=q)
#     return render(request, "encyclopedia/search.html", {"entries": util.search(q), "q": q})
