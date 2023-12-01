from .models import Page
from .forms import SearchForm


def pages(request):
    page_list = Page.objects.filter(show_in_nav__exact=1).order_by("title")
    return {"pages": page_list}


def search_form(request):
    return {"search_form": SearchForm(request.GET or None)}
