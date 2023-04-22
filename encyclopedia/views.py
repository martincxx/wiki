from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from django.urls import reverse
import markdown2
from . import util


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })


def entry_page(request, title):
    entry = util.get_entry(title)
    if (entry == None):
        title += " - not found!"
        html_content = "404 - Not found!"
    else:
        html_content = markdown2.markdown(entry)
    return render(request, "encyclopedia/entry.html", {"title": title, "content": html_content})


def search(request):
    title = request.GET.get("q", None)
    entries = util.list_entries()
    if title in entries:
        return HttpResponseRedirect(reverse("entry_page", kwargs={"title": title}))

    not_found = """
    <h1>Search results</h1>
    <p>//TODO</p>"""

    return render(request, "encyclopedia/search_results.html",
                  {"title": title, "content": not_found})
