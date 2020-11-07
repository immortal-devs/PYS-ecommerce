
from django.contrib import admin

from admin_role import views
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    # path('admin/', admin.site.urls),
    
    path('',include('shop.urls')),
    path('admin_role/',include('admin_role.urls')),
    path('social-auth/', include('social_django.urls', namespace="social")),
    
    path('admin_role/', views.admin, name="admin"),
    path('addproduct/', views.addproduct, name="addproduct"),
    path('orders/orderstatus/<int:id>', views.orderstatus, name="orderstatus"),
    path('orders/', views.orders, name="orders"),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)