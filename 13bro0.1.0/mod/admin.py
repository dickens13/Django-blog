from django.contrib import admin

from mod.models import User, Category, Article


class ArtAdmin(admin.ModelAdmin):
    list_display = ('title', 'content', 'status', 'create_time', 'last_mod_time',
                    'pub_time')
    search_fields = ('title', 'content')

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
