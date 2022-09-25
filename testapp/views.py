from django.urls import reverse
from django.views.generic import DetailView, ListView, RedirectView

from .models import Page


class IndexView(ListView):
    template_name = "index.html"
    model = Page


class PageView(DetailView):
    template_name = "page.html"
    model = Page


class FormRedirectView(RedirectView):
    def get_redirect_url(self, *args, **kwargs):
        return reverse("page", kwargs={"slug": kwargs.get("slug")})
