from .views import PostCreateAPIView, PostListAPIView, PostDetailAPIView, PostUpdateAPIView, PostDeleteAPIView
from django.urls import path


urlpatterns = [
    path('post_create/', PostCreateAPIView.as_view(), name='post_create'),
    path('post_list/', PostListAPIView.as_view(), name='post_list'),
    path('post_detail/<int:id>/', PostDetailAPIView.as_view(), name='post_detail'),
    path('post_update/<int:id>/', PostUpdateAPIView.as_view(), name='post_update'),
    path('post_delete/<int:id>/', PostDeleteAPIView.as_view(), name='post_delete'),
]