from rest_framework import routers

from .views import SpeakerView, TopicView

router = routers.DefaultRouter()
router.register("speakers", viewset=SpeakerView)
router.register("topics", viewset=TopicView)

app_name = "speeches"
urlpatterns = router.urls
