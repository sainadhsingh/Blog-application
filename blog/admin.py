from django.contrib import admin
from .models import Profile, Category, Tag, Post, Comment

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'location', 'website', 'created_at')
    search_fields = ('user__username', 'user__email', 'location')


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'post_count')
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ('name',)

    def post_count(self, obj):
        return obj.posts.count()
    post_count.short_description = 'Posts Count'


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'post_count')
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ('name',)

    def post_count(self, obj):
        return obj.posts.count()
    post_count.short_description = 'Posts Count'


class CommentInline(admin.TabularInline):
    model = Comment
    extra = 0
    readonly_fields = ('author', 'content', 'created_at')


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'category', 'status', 'created_at', 'views_count', 'total_likes_display')
    list_filter = ('status', 'category', 'created_at', 'tags')
    search_fields = ('title', 'content', 'author__username')
    prepopulated_fields = {'slug': ('title',)}
    filter_horizontal = ('tags',)
    raw_id_fields = ('author',)
    date_hierarchy = 'created_at'
    inlines = [CommentInline]
    actions = ['make_published', 'make_draft']

    def total_likes_display(self, obj):
        return obj.total_likes()
    total_likes_display.short_description = 'Likes'

    @admin.action(description='Mark selected posts as published')
    def make_published(self, request, queryset):
        queryset.update(status='published')

    @admin.action(description='Mark selected posts as draft')
    def make_draft(self, request, queryset):
        queryset.update(status='draft')


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('author', 'post', 'parent', 'created_at', 'is_active')
    list_filter = ('is_active', 'created_at')
    search_fields = ('content', 'author__username', 'post__title')
    actions = ['approve_comments', 'disapprove_comments']

    @admin.action(description='Approve selected comments')
    def approve_comments(self, request, queryset):
        queryset.update(is_active=True)

    @admin.action(description='Disapprove selected comments')
    def disapprove_comments(self, request, queryset):
        queryset.update(is_active=False)
