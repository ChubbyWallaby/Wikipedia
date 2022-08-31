from django.shortcuts import render, redirect
from django import forms
from django.urls import reverse
from markdown import Markdown
from django.contrib import messages
from . import util
from random import choice

class SearchForm(forms.Form):
    title = forms.CharField(label="",widget=forms.TextInput(attrs={
        "class":"search",
        "placeholder": "Search my wiki"
    }))
class CreateForm(forms.Form):
    title = forms.CharField(label="", widget=forms.TextInput(attrs={
        "class":"search",
        "placeholder": "Page Title"
    }))
    text = forms.CharField(label="",widget=forms.Textarea(attrs={
        "placeholder":"Page content in markup language"
    }))
class EditForm(forms.Form):
    text = forms.CharField(label="",widget=forms.Textarea(attrs={
        "placeholder":"Page content in markup language"
    }))



def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries(),
        "SearchForm": SearchForm()
    })
def entry(request,title):

    entry_md = util.get_entry(title)

    if entry_md != None:
        entry_html = Markdown().convert(entry_md)
        return render(request, "encyclopedia/entry.html",{
            "title": title,
            "entry": entry_html,
            "searchform": SearchForm
        })
    else:
        related_titles = util.related_entries(title)
        return render(request, "encyclopedia/search.html",{
            "title": title,
            "related": related_titles,
            "searchForm": SearchForm
        })

def search(request):

    if request.method == "POST":
        form = SearchForm(request.POST)

        if form.is_valid():
            title = form.cleaned_data["title"]
            entry_md = util.get_entry(title)

            if entry_md:
                return redirect(reverse('entry', args=[title]))

            else:
                related_titles = util.related_entries(title)

                return render(request,"encyclopedia/search.html",{
                    "title": title,
                    "related": related_titles,
                    "searchform": SearchForm()
                })
def edit(request,title):
    if request.method == "GET":
        text = util.get_entry(title)

        if not text:
            messages.error(request, f'"{title}" page does not exist and can\'t be edited, please create a new page instead!')

        return render(request, "encyclopedia/edit.html",{
            "title": title,
            "EditForm": EditForm(initial={"text":text}),
            "searchform": SearchForm()
        })

    elif request.method == "POST":
        form = EditForm(request.POST)

    if form.is_valid():
        text = form.cleaned_data['text']
        util.save_entry(title, text)
        return redirect(reverse('entry', args=[title]))

    else:
        return render(request, "encyclopedia/edit.html", {
        "title": title,
        "edit_form": form,
        "search_form": SearchForm()
        })

def create(request):
    """ Lets users create a new page on the wiki """

    # If reached via link, display the form:
    if request.method == "GET":
        return render(request, "encyclopedia/create.html", {
          "create_form": CreateForm(),
          "search_form": SearchForm()
        })

    # Otherwise if reached by form submission:
    elif request.method == "POST":
        form = CreateForm(request.POST)

        # If form is valid, process the form:
        if form.is_valid():
          title = form.cleaned_data['title']
          text = form.cleaned_data['text']
        else:
          messages.error(request, 'Entry form not valid, please try again!')
          return render(request, "encyclopedia/create.html", {
            "create_form": form,
            "search_form": SearchForm()
          })

        # Check that title does not already exist:
        if util.get_entry(title):
            messages.error(request, 'This page title already exists! Please go to that title page and edit it instead!')
            return render(request, "encyclopedia/create.html", {
              "create_form": CreateForm(),
              "search_form": SearchForm()
            })
        # Otherwise save new title file to disk, take user to new page:
        else:
            util.save_entry(title, text)
            messages.success(request, f'New page "{title}" created successfully!')
            return redirect(reverse('entry', args=[title]))

def random (request):
    titles = util.list_entries()
    title = choice(titles)
    return redirect(reverse('entry', args=[title]))