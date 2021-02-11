from rest_framework import routers
from backend.views import TodoView

router = routers.DefaultRouter()
router.register('api/todo', TodoView, 'todo')

urlpatterns = router.urls
