from django.shortcuts import render
from . import util
import markdown2
from markdown2 import Markdown



def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def entry(request, title):
    get_title_md = util.get_entry(title)

    if get_title_md == None:
        return render(request, "encyclopedia/error.html"), {
            "title": get_title_md
        }

    else:
        markdowner = Markdown()
        get_title_html = markdowner.convert(get_title_md)
        return render(request, "encyclopedia/entry.html", {
            "title": title,
            "entry": get_title_html
        })