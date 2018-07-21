from django.shortcuts import render

from mod.models import Article


def index(request):
    b_art = Article.objects.filter(chicategory__first_type_id=1)
    h_art = Article.objects.filter(chicategory_id=3)
    s_art = Article.objects.filter(chicategory_id=4)
    posts = {'b_art': b_art, 'h_art': h_art, 's_art': s_art}
    return render(request, 'index.html', posts)
