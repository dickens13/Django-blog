from django.contrib import admin

from mod.models import User, Category, Article


class ArtAdmin(admin.ModelAdmin):
    list_display = ('title', 'content', 'status', 'create_time', 'last_mod_time',
                    'pub_time')
    search_fields = ('title', 'content')


admin.site.register(User)
# admin.site.register(Tag)
admin.site.register(Category)
# admin.site.register(ChiCategory)
admin.site.register(Article, ArtAdmin)
