"""blog_api URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
# from rest_framework import settings
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions
from rest_framework.routers import DefaultRouter

from main.views import CategoryListView, PostsListView, PostImageView, SearchListView, RatingViewSet, LikeViewSet, \
    CommentViewSet, FavoritesViewSet

schema_view = get_schema_view(
   openapi.Info(
      title="Blog API",
      default_version='v1',
      description="My Blog",
      terms_of_service="https://www.google.com/policies/terms/",
      contact=openapi.Contact(email="contact@snippets.local"),
      license=openapi.License(name="BSD License"),
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)


router = DefaultRouter()
router.register('posts', PostsListView)
router.register('ratings', RatingViewSet)
router.register('likes', LikeViewSet)
router.register('comments', CommentViewSet)
router.register('favorites', FavoritesViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api-auth/', include('rest_framework.urls')),
    path('v1/api/categories/', CategoryListView.as_view()),
    path('v1/api/add-image/', PostImageView.as_view()),
    path('v1/api/account/', include('account.urls')),
    path('v1/api/search/', SearchListView.as_view()),
    path('v1/api/', include(router.urls)),
    path('api/v1/docs/', schema_view.with_ui()),


]+static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
