from django.urls import path
from .views import (
    feed, post_detail, create_post,
    add_comment, like_post, like_comment,
    notifications, mark_notification_read
)

urlpatterns = [
    path('', feed, name='feed'),
    path('post/<int:pk>/', post_detail, name='post_detail'),
    path('post/create/', create_post, name='create_post'),
    path('post/<int:pk>/comment/', add_comment, name='add_comment'),
    path('post/<int:pk>/like/', like_post, name='like_post'),
    path('comment/<int:comment_id>/like/', like_comment, name='like_comment'),
    path('notifications/', notifications, name='notifications'),
    path('notification/<int:notif_id>/read/', mark_notification_read, name='mark_notification_read'),
]
