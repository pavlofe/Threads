from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from .models import Post, Comment, Like, Notification


# --------------------------
#  СТРІЧКА ПОСТІВ
# --------------------------
def feed(request):
    posts = Post.objects.all().order_by('-created_at')
    return render(request, 'main/feed.html', {'posts': posts})


# --------------------------
#  ДЕТАЛЬНИЙ ПОСТ
# --------------------------
def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    comments = post.comments.all().order_by('-created_at')
    return render(request, 'main/post_detail.html', {
        'post': post,
        'comments': comments
    })


# --------------------------
#  СТВОРЕННЯ ПОСТА
# --------------------------
@login_required
def create_post(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        content = request.POST.get('content')
        image = request.FILES.get('image')

        if title and content:
            Post.objects.create(
                author=request.user,
                title=title,
                content=content,
                image=image
            )
            return redirect('feed')

    return render(request, 'main/create_post.html')


# --------------------------
#  ДОДАТИ КОМЕНТАР
# --------------------------
@login_required
def add_comment(request, pk):
    post = get_object_or_404(Post, pk=pk)

    if request.method == 'POST':
        content = request.POST.get('content')
        if content:
            comment = Comment.objects.create(
                post=post,
                author=request.user,
                content=content
            )

            # -------- НОТИФІКАЦІЯ --------
            if post.author != request.user:
                Notification.objects.create(
                    user=post.author,
                    sender=request.user,
                    notification_type='comment',
                    post=post,
                    comment=comment
                )

    return redirect('post_detail', pk=pk)


# --------------------------
#  ЛАЙК ПОСТА
# --------------------------
@login_required
def like_post(request, pk):
    post = get_object_or_404(Post, pk=pk)
    existing_like = Like.objects.filter(post=post, user=request.user).first()

    if existing_like:
        existing_like.delete()  # анлайк
    else:
        Like.objects.create(post=post, user=request.user)

        # -------- НОТИФІКАЦІЯ --------
        if post.author != request.user:
            Notification.objects.create(
                user=post.author,
                sender=request.user,
                notification_type='like',
                post=post
            )

    return redirect('feed')


# --------------------------
#  ЛАЙК КОМЕНТАРЯ
# --------------------------
@login_required
def like_comment(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)
    existing_like = Like.objects.filter(comment=comment, user=request.user).first()

    if existing_like:
        existing_like.delete()
    else:
        Like.objects.create(comment=comment, user=request.user)

        # -------- НОТИФІКАЦІЯ --------
        if comment.author != request.user:
            Notification.objects.create(
                user=comment.author,
                sender=request.user,
                notification_type='like',
                comment=comment
            )

    return redirect('post_detail', pk=comment.post.pk)


# --------------------------
#  НОТИФІКАЦІЇ
# --------------------------
@login_required
def notifications(request):
    notes = request.user.notifications.all().order_by('-created_at')
    return render(request, 'main/notifications.html', {'notifications': notes})


# --------------------------
#  ПОЗНАЧИТИ ЯК ПРОЧИТАНЕ
# --------------------------
@login_required
def mark_notification_read(request, notif_id):
    note = get_object_or_404(Notification, id=notif_id, user=request.user)
    note.is_read = True
    note.save()
    return redirect('notifications')
