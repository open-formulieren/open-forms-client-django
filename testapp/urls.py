from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.urls import path, re_path

from .views import FormRedirectView, IndexView, PageView

urlpatterns = [
    path("admin/", admin.site.urls),
    # The view thats starts the form
    path("page/<slug:slug>", PageView.as_view(), name="page"),
    # Whenever you refresh the page that has the form, the URL might be changed
    # and needs to redirect the user to the start of the form.
    re_path(r"^page/(?P<slug>\w+)/", FormRedirectView.as_view()),
    path("", IndexView.as_view()),
]

# NOTE: The staticfiles_urlpatterns also discovers static files (ie. no need to run collectstatic). Both the static
# folder and the media folder are only served via Django if DEBUG = True.
urlpatterns += staticfiles_urlpatterns() + static(
    settings.MEDIA_URL, document_root=settings.MEDIA_ROOT
)
