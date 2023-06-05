from django.urls import path

from event.views import IndexView, EventListView, TicketPurchaseView, PurchaseConfirmationView, EventView

urlpatterns = [
    path('', IndexView.as_view(), name='main-page'),
    path('events/', EventListView.as_view(), name='event-list'),
    path('events/<int:pk>', EventView.as_view(), name='detail-view'),
    path('events/<int:pk>/purchase/', TicketPurchaseView.as_view(), name='ticket-purchase'),
    path('event/<int:pk>/purchase/conformation/', PurchaseConfirmationView.as_view(), name='purchase-conformation')
]