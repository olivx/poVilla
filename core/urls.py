from django.urls import path
from . import views
app_name = 'core'
urlpatterns = [
    path('', views.index, name='home'),
    path('mailbag-list', views.mailbag_list, name='mailbag-list'),
    path('mailbag-create', views.mailbag_create, name='mailbag-create'),
    path('mailbag-delete/<pk>', views.mailbag_delete,  name='mailbag-delete'),
    path('mailbag-detail/<pk>', views.mailbag_details, name='mailbag-details'), 

    path('po-add/<mailbag_pk>', views.pod_add, name='po-add'),
    path('po-edit/<pk>/<mailbag_pk>', views.pod_edit, name='po-edit'),
    path('po-list/<mailbag_pk>', views.pod_list, name='po-list'),

]
