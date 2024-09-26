from django.urls import path
from .views import ItemDetail
from .views import CreateItemView, ReadItemView, UpdateItemView, DeleteItemView

urlpatterns = [
    path('api/items/', CreateItemView.as_view(), name='create_item'),
    path('api/items/<int:item_id>/', ReadItemView.as_view(), name='read_item'),
    path('api/items/<int:item_id>/', UpdateItemView.as_view(), name='update_item'),
    path('api/items/<int:item_id>/', DeleteItemView.as_view(), name='delete_item'),
    path('items/<int:id>/', ItemDetail.as_view(), name='item-detail'),

]
