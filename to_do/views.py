from django.shortcuts import get_object_or_404
# Create your views here.
from .models import Bucket, Task
from .serializers import BucketSerializer, TaskSerializer, TaskListSerializer, BucketAssociatedTaskListSerializer
from rest_framework import status, viewsets
from rest_framework.response import Response
from django.http.request import QueryDict
from core.api_permission import UserAuthentication


class BucketViewSet(viewsets.ViewSet):
    """
        A simple ViewSet for the Bucket.
    """
    model = Bucket
    serializer_class = BucketSerializer
    permission_classes = (UserAuthentication,)

    def list(self, request):
        """
            To list the Bucket
            URL Structure: /to-do/bucket/
            Required Fields: None
        """

        queryset = self.model.get_user_associated_bucket_all(user=request.user.pk)
        serializer = self.serializer_class(queryset, many=True)
        return Response(serializer.data)

    def create(self, request):
        """
            To create the Bucket
            URL Structure: /to-do/bucket/
            Required Fields: 'name'
        """

        data = QueryDict.dict(request.data)
        data['user'] = request.user.pk
        serializer = self.serializer_class(data=data)

        if serializer.is_valid():
            obj = serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, pk):
        """
            To update the particular Bucket
            URL Structure: /to-do/bucket/1/
            Required Fields: `id`, 'name'
        """
        queryset = get_object_or_404(self.model, pk=pk, user=request.user.pk)

        data = QueryDict.dict(request.data)
        serializer = self.serializer_class(queryset, data=data, partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)

    def delete(self, request, pk):
        """
            To delete the particular Bucket
            URL Structure: /to-do/bucket/1/
            Required Fields: id
        """
        queryset = get_object_or_404(self.model, pk=pk, user=request.user.pk)
        queryset.set_is_active()

        return Response({'message': 'Deleted'}, status=200)


class TaskViewSet(viewsets.ViewSet):
    """
        A simple ViewSet for the Task.
    """
    model = Task
    serializer_class = TaskSerializer
    permission_classes = (UserAuthentication,)

    def list(self, request):
        """
            To list the Task
            URL Structure: /to-do/task/
            Required Fields: None
        """
        user = request.user
        today = TaskListSerializer(self.model.get_today_tasks(user=user.pk), many=True).data

        queryset = Bucket.get_user_associated_bucket_all(user=user.pk)
        bucket = BucketAssociatedTaskListSerializer(queryset, many=True).data
        context = {
            'today': today,
            'bucket': bucket
        }
        return Response(context)

    def create(self, request):
        """
            To create the Task
            URL Structure: /to-do/task/
            Required Fields: 'name', 'bucket', 'due_date'
        """

        data = QueryDict.dict(request.data)
        data['user'] = request.user.pk
        serializer = self.serializer_class(data=data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, pk):
        """
            To update the particular Task
            URL Structure: /to-do/task/1/
            Required Fields: `id`, 'name', 'bucket', 'due_date'
        """
        user = request.user.pk
        queryset = get_object_or_404(self.model, pk=pk, user=user)

        data = QueryDict.dict(request.data)
        serializer = self.serializer_class(queryset, data=data, partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)

    def patch(self, request, pk):
        """
            To update the particular Task
            URL Structure: /to-do/task/1/
            Required Fields: `id`
        """
        queryset = get_object_or_404(self.model, pk=pk, user=request.user.pk)
        queryset.set_is_done()

        return Response({'message': 'Updated'}, status=200)

    def delete(self, request, pk):
        """
            To delete the particular Task
            URL Structure: /to-do/task/1/
            Required Fields: id
        """
        queryset = get_object_or_404(self.model, pk=pk, user=request.user.pk)
        queryset.set_is_active()

        return Response({'message': 'Deleted'}, status=200)