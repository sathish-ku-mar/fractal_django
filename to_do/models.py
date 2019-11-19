import datetime

from django.db import models
from account.models import CommonModel, User
# Create your models here.


class DefaultModelManager(models.Manager):
    """
    The default Manager to only returns objects with the is_active set to True
    """

    def get_queryset(self):
        return super(DefaultModelManager, self).get_queryset().filter(is_active=True)


class AllModelManager(models.Manager):
    """
    Returns all objects regardless of the value of 'is_active'
    """
    pass


class Bucket(CommonModel):
    """
    This model is used to store the Bucket details.
    """
    name = models.CharField(max_length=200, help_text='The bucket name for the to-do')
    user = models.ForeignKey(User, on_delete=models.CASCADE, help_text='The user id who created this bucket')

    objects = DefaultModelManager()
    all_project_requests = AllModelManager()

    def __str__(self):
        return self.name

    @classmethod
    def get_user_associated_bucket_all(cls, user):
        """
        Get all buckets associated with user
        :param user: User id to get associated buckets list
        :return: Bucket object
        :rtype: django.db.models.query.QuerySet
        """
        return cls.objects.filter(user=user)

    def set_is_active(self):
        """
        Set active as false to remove buckets associated with user
        """
        self.is_active = False
        self.save(update_fields=['is_active'])
        # To delete tasks associated this bucket
        Task.remove_task_associated_with_bucket(bucket=self.pk)


class Task(CommonModel):
    """
    This model is used to store the user details.
    """
    name = models.CharField(max_length=200, help_text='The task name for the to-do')
    user = models.ForeignKey(User, on_delete=models.CASCADE, help_text='The user id who posted this task')
    bucket = models.ForeignKey(Bucket, on_delete=models.CASCADE, help_text='The bucket id associated with this task')
    is_done = models.BooleanField(default=False, help_text='This task is done or not')
    due_date = models.DateTimeField()

    objects = DefaultModelManager()
    all_project_requests = AllModelManager()

    class Meta:
        ordering = ['due_date', ]
        verbose_name_plural = 'Tasks'
        db_table = 'task'
        get_latest_by = "created_at"
        verbose_name = "Task"

    def __str__(self):
        return self.name

    @classmethod
    def get_task_all(cls):
        """
        Get all task associated with user
        :param: None
        :return: Bucket object
        :rtype: django.db.models.query.QuerySet
        """
        return cls.objects.all()

    @classmethod
    def get_today_tasks(cls, user):
        """
        Get today buckets associated with user
        :param user: The user associated with task
        :return: Task object
        :rtype: django.db.models.query.QuerySet
        """
        return cls.objects.filter(due_date__startswith=datetime.date.today(), user=user)

    @classmethod
    def get_bucket_associated_task_all(cls, bucket):
        """
        Get all buckets associated with user
        :param bucket: Bucket id to get associated buckets list
        :return: Bucket object
        :rtype: django.db.models.query.QuerySet
        """
        return cls.objects.filter(bucket=bucket)

    def set_is_done(self):
        """
        Set is_done as true to completed task associated with user
        """
        self.is_done = True
        self.save(update_fields=['is_done'])

    def set_is_active(self):
        """
        Set active as false to remove task associated with user
        """
        self.is_active = False
        self.save(update_fields=['is_active'])

    @classmethod
    def remove_task_associated_with_bucket(cls, bucket):
        """
        Set active as false to delete tasks associated with bucket
        :param bucket: Bucket id to get associated with task
        :return: Task object
        :rtype: django.db.models.query.QuerySet
        """
        return cls.get_bucket_associated_task_all(bucket=bucket).update(is_active=False)

