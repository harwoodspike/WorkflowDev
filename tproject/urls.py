"""tproject URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls import url, include
from django.conf.urls.static import static
from django.contrib import admin
from rest_framework import routers
from app import views as app_views
from api import views as api


# THIS IS WHERE YOU DEFINE API VIEWS
router = routers.DefaultRouter()
router.register(r'test', api.TestViewSet, 'user')
router.register(r'app_list', api.AppCategoryViewSet, 'user')

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^api/', include(router.urls)),
    url(r'dynamic.(?P<ftype>(js|css))', app_views.dynamic_files, name="dynamic_files"),
    url(r'^workflow/(?P<wiz_id>[0-9]+)/step/(?P<step>[0-9]+)/$', app_views.workflow, name="workflow"),
    url(r'^workflow/(?P<wiz_id>[0-9]+)/$', app_views.workflow, name="jobs_workflow"),
    url(r'^$', app_views.redirectToVue, name="dashboard"),
]
urlpatterns = list(urlpatterns) + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
