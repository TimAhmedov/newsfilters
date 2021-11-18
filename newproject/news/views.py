from django.views.generic import ListView, DetailView
from .models import *


class NewsList(ListView):
    model = Post
    template_name = 'News.html'
    context_object_name = 'News'




class NewsDetail(DetailView):
    model = Post
    template_name = 'New.html'
    context_object_name = 'New'
