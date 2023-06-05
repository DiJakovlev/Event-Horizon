from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View


class IndexView(View):
    pass


class EventListView(View):
    pass


class EventView(View):
    pass


class TicketPurchaseView(LoginRequiredMixin, View):
    pass


class PurchaseConfirmationView(LoginRequiredMixin, View):
    pass
