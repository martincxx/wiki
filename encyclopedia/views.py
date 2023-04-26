from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from django.urls import reverse
import markdown2
from . import util
from django import forms
from django.contrib import messages
from random import randint


class EntryForm(forms.Form):
    title = forms.CharField(max_length=10, required=True, label="Title")
    new_entry = forms.CharField(
        widget=forms.Textarea(attrs={"rows": "10"}), required=True, label="New Entry")


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })


def entry_page(request, title):
    entry = util.get_entry(title)
    if (entry is None):
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
    title, content = None, None

    if request.method == "POST":
        form = EntryForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data["title"]
            content = form.cleaned_data["new_entry"]
            if title not in util.list_entries():
                util.save_entry(title, content)
                return HttpResponseRedirect(reverse("entry_page", kwargs={"title": title}))
            else:
                messages.info(request, "That entry already exists!")
                return render(request, "encyclopedia/new_page.html", {"form": EntryForm()})

    return render(request, "encyclopedia/new_page.html", {
        "form": EntryForm()
    })


def edit(request):
    if request.method == "GET":
        title = request.GET.get("edit", None)
        current_content = util.get_entry(title)
        form = EntryForm({"title": title, "new_entry": current_content})
        return render(request, "encyclopedia/edit_page.html", {"form": form})


def save_entry(request):
    if request.method == "POST":
        form = EntryForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data["title"]
            content = form.cleaned_data["new_entry"]
            util.save_entry(title, content)
            return HttpResponseRedirect(reverse("entry_page", kwargs={"title": title}))


def random_entry(request):
    if request.method == "GET":
        all_entries = util.list_entries()
        random_title = all_entries.__getitem__(
            randint(0, len(all_entries) - 1))
        return HttpResponseRedirect(reverse("entry_page", kwargs={"title": random_title}))
