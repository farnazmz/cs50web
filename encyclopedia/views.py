from ast import Try
from cgitb import html
from distutils.log import error
from doctest import IGNORE_EXCEPTION_DETAIL
from encodings import search_function
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

class SearchInput(forms.Form):
    title = forms.CharField(label="", widget=forms.TextInput(attrs={"PlaceHolder":"Title"}))

class CreatePage(forms.Form):
    create_title = forms.CharField(label="", widget=forms.TextInput(attrs={"PlaceHolder":"Create_Title"}))
    create_entry = forms.CharField(widget=forms.Textarea(attrs={"PlaceHolder":"Create_Text Area"}))

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
                                "search_form": form,
                                })             
                else:  
                    similar_data = util.similar(title)
                    if similar_data != None:
                        return render(request,"encyclopedia/entry.html", {
                            "title": title,
                            "error": "   : not found, try below similar pages",
                            "similar_data": similar_data,
                            "search_form": form,
                            }) 
            else:
                entry_md = title
                title_html = Markdown().convert(entry_md)
                return render(request, "encyclopedia/entry.html", {
                            "title": title,
                            "title_html": title_html,  
                            "error": "   :not found, create page",   
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
                    "error": "  already exists, only edit is available",
                    "create_form": form,
                    "search_form": SearchInput()
                })      
            else:
                entry = form.cleaned_data["create_entry"]
                util.save_entry(title, entry)
                entry = util.get_entry(title)
                entry = Markdown().convert(entry)
                return render(request, "encyclopedia/entry.html", {
                    "title": title,
                    "entry": entry,
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
            
            return render(request, "encyclopedia/edit.html", { 
                "title": title,
                "edit_form": EditPage(initial={"entry": entry_md}),
                "search_form": SearchInput()
            })
        else:
            return render(request, "encyclopedia/edit.html", {
                "edit_form": EditPage(title, entry), 
                "search_form": SearchInput
            })

      

def entry(request, title):
    entry_md = util.get_entry(title)
    if entry_md != None:           
        entry_html = Markdown().convert(entry_md)                      
        return render(request, "encyclopedia/entry.html", {
            "title": title,
            "entry":entry_html,
            "search_form": SearchInput(),                
            })
    else: 
        similar_data = util.similar(title)
        if similar_data != None:
            for s in similar_data:
                return render(request, "encyclopedia/entry.html", {
                    "title": title,
                    "error": "   :not found, try below similar pages",
                    "similar_data": similar_data,
                    "s": s,
                    "search_form": SearchInput()
                })
        else:
            return render(request, "encyclopedia/entry.html", {
                "title": title,
                "error": "   :not found, create page",   
                "search_form": SearchInput()
            })







        



        






    

            



