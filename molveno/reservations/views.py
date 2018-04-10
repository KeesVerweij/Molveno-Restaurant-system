from django.shortcuts import render
from django.views.generic.base import TemplateView
from django.http import HttpResponse

# Create your views here.
class IndexView(TemplateView):
    template_name = "reservations/index.html"
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # context['variable'] = self.value
        return context
