from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from django.urls import reverse
import markdown2
from . import util
from django import forms


class NewEntryForm(forms.Form):
    title = forms.CharField(max_length=10, required=True, label="Title")
    new_entry = forms.CharField(
        max_length=500, required=True, label="New Entry")


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

    results = util.partial_search(title, entries)

    return render(request, "encyclopedia/search_results.html",
                  {"title": title, "content": results})


def new(request):
    if request.method == "POST":
        form = NewEntryForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data["title"]
            content = form.cleaned_data["entry"]
            if content:
                util.save_entry(title, content)
