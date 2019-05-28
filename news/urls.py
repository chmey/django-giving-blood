from django.urls import path, include , re_path
from django.views.generic import ListView, DetailView
from news.models import Article
urlpatterns =(
  path('' , ListView.as_view(queryset=Article.objects.all().order_by('-date')[:20], template_name='news/posts.html')),
  re_path(r'^(?P<pk>\d+)$' , DetailView.as_view(model = Article , template_name='news/post.html')),
  )
