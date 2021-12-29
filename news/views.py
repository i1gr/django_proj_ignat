from django.shortcuts import render, get_object_or_404

from news.models import News
from service.models import Services


# Create your views here.


def home(request):
    services = Services.objects.all()
    print(services)
    return render(request, 'news/home.html', {"title": 'Home page', 'nav_active': 'home', 'services': services})


def news(request):
    all_news = News.objects.all()
    return render(request, 'news/news.html', {"title": 'News page', 'nav_active': 'news', "news": all_news})


def article(request, article_slug):
    article_data = get_object_or_404(News, slug=article_slug)

    context = {
        'title': f'{article_data.title}',
        'nav_active': 'news',
        'article_data': article_data
    }
    return render(request, 'news/article.html', context=context)
