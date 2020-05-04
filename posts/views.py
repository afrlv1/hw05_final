from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator
from posts.models import Post, Group, Comment, Follow
from .forms import PostForm, CommentForm
from django.db.models import Count
User = get_user_model()


def index(request):
    post_list = Post.objects.select_related(
        'author', 'group').order_by('-pub_date').annotate(
        comment_count=Count('comment'))
    paginator = Paginator(post_list, 5)  # показывать по 5 записей на странице.
    page_number = request.GET.get('page')  # переменная в URL с номером запрошенной страницы
    page = paginator.get_page(page_number)  # получить записи с нужным смещением
    return render(request, 'index.html', {
        'page': page,
        'paginator': paginator
    })


def group_posts(request, slug):
    group = get_object_or_404(Group, slug=slug)
    posts = Post.objects.filter(group=group).select_related('author').order_by('-pub_date').annotate(comment_count=Count('comment'))
    paginator = Paginator(posts, 5)  # показывать по 5 записей на странице.
    page_number = request.GET.get('page')  # переменная в URL с номером запрошенной страницы
    page = paginator.get_page(page_number)  # получить записи с нужным смещением
    return render(request, 'group.html', {
        'page': page,
        'group': group,
        'paginator': paginator
    })


@login_required
def new_post(request):
    if request.method == 'POST':
        form = PostForm(request.POST or None, files=request.FILES or None)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect('index')
    form = PostForm()
    return render(request, 'new_post.html', {
        'form': form
    })


def profile(request, username):
    # тут тело функции
    profile = get_object_or_404(User, username=username)
    posts_profile = Post.objects.filter(author=profile).order_by('-pub_date').all()
    posts_count = posts_profile.count()
    follow_count = Follow.objects.filter(author=profile).count()
    following_count = Follow.objects.filter(user=profile).count()
    following = False
    if request.user.is_authenticated:
        if Follow.objects.filter(user=request.user, author=profile).exists():
            following = True
    paginator = Paginator(posts_profile, 5)  # показывать по 5 записей на странице.
    page_number = request.GET.get('page')  # переменная в URL с номером запрошенной страницы
    page = paginator.get_page(page_number)  # получить записи с нужным смещением
    return render(request, 'profile.html', {
        'profile': profile,
        'posts_count': posts_count,
        'paginator': paginator,
        'page_num': page_number,
        'page': page,
        'follow_count': follow_count,
        'following_count': following_count,
        'following': following,
    })

def post_view(request, username, post_id):
    # тут тело функции
    profile = get_object_or_404(User, username=username)
    post_count = Post.objects.filter(author=profile).count()
    follow_count = Follow.objects.filter(author=profile).count()
    following_count = Follow.objects.filter(user=profile).count()
    following = False
    if request.user.is_authenticated:
        if Follow.objects.filter(user=request.user, author=profile).exists():
            following = True
    post = get_object_or_404(Post, pk=post_id)
    form = CommentForm()
    comments = Comment.objects.filter(post=post_id)
    return render(request, 'post.html', {
        'profile': profile,
        'posts_count': post_count,
        'post': post,
        'form': form,
        'comments': comments,
        'follow_count': follow_count,
        'following_count': following_count,
        'following': following,
    })


@login_required
def post_edit(request, username, post_id):
    author = get_object_or_404(User, username=username)
    post = get_object_or_404(Post, pk=post_id)

    if request.user != author:
        return redirect('post', username=username, post_id=post_id)
    if request.method == 'POST':
        form = PostForm(request.POST or None, files=request.FILES or None, instance=post)
        if form.is_valid():
            form.save()
            return redirect('post', username=username, post_id=post_id)
        return render(request, 'new_post.html', {'form': form, 'post': post})
    return render(request, 'new_post.html', {
        'form': PostForm(instance=post),
        'post': post
    })


@login_required
def add_comment(request, username, post_id):
    post = get_object_or_404(Post, pk=post_id)
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.author = request.user
            comment.post = post
            comment.save()
            return redirect('post', username=username, post_id=post_id)
    form = CommentForm()
    return redirect('post', username=post.author.username, post_id=post_id)


@login_required
def follow_index(request):
    author_list = Follow.objects.filter(user=request.user).values_list('author')
    post_list = Post.objects.filter(author__in=author_list).order_by("-pub_date")
    paginator = Paginator(post_list, 10)
    page_number = request.GET.get("page")
    page = paginator.get_page(page_number)
    return render(request, "follow.html", {"page": page, "paginator": paginator})


@login_required
def profile_follow(request, username):
    if request.user.username != username:
        follower = User.objects.get(username=request.user.username)
        following = User.objects.get(username=username)
        already_follows = Follow.objects.filter(user=follower, author=following).exists()
        if not already_follows:
            Follow.objects.create(user=follower, author=following)
    return redirect("profile", username=username)

@login_required
def profile_unfollow(request, username):
    follower = User.objects.get(username=request.user.username)
    following = User.objects.get(username=username)
    Follow.objects.filter(user=follower, author=following).delete()
    return redirect("profile", username=username)


def page_not_found(request, exception):
    # Переменная exception содержит отладочную информацию,
    # выводить её в шаблон пользователской страницы 404 мы не станем
    return render(request, 'misc/404.html', {'path': request.path}, status=404)


def server_error(request):
    return render(request, 'misc/500.html', status=500)
