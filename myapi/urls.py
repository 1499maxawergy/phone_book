# myapi/urls.py
from urllib import request
from django.urls import include, path, re_path
from . import views
from drf_yasg import openapi  # new
from rest_framework import permissions
from drf_yasg.views import get_schema_view  # new

#Swagger

schema_view = get_schema_view(  # new
    openapi.Info(
        title="Phonebook API",
        default_version='v1.1',
        description="Documentation for work with Phonebook project",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="maxawergy@yandex.ru"),
        license=openapi.License(name="GNU General Public License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    
    path('create', views.createView),
    path('store',views.store,name='store'),
    path('index',views.index),
    path('', views.index),
    path('view/<int:pk>',views.viewPT, name='viewPT'),
    path('delete/<int:pk>',views.deletePT, name='deletePT'),
    path('update/<int:pk>',views.updatePT, name='updatePT'),
    path('edit/<int:pk>',views.update, name='edit'),
    path('api', views.PhonebookViews.as_view()),
    path('api/<int:id>', views.PhonebookIDViews.as_view()),
    re_path(r'^swagger/$', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui')
]