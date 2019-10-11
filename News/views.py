from django.shortcuts import render, redirect
from .models import *
from django.db.models import Q
from .forms import *
from django.urls import reverse
from django.http import Http404, HttpResponseRedirect
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage

# Create your views here.


def pagination(request, articles):
    paginator = Paginator(articles.filter(status__iexact='A'), 4)

    page_number = request.GET.get('page', 1)
    page = paginator.get_page(page_number)

    is_paginated = page.has_other_pages()

    if page.has_previous():
        prev_url = '?page={}'.format(page.previous_page_number())
    else:
        prev_url = ''
    if page.has_next():
        next_url = '?page={}'.format(page.next_page_number())
    else:
        next_url = ''

    context = {
        'page_object': page,
        'is_paginated': is_paginated,
        'next_url': next_url,
        'prev_url': prev_url
    }
    return context


def footer_news(request):
    articles = Article.objects.filter(status__iexact='A').order_by('-pub_date')[:4]
    return articles


def index(request):
    context = {}
    if request.POST:
        print(request.POST['search'])
        search_query = request.POST['search']
        articles = Article.objects.filter(Q(article_title__icontains=search_query) | Q(author__first_name__icontains=search_query) | Q(author__last_name__contains=search_query)
                                          | Q(author__username__icontains=search_query) | Q(genres__title__icontains=search_query)).distinct()
    else:
        articles = Article.objects.order_by('-pub_date')
    context = pagination(request, articles)
    context.update({'articles': footer_news(request)})
    return render(request, 'News/index.html', context=context)


def view_article(request, slug):
    article = Article.objects.get(article_slug__iexact=slug)
    comments = article.comment_set.filter(status__iexact='A').order_by('-id')[:10]
    context = {
        'article': article,
        'comments': comments,
        'articles': footer_news(request)
    }

    return render(request, 'News/article_view.html', context=context)


def tag_view(request, slug):
    article = Article.objects.filter(genres__slug__iexact=slug)
    context = {'articles': footer_news(request)}
    context.update(pagination(request, article))
    return render(request, 'News/index.html', context=context)


def info(request):
    context = {'articles': footer_news(request)}
    context.update({'page_title': 'О нас'})
    return render(request, 'News/info.html', context=context)


def author_search(request, id):
    articles = Article.objects.filter(author_id__exact=id)
    context = {'articles': footer_news(request)}
    context.update(pagination(request, articles))
    return render(request, 'News/index.html', context=context)


def view_genre_article(request, slug):
    article = Article.objects.filter(genres__slug__iexact=slug)
    context = pagination(request, article)
    return render(request, 'News/index.html', context=context)


def leave_comment(request, slug):
    try:
        a = Article.objects.get(article_slug__iexact=slug)
    except:
        raise Http404("Статья не найдена!")
    a.comment_set.create(author_name=request.POST['name'], comment_text=request.POST['text'])
    return redirect(view_article, slug)


def cooperation_view(request):
    form = BookForm()
    context = footer_news(request)
    if request.method == 'GET':
        return render(request, 'News/cooperation.html', context={'form': form, 'articles': context})
    else:
        bound_form = BookForm(request.POST)
        if bound_form.is_valid():
            print(bound_form['article_text'])
            print(bound_form['article_title'])
            article = Article.objects.create(article_title=request.POST['article_title'],
                                             article_text=request.POST['article_text'])
            article.save()
            return redirect(index)
    return render(request, 'News/cooperation.html', context=context)
