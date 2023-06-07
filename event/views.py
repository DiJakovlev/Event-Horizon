from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.shortcuts import render, get_object_or_404
from django.views import View
from datetime import date
from event.models import Event


class IndexView(View):
    template_name = 'index_page'

    def get(self, request):
        search_query = request.GET.get('search_query')
        event_date = request.GET.get('event_date')

        events = Event.objects.filter(start_date__gte=date.today())

        if search_query and event_date:
            events = events.filter(Q(name__icontains=search_query) & Q(start_date=event_date))
        elif search_query:
            events = events.filter(name__icontains=search_query)
        elif event_date:
            events = events.filter(start_date=event_date)

        context = {
            'events': events,
            'search_query': search_query,
            'event_date': event_date
        }

        return render(request, self.template_name, context)


class EventListView(View):
    template_name = 'event_list'

    def get(self, request):
        events = Event.objects.all()

        context = {
            'events': events
        }

        return render(request, self.template_name, context)


class EventView(View):
    template_name = 'event_detail'

    def get(self, request, event_id):
        events = get_object_or_404(Event, id=event_id)

        context = {
            'events': events
        }

        return render(request, self.template_name, context)


class TicketPurchaseView(LoginRequiredMixin, View):
    template_name = 'ticket_purchase'

    def get(self, request, event_id):
        event = Event.objects.get(id=event_id)

        context = {
            'event': event
        }

        return render(request, self.template_name, context)


class PurchaseConfirmationView(LoginRequiredMixin, View):
    template_name = 'purchase_conformation'

    def get(self, request):
        return render(request, self.template_name)
