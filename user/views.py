from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.views import View
from user.forms import UserRegisterForm
from event.models import Ticket


class RegisterView(View):
    def get(self, request):
        form = UserRegisterForm()
        return render(request, 'event/registration_page.html', {'form': form})

    def post(self, request):
        form = UserRegisterForm(request.POST)

        if form.is_valid():
            form.save()
            return redirect('index')

        return render(request, 'event/registration_page.html', {'form': form})


class ProfileView(LoginRequiredMixin, View):
    template_name = 'event/profile_page.html'

    def get(self, request):
        user = request.user
        tickets = Ticket.objects.filter(user=user)

        context = {
            'user': user,
            'tickets': tickets
        }

        return render(request, self.template_name, context)
