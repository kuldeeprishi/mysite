from django.contrib import admin
from .models import Post, Category, Tag


class CategoryAdmin(admin.ModelAdmin):
	pass


class TagAdmin(admin.ModelAdmin):
	pass


class PostAdmin(admin.ModelAdmin):
	prepopulated_fields = {"slug": ("title",)}
	exclude = ('author',)

	def save_model(self, request, obj, form, change):
		obj.author = request.user
		obj.save()

admin.site.register(Post, PostAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Tag, TagAdmin)
