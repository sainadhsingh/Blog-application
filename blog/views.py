from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib import messages
from django.db.models import Q, Count, Sum
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, View
from django.urls import reverse_lazy, reverse
from django.http import JsonResponse, HttpResponseForbidden

from django.contrib.auth.models import User
from .models import Post, Category, Tag, Comment, Profile
from .forms import SignUpForm, UserUpdateForm, ProfileUpdateForm, PostForm, CommentForm

class PostListView(ListView):
    model = Post
    template_name = 'blog/post_list.html'
    context_object_name = 'posts'
    paginate_by = 6

    def get_queryset(self):
        queryset = Post.objects.filter(status='published').select_related('author', 'category').prefetch_related('tags')
        
        # Search query filter
        q = self.request.GET.get('q')
        if q:
            queryset = queryset.filter(
                Q(title__icontains=q) | 
                Q(content__icontains=q) |
                Q(category__name__icontains=q) |
                Q(tags__name__icontains=q)
            ).distinct()

        # Category filter by slug
        category_slug = self.kwargs.get('slug') if self.request.resolver_match.url_name == 'category_posts' else self.request.GET.get('category')
        if category_slug:
            self.category = get_object_or_404(Category, slug=category_slug)
            queryset = queryset.filter(category=self.category)
        else:
            self.category = None

        # Tag filter by slug
        tag_slug = self.kwargs.get('slug') if self.request.resolver_match.url_name == 'tag_posts' else self.request.GET.get('tag')
        if tag_slug:
            self.tag = get_object_or_404(Tag, slug=tag_slug)
            queryset = queryset.filter(tags=self.tag)
        else:
            self.tag = None

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['search_query'] = self.request.GET.get('q', '')
        context['current_category'] = getattr(self, 'category', None)
        context['current_tag'] = getattr(self, 'tag', None)
        context['featured_posts'] = Post.objects.filter(status='published').order_by('-views_count')[:3]
        return context


class PostDetailView(DetailView):
    model = Post
    template_name = 'blog/post_detail.html'
    context_object_name = 'post'

    def get_object(self, queryset=None):
        post = super().get_object(queryset)
        # Increment views count (using session to prevent duplicate counts per session)
        session_key = f'viewed_post_{post.pk}'
        if not self.request.session.get(session_key, False):
            post.views_count += 1
            post.save(update_fields=['views_count'])
            self.request.session[session_key] = True
        return post

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        post = self.object
        # Top-level comments only (parent is None)
        comments = post.comments.filter(is_active=True, parent__isnull=True).select_related('author', 'author__profile').prefetch_related('replies')
        context['comments'] = comments
        context['comment_form'] = CommentForm()
        context['is_liked'] = post.likes.filter(id=self.request.user.id).exists() if self.request.user.is_authenticated else False
        context['related_posts'] = Post.objects.filter(status='published', category=post.category).exclude(id=post.id)[:3]
        return context


class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    form_class = PostForm
    template_name = 'blog/post_form.html'

    def form_valid(self, form):
        form.instance.author = self.request.user
        messages.success(self.request, "Your blog post has been created successfully!")
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = 'Create New Blog Post'
        return context


class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    form_class = PostForm
    template_name = 'blog/post_form.html'

    def test_func(self):
        post = self.get_object()
        return self.request.user == post.author or self.request.user.is_superuser

    def form_valid(self, form):
        messages.success(self.request, "Your blog post has been updated successfully!")
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = f'Edit "{self.object.title}"'
        return context


class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    template_name = 'blog/post_confirm_delete.html'
    success_url = reverse_lazy('blog:dashboard')

    def test_func(self):
        post = self.get_object()
        return self.request.user == post.author or self.request.user.is_superuser

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, "Blog post deleted successfully.")
        return super().delete(request, *args, **kwargs)


class UserDashboardView(LoginRequiredMixin, ListView):
    model = Post
    template_name = 'blog/dashboard.html'
    context_object_name = 'posts'
    paginate_by = 10

    def get_queryset(self):
        status_filter = self.request.GET.get('status')
        queryset = Post.objects.filter(author=self.request.user).select_related('category')
        if status_filter in ['published', 'draft']:
            queryset = queryset.filter(status=status_filter)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user_posts = Post.objects.filter(author=self.request.user)
        context['total_posts'] = user_posts.count()
        context['published_count'] = user_posts.filter(status='published').count()
        context['draft_count'] = user_posts.filter(status='draft').count()
        context['total_views'] = user_posts.aggregate(Sum('views_count'))['views_count__sum'] or 0
        context['total_likes'] = user_posts.aggregate(total=Count('likes'))['total'] or 0
        context['current_status'] = self.request.GET.get('status', 'all')
        return context


class SignUpView(CreateView):
    form_class = SignUpForm
    template_name = 'registration/signup.html'
    success_url = reverse_lazy('blog:home')

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        messages.success(self.request, f"Welcome to the blog, {user.username}! Your account was created.")
        return redirect('blog:home')


@login_required
def profile_edit_view(request):
    profile, _ = Profile.objects.get_or_create(user=request.user)
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST, request.FILES, instance=profile)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, "Your profile has been updated successfully!")
            return redirect('blog:profile', username=request.user.username)
    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=profile)

    context = {
        'u_form': u_form,
        'p_form': p_form
    }
    return render(request, 'registration/profile_edit.html', context)


def profile_view(request, username):
    profile_user = get_object_or_404(User, username=username)
    profile, _ = Profile.objects.get_or_create(user=profile_user)
    user_posts = Post.objects.filter(author=profile_user, status='published')
    context = {
        'profile_user': profile_user,
        'profile': profile,
        'posts': user_posts,
    }
    return render(request, 'registration/profile.html', context)


class LikePostView(LoginRequiredMixin, View):
    def post(self, request, slug, *args, **kwargs):
        post = get_object_or_404(Post, slug=slug)
        if post.likes.filter(id=request.user.id).exists():
            post.likes.remove(request.user)
            liked = False
        else:
            post.likes.add(request.user)
            liked = True

        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            return JsonResponse({'liked': liked, 'total_likes': post.total_likes()})
        
        return redirect('blog:post_detail', slug=slug)


class AddCommentView(LoginRequiredMixin, View):
    def post(self, request, slug, *args, **kwargs):
        post = get_object_or_404(Post, slug=slug)
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.author = request.user
            parent_id = request.POST.get('parent_id')
            if parent_id:
                parent_comment = get_object_or_404(Comment, id=parent_id)
                comment.parent = parent_comment
            comment.save()
            messages.success(request, "Comment posted successfully!")
        else:
            messages.error(request, "Failed to post comment. Please check your text.")
        return redirect('blog:post_detail', slug=slug)


class DeleteCommentView(LoginRequiredMixin, View):
    def post(self, request, pk, *args, **kwargs):
        comment = get_object_or_404(Comment, pk=pk)
        # Only comment author, post author, or superuser can delete
        if request.user == comment.author or request.user == comment.post.author or request.user.is_superuser:
            post_slug = comment.post.slug
            comment.delete()
            messages.success(request, "Comment deleted successfully.")
            return redirect('blog:post_detail', slug=post_slug)
        return HttpResponseForbidden("You are not allowed to delete this comment.")
