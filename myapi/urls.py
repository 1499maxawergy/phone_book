# myapi/urls.py
from django.urls import include, path
from . import views


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
    path('api/<int:id>', views.PhonebookViews.as_view())
]