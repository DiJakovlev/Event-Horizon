from django.contrib.auth import logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.views import View
from .forms import UserRegisterForm


class RegisterView(View):
    def get(self, request):
        form = UserRegisterForm()
        return render(request, 'users/homepage.html', {'form': form})

    def post(self, request):
        form = UserRegisterForm(request.POST)

        if form.is_valid():
            form.save()
            return redirect('index')


# class ProfileView(LoginRequiredMixin, View):
#     template_name = 'user_profile'

#     def get(self, request):
#         user = request.user
#         tickets = Ticket.objects.filter(user=user)

#         context = {
#             'user': user,
#             'tickets': tickets
#         }

#         return render(request, self.template_name, context)
