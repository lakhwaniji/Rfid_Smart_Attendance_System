from django.urls import path
from . import views

urlpatterns=[
    path("",views.index,name='index'),
    path("registration/",views.registration,name="registration"),
    path("scanning/",views.scanning,name="scanning"),
    path("process/",views.process,name="process"),
    path("get_messages/",views.get_messages,name="get_messages"),
    path("create_pdf/",views.pdf_creator,name="pdf_creator")
]