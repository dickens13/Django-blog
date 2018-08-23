import json
import pytz
from datetime import datetime

from django.core.paginator import Paginator, EmptyPage
from django.db.models import Q
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect

from mod.models import Article, Poll, Comments


# 主页的视图函数，分成两类显示，以关联类型的id来分类
def index(request):
    b_art = Article.objects.filter(category_id=1).order_by('-create_time')
    h_art = Article.objects.filter(category_id=2).order_by('pub_time')
    j_art = Article.objects.filter(category_id=3).order_by('pub_time')
    posts = {'b_art': b_art, 'h_art': h_art, 'j_art': j_art}
    return render(request, 'index.html', posts)


# 博客页面的视图函数
def share(request):
    b_art = Article.objects.filter(category_id=1).order_by('-create_time')
    paginator = Paginator(b_art, 8, 2)  # 每页显示8条,少于1条合并到上一页
    page = request.GET.get('page', 1)  # 获取url中page参数的值，1为默认值
    try:
        post_list = paginator.page(page)
    except EmptyPage:
        post_list = paginator.page(paginator.num_pages)  # 如页面超出范围则显示最后一页
    return render(request, 'share.html', {'post_list': post_list})


# 其他文章页面的视图函数
def essay(request):
    h_art = Article.objects.filter(category_id=2).order_by('-create_time')
    paginator = Paginator(h_art, 8, 2)  # 每页显示8条,少于1条合并到上一页
    page = request.GET.get('page', 1)  # 获取url中page参数的值
    try:
        post_list = paginator.page(page)
    except EmptyPage:
        post_list = paginator.page(paginator.num_pages)  # 如页面超出范围则显示最后一页
    return render(request, 'essay.html', {'post_list': post_list})


def study(request):
    s_art = Article.objects.filter(category_id=3).order_by('-create_time')
    paginator = Paginator(s_art, 8, 2)  # 每页显示8条,少于1条合并到上一页
    page = request.GET.get('page', 1)  # 获取url中page参数的值
    try:
        post_list = paginator.page(page)
    except EmptyPage:
        post_list = paginator.page(paginator.num_pages)  # 如页面超出范围则显示最后一页
    return render(request, 'study.html', {'post_list': post_list})


# 时间轴的视图函数
def time(request):
    art = Article.objects.all().order_by('-pub_time')
    paginator = Paginator(art, 20, 4)  # 每页显示8条,少于1条合并到上一页
    page = request.GET.get('page', 1)
    try:
        post_list = paginator.page(page)
    except EmptyPage:
        post_list = paginator.page(paginator.num_pages)  # 如页面超出范围则显示最后一页
    return render(request, 'time.html', {'post_list': post_list})


def about(request):
    return render(request, 'about.html')


# 内容详情页的视图函数
def content(request, no):  # 用传入no的方式获取文章
    art = Article.objects.get(pk=no)
    len_art = len(Article.objects.all())  # 获取文章总数
    art.viewed()  # 调用文章model属性的方法，增加浏览量
    comms = Comments.objects.filter(blog_id=no)  # 增加一个获取文章相关评论的参数以便页面调用
    if len_art > no >= 2:  # 如果文章总数大于2
        last_art = Article.objects.get(pk=no-1)  # 上一篇为当前no-1
        next_art = Article.objects.get(pk=no+1)  # 下一篇为当前no+1
    elif no == 1:  # 如果文章为第一篇时
        last_art = Article.objects.order_by('id').last()  # 上一篇为最后一篇
        next_art = Article.objects.get(pk=no+1)  # 下一篇为当前no+1
    else:  # 其他情况：如果当前no=文章总数(即当前文章为最后一篇时)
        last_art = Article.objects.get(pk=no-1)  # 上一篇文章为当前no+1
        next_art = Article.objects.order_by('id').first()  # 下一篇文章为第一篇
    posts = {'art': art, 'last': last_art, 'next': next_art, 'comms': comms}
    return render(request, 'content.html', posts)


# 获取ip的方法
def get_ip(request):
    # META自带的HTTP_X_FORWARDED_FOR可以获取真实IP地址
    if 'HTTP_X_FORWARDED_FOR' in request.META:
        return request.META['HTTP_X_FORWARDED_FOR']
    # REMOTE_ADDR是代理前的IP地址
    else:
        return request.META['REMOTE_ADDR']


