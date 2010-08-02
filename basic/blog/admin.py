from django.contrib import admin
from basic.blog.models import *


class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('title',)}
admin.site.register(Category, CategoryAdmin)

class PostAdmin(admin.ModelAdmin):
    list_display  = ('title', 'publish', 'status')
    list_filter   = ('publish', 'categories', 'status')
    search_fields = ('title', 'body')
    prepopulated_fields = {'slug': ('title',)}

    def get_form(self, request, obj=None, *args, **kwargs):
        if request.user.has_perm("blog.change_author"):
            self.exclude = ()
        else:
            self.exclude = ('author',)
        return super(PostAdmin,self).get_form(request, obj, *args, **kwargs)

    def save_model(self, request, obj, form, change):
        if getattr(obj, 'author', None) is None:
            obj.author = request.user
        obj.last_modified_by = request.user
        obj.save()

    def queryset(self, request):
        qs = super(PostAdmin,self).queryset(request)

        if request.user.is_superuser:
            return qs
        print request.user.user_permissions.values("codename")
        if request.user.has_perm("blog.change_post"):
            if request.user.has_perm("blog.change_own_post"):
                return qs.filter(author=request.user)
            else:
                return qs
        else:
            return qs.none()

admin.site.register(Post, PostAdmin)


class BlogRollAdmin(admin.ModelAdmin):
    list_display = ('name', 'url', 'sort_order',)
    list_editable = ('sort_order',)
admin.site.register(BlogRoll)
