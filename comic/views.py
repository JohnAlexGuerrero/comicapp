from django.shortcuts import render

from .models import Comic

from django.views.generic import TemplateView

class ComicDetailView(TemplateView):
    template_name = "comic_detail.html"
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["comic"] = Comic.objects.get(slug=self.kwargs['comic_slug'])
        # print(context['comic'].image)
        return context
    
