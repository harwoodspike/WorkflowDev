from django.conf.urls import url
from rest_framework.routers import DefaultRouter
from api.views import WorkflowViewSet


class ApiRouter(DefaultRouter):
    def get_urls(self):
        urls = super(ApiRouter, self).get_urls()
        urls.append(url(
            '^workflow/(?P<pk>[^/.]+)/get_step/(?P<step>[^/.]+)/$',
            WorkflowViewSet.as_view({'get': 'get_step'}),
            name='workflow-get-step'
        ))
        urls.append(url(
            '^workflow/(?P<pk>[^/.]+)/get_step/(?P<step>[^/.]+)\.(?P<format>[a-z0-9]+)/?$',
            WorkflowViewSet.as_view({'get': 'get_step'}),
            name='workflow-get-step'
        ))
        print("URLS", urls)
        return urls
