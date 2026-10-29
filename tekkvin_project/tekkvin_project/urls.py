from django.contrib import admin
from django.urls import include, path
from apps.store.views import LoginView, ProductDetailView, ProductListView, RegisterView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/auth/register/', RegisterView.as_view(), name='register'),
    path('api/auth/login/', LoginView.as_view(), name='login'),
    path('api/products/', ProductListView.as_view(), name='product-list'),
    path('api/products/<int:pk>/', ProductDetailView.as_view(), name='product-detail'),
    path("api/", include("apps.store.urls")),
]