# 显示点赞的函数
def make_good_comment(request, no):
    art = Article.objects.get(pk=no)  # 用传入no的方式获取文章
    ip = get_ip(request)
    poll = Poll.objects.filter(ip=ip, art=art).first()
    # 如果访问ip存在，就进行时间计算
    if poll:
        # 将现在的时间转换为utc以便跟click_time做比较，同一时区才能加减
        now_time = datetime.now(pytz.utc)
        diff_time = now_time - poll.click_time
        # 如果访问时间差超过2分钟，则可以点赞并+1
        if diff_time.seconds > 120:
            poll.art.good_count += 1
            # 刷新点击的初始时间，以备下一次计算
            # 必须先刷新时间，后进行次数更新，否则报错
            poll.click_time = now_time
            poll.save()  # 存入数据库,同时新的ip点击时间替换掉之前存储的ip时间
            ctx = {'code': 200, 'result': f'{poll.art.good_count}'}
            return HttpResponse(json.dumps(ctx),
                                content_type='application/json; charset=utf-8')
        # 如没超过2分钟则弹出提示
        else:
            return JsonResponse({'result1': 'ok'})  # 返回json数据以便前端接收
    # 如果访问ip不存在，则允许点赞
    else:
        Poll.objects.create(ip=ip, art=art, click_time=datetime.now())  # 获取
        art.good_count += 1  # 点赞之后数量加1
        art.save()  # 存入数据库
        ctx = {'code': 200, 'result': f'{art.good_count}'}
        return HttpResponse(json.dumps(ctx),
                            content_type='application/json; charset=utf-8')


# 评论的视图函数
def comments(request, no):
    if request.method == 'POST':  # 如果有请求调用本函数时(即前端进行评论提交时)
        art = Article.objects.get(pk=no)
        ip = get_ip(request)
        say = request.POST.get('say')  # 获取页面输入的评论内容
        name = request.POST.get('name')  # 获取页面输入的昵称
        comm = Comments.objects.filter(ip=ip, blog=art).last()  # 实例化评论模型,取第一个
        if comm:
            now_time = datetime.now(pytz.utc)
            diff_time = now_time - comm.create_time
            if diff_time.seconds > 120:  # 对比系统时间和之前存在的评论时间，是否大于2分钟
                comm = Comments()
                comm.content = say  # 关联评论内容
                comm.nickname = name  # 关联昵称
                comm.blog = art  # 关联文章
                comm.ip = ip
                comm.save()  # 存储评论
                ctx = {'code': 200}
                return JsonResponse(ctx)  # 返回数据
            else:  # 如果在两分钟之内
                return JsonResponse({'too_fast': '评论得太快了，休息一会吧！'})
        else:  # 如果评论不存在，则直接创建新评论
            comm = Comments()
            comm.content = say  # 关联评论内容
            comm.nickname = name    # 关联昵称
            comm.blog = art  # 关联文章
            comm.ip = ip
            comm.save()  # 存储评论
            ctx = {'code': 200}
            return JsonResponse(ctx)  # 返回数据

# def comments(request, no):
#     if request.method == 'POST':
#         art = Article.objects.get(pk=no)
#         say = request.POST.get('say')  # 获取页面输入的评论内容
#         name = request.POST.get('name')  # 获取页面输入的昵称
#         comm = Comments()  # 实例化评论模型
#         comm.content = say  # 关联评论内容
#         comm.nickname = name    # 关联昵称
#         comm.blog = art  # 关联文章
#         comm.save()  # 存储评论
#         ctx = {'code': 200}
#         return JsonResponse(ctx)  # 返回数据


# 搜索函数
def search(request):
    k = request.POST.get('keyboard')  # 定义一个变量接收页面过来的请求内容
    error_msg = ''  # 定义错误信息为空
    if not k:
        error_msg = '请输入关键词'  # 如果请求不是k则后端返回信息
        return render(request, 'search.html', {'error_msg': error_msg})
    # k请求过来之后，查询相关联的文章（包括标题、内容）；Q是自带的模块，通过或字符达到or的效果
    post_list = Article.objects.filter(Q(title__icontains=k) | Q(content__contains=k))
    # 返回数据给前端
    return render(request, 'search.html', {'error_msg': error_msg, 'post_list': post_list})
