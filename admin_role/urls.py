from django.urls import path
from admin_role import views
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    #Leave as empty string for base url
	path('', views.admin, name="admin"),
    path('admin_role/', views.admin, name="admin"),
    path('adminlogin/', views.adminlogin, name="adminlogin"),
    path('adminlogout/', views.adminlogout, name="adminlogout"),
    path('checkuser/', views.checkuser, name="checkuser"),
    path('addproduct/', views.addproduct, name="addproduct"),
    path('checkproductdata/', views.checkproductdata, name="checkproductdata"),
]