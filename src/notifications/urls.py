from rest_framework import routers

from .views import SubscriptionView

router = routers.DefaultRouter()
router.register("subscriptions", viewset=SubscriptionView)

app_name = "notifications"
urlpatterns = router.urls
