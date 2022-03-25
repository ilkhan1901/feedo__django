from django.contrib import admin
from .models import Post,Comment

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
	
	# поле даты для навигации по иерархии дат
	date_hierarchy = 'publish'
	# отображение в таблице
	list_display = ('title','updated','status','author','publish')
	# фильтры в сайдбаре
	list_filter = ('status','created','publish','author')
	# правило для отображения в таблице по умолчанию
	ordering = ('status','publish')
	# слаг берётся с названия записи
	prepopulated_fields = {'slug':('title',)}
	# автор определяется по id
	raw_id_fields = ('author',)
	# поля для поиска
	search_fields = ('title','content')


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
	list_display = ('name','email','post','created','active')
	list_filter = ('active','created','updated')
	search_fields = ('name','email','body')
