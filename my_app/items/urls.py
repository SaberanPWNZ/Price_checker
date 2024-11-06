from django.contrib import admin
from django.urls import path, include

from items.views import ItemCreateView

urlpatterns = [
    path('create/', ItemCreateView.as_view(), name='item-create'),

]