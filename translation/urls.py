from django.urls import path
from . import views

app_name = "translation"
urlpatterns = [
    path("", views.call_chat_gpt_api, name="call_chat_gpt_api"),
]
