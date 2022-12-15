from rest_framework import routers

from .views import SongView

router = routers.DefaultRouter()
router.register("", viewset=SongView)

app_name = "songs"
urlpatterns = router.urls
