"""myblog URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.views.static import serve

from mod import views
from myblog.settings import STATICFILES_DIRS

urlpatterns = [
    path('', views.index),
    path('share/', views.share),
    path('essay/', views.essay),
    path('time/', views.time),
    path('about/', views.about),
    path('study/', views.study),
    path('content/<int:no>', views.content),  # 针对内容页的映射链接
    path('good/<int:no>/', views.make_good_comment),  # 针对点赞功能的映射链接
    path('comment/<int:no>/', views.comments),
    path('search/', views.search),  # 针对搜索功能的映射链接
    path('static/<path>', serve, {"document_root": STATICFILES_DIRS[0]}),
    # path('mod', include('mod.urls', namespace='mod')),
    path('admin/', admin.site.urls)
]
