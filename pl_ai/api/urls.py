from django.conf.urls import url, include
from rest_framework.urlpatterns import format_suffix_patterns
from . import views

urlpatterns = {
        url(r'^notes/$', views.note_list, name="note_list"),
}

urlpatterns = format_suffix_patterns(urlpatterns)
