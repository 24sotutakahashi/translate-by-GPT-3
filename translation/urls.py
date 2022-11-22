from django.urls import path
from . import views

app_name = "translation"
urlpatterns = [
    path("", views.Translation_and_Summary, name="Translation_and_Summary"),
]
