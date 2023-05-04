from django.urls import include, path

from rest_framework.routers import DefaultRouter

from api.views import (CategoryViewSet, CommentViewSet, GenreViewSet,
                       ReviewsViewSet, TitleViewSet, UserViewSet,
                       get_token_for_user, user_registration)

app_name = 'api'

router = DefaultRouter()
router.register(r'users', UserViewSet, basename='user')
router.register(r'titles', TitleViewSet)
router.register(r'genres', GenreViewSet)
router.register(r'categories', CategoryViewSet)
router.register(r'titles/(?P<title_id>[\d]{1,})/reviews',
                ReviewsViewSet, basename='reviews'
                )
router.register(
    r'titles/(?P<title_id>[\d]{1,})/reviews/(?P<review_id>[\d]{1,})/comments',
    CommentViewSet, basename='comments'
)


urlpatterns = [
    path('', include(router.urls)),
    path('auth/signup/', user_registration),
    path('auth/token/', get_token_for_user),
]
