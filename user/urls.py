from django.contrib import admin
from django.urls import path

from user.views import RegisterView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', RegisterView.as_view(), name='homepage')
]