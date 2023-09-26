from django.urls import path
from main.views import show_main, create_item, show_xml, show_json, show_xml_by_id, show_json_by_id, register, login_user, logout_user
from main.views import add_amount, sub_amount, delete_item

app_name = 'main'

urlpatterns = [
    path('', show_main, name='show_main'),
    path('add-amount/<int:id>/',add_amount, name='add_amount'),
    path('sub-amount/<int:id>/',sub_amount, name='sub_amount'),
    path('delete_item/<int:id>/',delete_item, name='delete_item'),
    path('logout/', logout_user, name='logout'),
    path('login/', login_user, name='login'),
    path('create-item', create_item, name='create_item'),
    path('xml/', show_xml, name='show_xml'),
    path('json/', show_json, name='show_json'), 
    path('xml/<int:id>/', show_xml_by_id, name='show_xml_by_id'),
    path('json/<int:id>/', show_json_by_id, name='show_json_by_id'), 
    path('register/', register, name='register'), #sesuaikan dengan nama fungsi yang dibuat
]