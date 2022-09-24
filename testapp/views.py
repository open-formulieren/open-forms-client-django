from django.views.generic import DetailView, ListView

from .models import Page


class IndexView(ListView):
    template_name = "index.html"
    model = Page


class PageView(DetailView):
    template_name = "page.html"
    model = Page
