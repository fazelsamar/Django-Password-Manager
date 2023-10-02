from django.urls import path

from rest_framework_nested import routers

from . import views

app_name = "password"

router = routers.DefaultRouter()
router.register('collections', views.PasswordCollectionViewSet, basename='collections')

collection_router = routers.NestedSimpleRouter(router, 'collections', lookup='collection')
collection_router.register('passwords', views.PasswordViewSet, basename='collection-passwords')

urlpatterns = router.urls + collection_router.urls + [
    path("get-password-by-token/<uuid:token_id>/", views.GetPasswordByToken.as_view(), name="get_password_by_token"),
]
