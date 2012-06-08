#-*- coding: utf-8 -*-

from django.views.generic.list import ListView

from infinite_pagination.paginator import InfinitePaginator

from .models import Article


class ArticleListView(ListView):
    model = Article
    paginate_by = 10
    paginator_class = InfinitePaginator
    template_name = "article_list.html"
