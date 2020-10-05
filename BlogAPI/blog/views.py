from rest_framework.generics import CreateAPIView, ListAPIView, RetrieveAPIView, RetrieveUpdateAPIView, DestroyAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .serializers import PostSerializer
from rest_framework import status
from .permissions import IsOwner
from .models import Post


class PostCreateAPIView(CreateAPIView):
    serializer_class = PostSerializer
    queryset = Post.objects.all()
    permission_classes = (IsAuthenticated,)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class PostListAPIView(ListAPIView):
    serializer_class = PostSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        queryset = Post.objects.filter(owner=self.request.user)
        return queryset


class PostDetailAPIView(RetrieveAPIView):
    serializer_class = PostSerializer
    queryset = Post.objects.all()
    permission_classes = (IsAuthenticated, IsOwner)
    lookup_field = 'id'


class PostUpdateAPIView(RetrieveUpdateAPIView):
    serializer_class = PostSerializer
    queryset = Post.objects.all()
    permission_classes = (IsAuthenticated, IsOwner)
    lookup_field = 'id'

    def perform_update(self, serializer):
        serializer.save(owner=self.request.user)


class PostDeleteAPIView(DestroyAPIView):
    serializer_class = PostSerializer
    queryset = Post.objects.all()
    permission_classes = (IsAuthenticated, IsOwner)
    lookup_field = 'id'

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response({'message': 'Post is deleted'}, status=status.HTTP_204_NO_CONTENT)
