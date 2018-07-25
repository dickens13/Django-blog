from django.shortcuts import render

from mod.models import Article


def index(request):
    b_art = Article.objects.filter(category_id=1)
    h_art = Article.objects.filter(category_id=2)
    posts = {'b_art': b_art, 'h_art': h_art}
    return render(request, 'index.html', posts)


def share(request):
    b_art = Article.objects.filter(category_id=1)
    posts = {'b_art': b_art}
    return render(request, 'share.html', posts)


def list(request):
    h_art = Article.objects.filter(category_id=2)
    posts = {'h_art': h_art}
    return render(request, 'list.html', posts)


def time(request):
    return render(request, 'time.html')
