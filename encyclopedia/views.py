from django.shortcuts import render
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
