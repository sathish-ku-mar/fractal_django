from django.urls import path,include
from django.conf.urls import url

from .views import BucketViewSet, TaskViewSet
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'bucket', BucketViewSet,base_name='bucket')
router.register(r'task', TaskViewSet,base_name='task')


urlpatterns = [
]

urlpatterns += router.urls