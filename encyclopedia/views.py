from ast import Try
from cgitb import html
from distutils.log import error
from doctest import IGNORE_EXCEPTION_DETAIL
from encodings import search_function
from html import entities
from logging import PlaceHolder
from pickle import GET, NONE
from re import M
import re
from tkinter.tix import Form
from turtle import title
from urllib import response
from xml.dom.minidom import Attr
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect, render
from flask import render_template, request
from . import util
from .views import redirect
import markdown2
from markdown2 import Markdown
from django import forms
import encyclopedia
from django.urls import reverse, path
from django.views.generic.base import RedirectView
from django.http import Http404
import random

class SearchInput(forms.Form):
    title = forms.CharField(label="", widget=forms.TextInput(attrs={"PlaceHolder":"Title"}))

class CreatePage(forms.Form):
    create_title = forms.CharField(label="", widget=forms.TextInput(attrs={"PlaceHolder":"Title"}))
    create_entry = forms.CharField(label="", widget=forms.Textarea(attrs={"PlaceHolder":"Create Markdown Format: Title/Text Area"}))

class EditPage(forms.Form):
    entry = forms.CharField(widget=forms.Textarea(attrs={"PlaceHolder": "Edit Page"}), required=True)

def index(request):
    entries = util.list_entries()
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries(),
        "search_form": SearchInput()
        })

def search(request):
    if request.method == "GET":
        form = SearchInput(request.GET)
        if form.is_valid():
            title = form.cleaned_data["title"]
            list_entries = util.list_entries()
            search_results = [entry.lower() for entry in list_entries if title.lower() in entry.lower() or entry.lower() in title.lower()] 
            for i in search_results:      
                if title.lower() in search_results:
                    entry = util.get_entry(title)
                    entry = Markdown().convert(entry)
                    return render(request,"encyclopedia/entry.html", {
                                "title": title,
                                "entry": entry,
                                "edit": "edit",
                                "search_form": form,
                                })             
                else:  
                    similar_data = util.similar(title)
                    if similar_data != None:
                        return render(request,"encyclopedia/entry.html", {
                            "title": title,
                            "error": "Title Not Found, Similar Results",
                            "edit": "",
                            "create": "create",
                            "similar_data": similar_data,
                            "search_form": form,
                            }) 
            else:
                entry_md = title
                title_html = Markdown().convert(entry_md)
                return render(request, "encyclopedia/entry.html", {
                            "title": title,
                            "title_html": title_html,  
                            "edit": "",
                             "create": "create",
                            "error": "Title Not Found, Create Only",   
                            "search_form": form
                        })           
        else: 
            return render(request, "encyclopedia/index.html", {
                    "search_form": form
                })
    else:
        return render(request, "encyclopedia/index.html", {
            "search_form": form
        })

def create(request):
    if request.method == "POST":
        form = CreatePage(request.POST)
        if form.is_valid():
            title = form.cleaned_data["create_title"]
            entry = util.get_entry(title)
            if entry != None:
                entry = Markdown().convert(entry)
                return render(request, "encyclopedia/entry.html", {
                    "title": title,
                    "entry": entry,
                    "error": "  Title Exists, Edit Only",
                    "create_form": form,
                    "search_form": SearchInput(),
                    "edit": "edit",
                    "create": ""
                })      
            else:
                entry = form.cleaned_data["create_entry"]
                util.save_entry(title, entry)
                entry = util.get_entry(title)
                entry = Markdown().convert(entry)
                title_html = Markdown().convert(title)
                return render(request, "encyclopedia/entry.html", {
                    "title_html": title_html,
                    "title": title,
                    "entry": entry,
                    "edit": "",
                    "edit": "edit",
                    "search_form": SearchInput(),
                    "create_form": form
                 })
    else: 
        return render(request, "encyclopedia/create.html", {
            "create_form": CreatePage(),
            "search_form": SearchInput()   
        }) 

def edit(request, title):
    if request.method == "POST":
        form = EditPage(request.POST)
        if form.is_valid():
            entry = form.cleaned_data["entry"]
            util.save_entry(title, entry)
            entry = Markdown().convert(entry)     
            return HttpResponseRedirect(reverse('entry', args=[title]))
        else:
            return render(request, "encyclopedia/edit.html", {
                "edit_form": EditPage(title, entry), 
                "search_form": SearchInput
            })
    else:
        entry_md = util.get_entry(title)
        if entry_md != None:
            entry = entry_md
            return render(request, "encyclopedia/edit.html", { 
                "title": title,
                "edit_form": EditPage(initial={"entry": entry}),
                "search_form": SearchInput()
            })

def random_page(request):
    entries = util.list_entries()
    title = random.choice(entries)
    entry_md = util.get_entry(title)
    entry = Markdown().convert(entry_md)
    return render(request, "encyclopedia/entry.html", {
            "title": title,
            "entry":entry,
            "search_form": SearchInput(),   
             "edit": "edit", 
            "create": ""               
            })
       
def entry(request, title):
    entry_md = util.get_entry(title)
    if entry_md != None:           
        entry_html = Markdown().convert(entry_md)
        title_html = Markdown().convert(title)                      
        return render(request, "encyclopedia/entry.html", {
            "title_html": title_html,
            "title": title,
            "entry":entry_html,
            "search_form": SearchInput(),  
            "edit": "edit", 
            "create": ""             
            })
    else: 
        similar_data = util.similar(title)
        if similar_data != None:
            for s in similar_data:
                return render(request, "encyclopedia/entry.html", {
                    "title": title,
                    "error": "Title Not Found, Similar Results:",
                    "similar_data": similar_data,
                    "s": s,
                    "edit": "",
                    "create": "create",
                    "search_form": SearchInput()
                })
        else:
            return render(request, "encyclopedia/entry.html", {
                "title": title,
                "error": "Title Not Found, Create Only",
                "edit": "",  
                "create": "create", 
                "search_form": SearchInput()
            })
