from rest_framework.routers import SimpleRouter

from patients.views import PatientViewSet

router = SimpleRouter()
router.register(r'', PatientViewSet, basename='patient-create')

urlpatterns = router.urls
