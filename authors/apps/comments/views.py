from rest_framework import generics
from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from . import serializers
from .utils import Utils
from .models import Comment
from authors.apps.articles.models import Article


class CreateCommentAPiView(generics.ListCreateAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = serializers.CommentSerializer

    queryset = Comment.objects.all()
    util = Utils()

    def post(self, request, *args, **kwargs):
        '''This method creates a comment on an article'''

        slug = self.kwargs['slug']
        article = self.util.check_article(slug)
        comment = request.data
        comment.update({'author': request.user.pk, 'article': article.id})
        serializer = self.serializer_class(data=comment)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({"message": "Comment Successfully added"},
                        status=status.HTTP_201_CREATED)

    def get(self, *args, **kwargs):
        '''This method gets all comments for an article'''

        slug = self.kwargs['slug']
        article = self.util.check_article(slug)
        comments = self.queryset.filter(article_id=article.id)
        serializer = self.serializer_class(comments, many=True)
        return Response({"comments": serializer.data,
                         "commentsCount": comments.count()})


class CommentApiView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = serializers.CommentSerializer
    util = Utils()

    def retrieve(self, request, id, *args, **kwargs):
        '''This method gets a single comment by id'''

        slug = self.kwargs['slug']
        article = self.util.check_article(slug)
        comment = self.util.check_comment(id)
        serializer = self.serializer_class(comment)
        return Response({"comment": serializer.data})

    def update(self, request, id, *args, **kwargs):
        '''This method updates a comment'''

        slug = self.kwargs['slug']
        article = self.util.check_article(slug)
        comment = self.util.check_comment(id)

        if request.user.pk == comment.author.id:
            Comment.objects.all().filter(pk=id).update(**request.data)
            msg = "Comment successfully updated"
            return Response({
                "message": msg
            }, status=status.HTTP_200_OK)
        else:
            msg = {"error": "Unauthorized to update this comment"}
            return Response({
                "message": msg
            }, status=status.HTTP_401_UNAUTHORIZED)

    def destroy(self, request, id, *args, **kwargs):
        '''This method deletes a comment'''

        slug = self.kwargs['slug']
        article = self.util.check_article(slug)
        comment = self.util.check_comment(id)

        if request.user.pk == comment.author.id:
            self.perform_destroy(comment)
            msg = "Comment successfully deleted"
            return Response({
                "message": msg
            }, status=status.HTTP_200_OK)
        else:
            msg = {"error": "Unauthorized to delete this comment"}
            return Response({
                "message": msg
            }, status=status.HTTP_401_UNAUTHORIZED)


class CommentThreadApiView(generics.ListCreateAPIView):

    queryset = Comment.objects.all()
    serializer_class = serializers.CommentSerializer
    util = Utils()

    def post(self, request, id, *args, **kwargs):
        '''This method comments on a comment creating a thread'''

        slug = self.kwargs['slug']
        article = self.util.check_article(slug)
        parent = self.util.check_comment(id)
        comment = request.data
        comment.update({'author': request.user.pk,
                        'article': article.id,
                        'parent': id})
        serializer = self.serializer_class(data=comment)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({"message": "Comment Thread Successfully added"},
                        status=status.HTTP_201_CREATED)

    def get(self, request, id, *args, **kwargs):
        '''This method gets an entire thread of comments'''

        slug = self.kwargs['slug']
        article = self.util.check_article(slug)
        parent = self.util.check_comment(id)
        thread = self.queryset.filter(article_id=article.id, parent=id)
        serializer = self.serializer_class(thread, many=True)
        return Response({"comments": serializer.data,
                         "thread count": thread.count()})
