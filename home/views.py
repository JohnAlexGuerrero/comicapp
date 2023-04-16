from django.shortcuts import render

from django.views.generic import TemplateView

from comic.models import Comic

class HomeView(TemplateView):
    template_name = "index.html"
    
    def get_context_data(self, **kwargs):
        comics = Comic.objects.all()
        context = super().get_context_data(**kwargs)
        context['comics'] = comics
        print(context['comics'][0].get_thumbnail)
        return context

