from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, get_object_or_404
from .models import Event
from django.views import View
import requests


"""Page view classes"""


class IndexView(View):
    template_name = 'event/index_page.html'

    def get(self, request):
        all_events = {}
        if 'event_id' in request.GET:
            event_id = request.GET['event_id']
            url = f'https://www.eventbriteapi.com/v3/events/{event_id}/?token=HYQLBZQMBFLBRTL3PQJE'
            response = requests.get(url)
            data = response.json()

            if 'event' in data:
                event = data['event']

                event_data = Event(
                    name=event['name']['text'],
                    summary=event['summary']['text'],
                    description=event['description']['text'],
                    url=event['url'],
                    start_date=event['start']['utc'],
                    end_date=event['end']['utc'],
                    currency=event['currency'],
                    online_event=event['online_event'],
                    listed=event['listed'],
                    shareable=event['shareable'],
                    capacity=event['capacity'],
                    event_logo=event['logo']['original']['url']
                )
                event_data.save()
                all_events = Event.objects.all().order_by('-id')
            else:
                # Handle the case when 'event' key is missing in the response
                # Add appropriate error handling or response as needed
                pass

        return render(request, self.template_name, {"all_events": all_events})


class EventListView(View):
    template_name = 'event_list.html'

    def get(self, request):
        events = Event.objects.all()

        context = {
            'events': events
        }

        return render(request, self.template_name, context)


class EventView(View):
    template_name = 'event_detail.html'

    def get(self, request, event_id):
        events = get_object_or_404(Event, id=event_id)

        context = {
            'events': events
        }

        return render(request, self.template_name, context)


class TicketPurchaseView(LoginRequiredMixin, View):
    template_name = 'ticket_purchase.html'

    def get(self, request, event_id):
        event = Event.objects.get(id=event_id)

        context = {
            'event': event
        }

        return render(request, self.template_name, context)


class PurchaseConfirmationView(LoginRequiredMixin, View):
    template_name = 'purchase_confirmation.html'

    def get(self, request):
        return render(request, self.template_name)




