from rest_framework import serializers
from .models import Bucket, Task


class BucketSerializer(serializers.ModelSerializer):

    class Meta:
        model = Bucket
        fields = ('id', 'name', 'user')
        read_only_fields = ('id',)


class TaskSerializer(serializers.ModelSerializer):
    bucket_name = serializers.CharField(source='bucket.name', read_only=True)

    class Meta:
        model = Task
        fields = ('id', 'name', 'user', 'bucket', 'bucket_name', 'is_done', 'due_date')
        read_only_fields = ('id', 'is_done', 'bucket_name')


class TaskListSerializer(TaskSerializer):
    bucket = BucketSerializer(read_only=True)

    class Meta(TaskSerializer.Meta):
        model = Task
        fields = TaskSerializer.Meta.fields


class BucketAssociatedTaskListSerializer(BucketSerializer):
    tasks = serializers.SerializerMethodField()

    @staticmethod
    def get_tasks(obj):
        queryset = Task.get_bucket_associated_task_all(bucket=obj.pk)
        return TaskSerializer(queryset, many=True).data

    class Meta(BucketSerializer.Meta):
        model = Bucket
        fields = BucketSerializer.Meta.fields + ('tasks',)