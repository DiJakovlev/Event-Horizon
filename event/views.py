from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import DetailView, ListView
from .models import Event, Ticket
from django.views import View
from user.forms import TicketPurchaseForm
from django.views.generic.edit import FormView
from django import forms
import requests

"""Page view classes"""


class IndexView(LoginRequiredMixin, View):
    template_name = 'event/index_page.html'

    def get(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('user/login-page')
        else:
            return redirect('event-list')


class EventListView(ListView):
    model = Event
    template_name = 'event/event_list.html'


class EventDetailView(DetailView):
    model = Event
    template_name = 'event/event_detail.html'


class EventSearchForm(forms.Form):
    search_term = forms.CharField()


class EventSearchView(FormView):
    template_name = 'event/event_search.html'
    form_class = EventSearchForm

    def form_valid(self, form):

        # Retrieve the cleaned search term from the form
        search_term = form.cleaned_data['search_term']
        self.request.session['search_term'] = search_term

        # Proceed with the form validation using the parent class method
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        # Retrieve the context data from the parent class method
        context = super().get_context_data(**kwargs)

        # Retrieve the search term from the session
        search_term = self.request.session.get('search_term')

        if search_term:
            api_url = f'https://serpapi.com/search.json?engine=google_events&' \
                      f'q={search_term}&api_key=21ef569aeaad22e8351415e6c05f6e9d67277c1030e1be04931672a50229bd38'
            response = requests.get(api_url).json()

            if 'events_results' not in response:
                return context

            required_fields = ['title', 'date', 'address', 'link', 'description', 'venue', 'thumbnail']

            # Empty list to store search results
            search_results = []

            # Iterate over each event data obtained from the API response
            for event_data in response['events_results']:
                # Check if all required fields exist in the event data
                if not all(field in event_data for field in required_fields):
                    continue

                # Extract necessary data for creating or updating the Event object
                venue_name = event_data['venue']['name']
                event_logo = event_data['thumbnail']

                # Use the 'link' field to find unique events and update or create them in the database
                event, created = Event.objects.update_or_create(
                    link=event_data['link'],
                    defaults={
                        'title': event_data['title'],
                        'start_date': event_data['date']['start_date'],
                        'address': ", ".join(event_data['address']),
                        'description': event_data['description'],
                        'venue': venue_name,
                        'event_logo': event_logo,
                    },
                )

                # Add each created/updated event to the search results list
                search_results.append(event)

            # Add the search results to the context
            context['search_results'] = search_results

        return context

    def get_success_url(self):
        # Return the current page URL to stay on the same page after form submission
        return self.request.path


"""Ticket classes"""


class TicketPurchaseView(LoginRequiredMixin, View):
    def get(self, request, pk):
        form = TicketPurchaseForm()
        event = get_object_or_404(Event, pk=pk)
        context = {
            'form': form,
            'event': event,
        }
        return render(request, 'event/ticket_purchase.html', context)

    def post(self, request, pk):
        form = TicketPurchaseForm(request.POST)
        if form.is_valid():
            event = form.cleaned_data['event']
            quantity = form.cleaned_data['quantity']

            for _ in range(quantity):
                ticket = Ticket(user=request.user, event=event)
                ticket.save()

            return redirect('purchase-confirmation', pk=pk)

        context = {
            'form': form,
            'event': get_object_or_404(Event, pk=pk),
        }
        return render(request, 'event/ticket_purchase.html', context)


class PurchaseConfirmationView(LoginRequiredMixin, DetailView):
    model = Event
    template_name = 'event/purchase_confirmation.html'
    context_object_name = 'event'
    pk_url_kwarg = 'pk'
