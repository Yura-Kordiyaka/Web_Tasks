from django.urls import path
from .views import OrderView, CartView, OrderListView, OrderDetailView

urlpatterns = [
    path('cart/', CartView.as_view(), name='cart'),
    path('order/', OrderView.as_view(), name='order'),
    path('order/list/', OrderListView.as_view(), name='order-list'),
    path('order/<int:id>/', OrderDetailView.as_view(), name='order-detail'),
]
