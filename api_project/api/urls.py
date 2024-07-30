from django.urls import path
from . import views

urlpatterns = [
    path('generate-ans/', views.GenerateAnsView.as_view(), name='generate_ans'),
    path('generated-ans-dummy/', views.dummy.as_view(), name='dummy'),
]
