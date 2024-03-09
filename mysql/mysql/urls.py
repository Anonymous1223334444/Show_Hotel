"""
URL configuration for mysql project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
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
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf.urls.static import static
from django.conf import settings
from django.contrib import admin
from django.urls import path
from test_app import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('request_1', views.index1),
    path('request_2', views.index2),
    path('request_3', views.index3),                                
    path('request_4', views.index4),
    path('request_5', views.index5),
    path('extra_1', views.extra1),
    path('extra_2', views.extra2),                                
    path('extra_3', views.extra3),
    path('extra_4', views.extra4),
    path('extra_5', views.extra5),
    path('extra_6', views.extra6),
    path('extra_7', views.extra7),
    path('extra_8', views.extra8),
    path('extra_9', views.extra9),
    path('annuler_reservation', views.annuler),
    path('annulation_reussi', views.ann_reussi),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

urlpatterns += staticfiles_urlpatterns()
