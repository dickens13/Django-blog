from django.contrib import admin

from mod.models import User, Category, Article, Comments


# 创建管理后台的文章管理类型，包含显示内容、搜索内容，并加入富文本编辑器
class ArtAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'create_time', 'last_mod_time',
                    'pub_time')  # 后台显示的属性
    search_fields = ('title', 'content')  # 后台搜索及范围

    class Media:
        # 在管理后台的HTML文件中加入js文件，每一个路径都会追加STATIC_URL/
        js = (
            'js/kindeditor/kindeditor-all.js',
            'js/kindeditor/kindeditor-all-min.js',
            'js/kindeditor/lang/zh_CN.js',
            'js/kindeditor/config.js',
        )


admin.site.register(User)
# admin.site.register(Tag)
admin.site.register(Category)
# admin.site.register(ChiCategory)
admin.site.register(Article, ArtAdmin)
admin.site.register(Comments)  # 注册评论以便后台可以修改
