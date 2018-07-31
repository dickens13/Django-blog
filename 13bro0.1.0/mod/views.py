import json

from django.core.paginator import Paginator, EmptyPage
from django.http import HttpResponse
from django.shortcuts import render

from mod.models import Article


# 主页的视图函数，分成两类显示，以关联类型的id来分类
def index(request):
    b_art = Article.objects.filter(category_id=1)
    h_art = Article.objects.filter(category_id=2)
    posts = {'b_art': b_art, 'h_art': h_art}
    return render(request, 'index.html', posts)


# 博客页面的视图函数
def share(request):
    b_art = Article.objects.filter(category_id=1)
    paginator = Paginator(b_art, 4, 1)  # 每页显示8条,少于1条合并到上一页
    page = request.GET.get('page', 1)  # 获取url中page参数的值，1为默认值
    try:
        post_list = paginator.page(page)
    except EmptyPage:
        post_list = paginator.page(paginator.num_pages)  # 如页面超出范围则显示最后一页
    return render(request, 'share.html', {'post_list': post_list})


# 其他文章页面的视图函数
def essay(request):
    h_art = Article.objects.filter(category_id=2)
    paginator = Paginator(h_art, 4, 1)  # 每页显示8条,少于1条合并到上一页
    page = request.GET.get('page', 1)  # 获取url中page参数的值
    try:
        post_list = paginator.page(page)
    except EmptyPage:
        post_list = paginator.page(paginator.num_pages)  # 如页面超出范围则显示最后一页
    return render(request, 'essay.html', {'post_list': post_list})


# 时间轴的视图函数
def time(request):
    art = Article.objects.all()
    paginator = Paginator(art, 20, 5)  # 每页显示8条,少于1条合并到上一页
    page = request.GET.get('page', 1)
    try:
        post_list = paginator.page(page)
    except EmptyPage:
        post_list = paginator.page(paginator.num_pages)  # 如页面超出范围则显示最后一页
    return render(request, 'time.html', {'post_list': post_list})


def about(request):
    return render(request, 'about.html')


def gbook(request):
    return render(request, 'gbook.html')


# 内容详情页的视图函数
def content(request, no):  # 用传入no的方式获取文章
    art = Article.objects.get(pk=no)
    len_art = len(Article.objects.all())  # 获取文章总数
    art.viewed()  # 调用文章model属性的方法，增加浏览量
    if len_art > no >= 2:  # 如果文章总数大于2
        last_art = Article.objects.get(pk=no-1)  # 上一篇为当前no-1
        next_art = Article.objects.get(pk=no+1)  # 下一篇为当前no+1
    elif no == 1:  # 如果文章为第一篇时
        last_art = Article.objects.order_by('id').last()  # 上一篇为最后一篇
        next_art = Article.objects.get(pk=no+1)  # 下一篇为当前no+1
    else:  # 其他情况：如果当前no=文章总数(即当前文章为最后一篇时)
        last_art = Article.objects.get(pk=no-1)  # 上一篇文章为当前no+1
        next_art = Article.objects.order_by('id').first()  # 下一篇文章为第一篇
    posts = {'art': art, 'last': last_art, 'next': next_art}
    return render(request, 'content.html', posts)


# 显示点赞的函数
def make_good_comment(request, no):
    art = Article.objects.get(pk=no)  # 用传入no的方式获取文章
    art.good_count += 1  # 点赞之后数量加1
    art.save()  # 存入数据库
    ctx = {'code': 200, 'result': f'{art.good_count}'}
    return HttpResponse(json.dumps(ctx),
                        content_type='application/json; charset=utf-8')
