from django.conf.urls import url, include
from django.contrib import admin
from rest_framework.urlpatterns import format_suffix_patterns
from backend import views
from rest_framework_nested import routers
from django.conf import settings


router = routers.DefaultRouter()
router.register(r'users', views.UserViewSet)
router.register(r'images', views.ImageViewSet)
router.register(r'comments', views.CommentViewSet)
router.register(r'faq', views.FAQViewSet)

images_router = routers.NestedSimpleRouter(router, r'images', lookup='image')
images_router.register(r'comments', views.NestedCommentViewSet)

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^api/', include(router.urls)),
    url(r'^api/', include(images_router.urls)),
]

# Login and logout views for the browsable API
urlpatterns += [
    url(r'^api-auth/', include('rest_framework.urls',
                               namespace='rest_framework')),
]

if settings.DEBUG:
    from django.contrib.staticfiles.urls import staticfiles_urlpatterns
    from django.conf.urls.static import static

    urlpatterns += staticfiles_urlpatterns()
    urlpatterns += static(
        settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
