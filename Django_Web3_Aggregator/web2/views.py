from django.shortcuts import render
from django.views.generic import TemplateView


# Create your views here.
class Web2(TemplateView):
    template_name = "base.html"