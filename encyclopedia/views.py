from ast import Try
from cgitb import html
from distutils.log import error
from encodings import search_function
from logging import PlaceHolder
from pickle import NONE
from re import M
import re
from tkinter.tix import Form
from turtle import title
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
    title = forms.CharField(widget=forms.TextInput(attrs={"PlaceHolder":"Search"}))

def index(request):
    entries = util.list_entries()
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries(),
        "form": SearchInput()
        })

def search(request):
    if request.method == "GET":
            form = SearchInput(request.GET)
            if form.is_valid():
                list_entries = util.list_entries()
                title = form.cleaned_data["title"]
                search_results = [entry.lower() for entry in list_entries if title.lower() in entry.lower()]      
                for i in search_results:           
                    if title.lower() in search_results:
                        entry_input = util.get_entry(title)
                        input_html = Markdown().convert(entry_input)
                        return render(request,"encyclopedia/entry.html", {
                            "entry_html":input_html,
                            "form": form
                            }) 
                    else:
                        return
                list_entries = title 
                search_results = list_entries
                i = search_results
                title = i
                return render(request,"encyclopedia/entry.html", {     
                    "title": title, 
                    "form": form
                    }) 
            else:
                return render(request, "encyclopedia/index.html", {
                    "form": form
                })
    else: 
        return render(request, "encyclopedia/index.html", {
                    "form": form
                })

def entry(request, title):
    entry_input = util.get_entry(title)
    if entry_input != None:
        entry_html = Markdown().convert(entry_input)
        return render(request, "encyclopedia/entry.html", {
            "title": title,
            "entry_html":entry_html,
            "form": SearchInput()
        })
    else:
        entry_input = title
        entry_html = Markdown().convert(entry_input)
        return render(request, "encyclopedia/entry.html", {
            "title": title,
            "form": SearchInput()
        })

def similar():
    form = SearchInput(request.GET)
    title = form.cleaned_data["title"]
    list_entries = util.list_entries()
    for i in range(len(list_entries), -1, -1):
        for j in range(len(title), -1, -1):
            if list_entries[i: -1] == title[j: -1]:
                similar_results = [k.lower() for k in list_entries]
                for m in similar_results:
                    similar_results[0] = m
                    m_html = Markdown().convert(m)
                    return render(request,"encyclopedia/entry.html", {
                            "entry":m_html,
                            "form": form
                            })
                    


        



        






    

            



