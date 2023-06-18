from django.urls import path
from event.views import EventListView, TicketPurchaseView, PurchaseConfirmationView, \
    EventDetailView, EventSearchView, IndexView

urlpatterns = [
    path('', IndexView.as_view(), name='index-page'),
    path('events/', EventListView.as_view(), name='event-list'),
    path('events/<int:pk>', EventDetailView.as_view(), name='detail-view'),
    path('search/', EventSearchView.as_view(), name='event-search'),
    path('events/<int:pk>/purchase/', TicketPurchaseView.as_view(), name='ticket-purchase'),
    path('event/<int:pk>/purchase/confirmation/', PurchaseConfirmationView.as_view(), name='purchase-confirmation')
]


