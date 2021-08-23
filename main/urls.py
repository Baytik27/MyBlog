# from django.urls import path
#
# from main import views
#
#
# urlpatterns = [
#     path('categories/', views.CategoryListView.as_view(), name='categories-list'),
#     path('posts/', views.PostView.as_view(), name='post-list'),
#     path('posts/<int:pk>/', views.PostDetailView.as_view(), name='post-detail'),
#     path('posts-delete/<int:pk>/', views.PostDeleteView.as_view()),
#     path('posts-update/<int:pk>/', views.PostUpdateView.as_view()),
# ]


from django.urls import path, include
from rest_framework.routers import DefaultRouter

from main.views import *


router = DefaultRouter()
# router.register('posts', PostViewSet)
router.register('ratings', RatingViewSet)
router.register('likes', LikeViewSet)
router.register('comments', CommentViewSet)
router.register('favorites', FavoritesViewSet)


urlpatterns = [
    path('categories/', CategoryListView.as_view()),
    path('search/', SearchListView.as_view()),
    path('', include(router.urls)),
]
