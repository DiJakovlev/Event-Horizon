from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, get_object_or_404, redirect
from .models import Event, Ticket
from django.views import View
from user.forms import TicketPurchaseForm
import requests

"""Page view classes"""


class IndexView(View):
    template_name = 'event/index_page.html'

    def get(self, request):
        all_events = {}

        if 'event_id' in request.GET:
            event_id = request.GET.get('event_id')
            url = f'https://www.eventbriteapi.com/v3/events/{event_id}/?token=HYQLBZQMBFLBRTL3PQJE'

            try:
                response = requests.get(url)
                response.raise_for_status()  # Raise an exception for non-successful status codes
                data = response.json()

                if not data:
                    raise ValueError("Empty response body")

                event = data
                event_data, created = Event.objects.update_or_create(
                    event_id=event_id,
                    defaults={
                        'name': event.get('name', {}).get('text'),
                        'summary': event.get('summary'),
                        'description': event.get('description', {}).get('text'),
                        'url': event.get('url'),
                        'start_date': event.get('start', {}).get('utc'),
                        'end': event.get('end', {}).get('utc'),
                        'currency': event.get('currency'),
                        'online_event': event.get('online_event'),
                        'listed': event.get('listed'),
                        'shareable': event.get('shareable'),
                        'capacity': event.get('capacity'),
                        'event_logo': event.get('logo', {}).get('original', {}).get('url')
                    }
                )
                event_data.save()
                all_events = Event.objects.filter(event_id=event_id).first()

            except requests.exceptions.HTTPError as error:
                # Handle HTTP errors (e.g., 404, 500)
                print(f"HTTP error occurred: {error}")
                # Add appropriate error handling or response as needed
            except requests.exceptions.RequestException as error:
                # Handle request exceptions (e.g., connection error, timeout, invalid URL)
                print(f"Request failed: {error}")
                # Add appropriate error handling or response as needed

            except ValueError as error:
                # Handle the case when the response body is empty
                print(f"Empty response body: {error}")
                # Add appropriate error handling or response as needed

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
    def get(self, request):
        form = TicketPurchaseForm

        return render(request, 'event/ticket_purchase.html', {'form': form})

    def post(self, request):
        form = TicketPurchaseForm
        if form.is_valid:
            event = form.cleaned_data['event']
            quantity = form.cleaned_data['quantity']

            for _ in range(quantity):
                ticket = Ticket(user=request.user, event=event)
                ticket.save()

            return redirect('purchase-conformation')

        return render(request, 'event/ticket_purchase.html', {'form': form})


class PurchaseConfirmationView(LoginRequiredMixin, View):
    template_name = 'purchase_confirmation.html'

    def get(self, request):
        return render(request, self.template_name)
