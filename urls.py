from django.views.generic import TemplateView
from django.urls import path


app_name = 'netzkarte'
urlpatterns = [
    path('', TemplateView.as_view(template_name="netzkarte/index.html"), name='index'),
]
