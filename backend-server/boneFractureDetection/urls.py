from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
                  path('', views.index, name='Bone Fracture Detection'),
                  path('api', views.BoneFractureDetectionAPIView.as_view()),
              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
