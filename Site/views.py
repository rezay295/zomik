from django.shortcuts import render
from django.http import HttpResponse
from Panel.models import *


# Create your views here.


def index(request):
    context = {}
    context.update({"Category": Category.objects.all()})
    context.update({"Varzeshi": News.objects.filter(category=Category.objects.get(title="ورزشی"))})
    context.update({"Baratin": News.objects.all().order_by("seenCount")[0:3]})
    return render(request, "index.html", context)


def list_category_news(request, cat_id):
    context = {}
    context.update({"News": News.objects.filter(category=Category.objects.get(id=cat_id))})
    return render(request, "category-01.html", context)


def news_detail(request, news_id):
    context = {}
    news = News.objects.get(id=news_id)
    news.seenCount += 1
    news.save()
    context.update({"News": news})
    return render(request, "single.html", context)
