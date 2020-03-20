from django.urls import path
from django.views.generic import TemplateView

app_name = 'netzkarte'
urlpatterns = [
    path(
        '',
        TemplateView.as_view(
            template_name="netzkarte/index.html"),
        name='index'),
]
