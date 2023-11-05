from django.shortcuts import render
from util import MQTTMessageReceiver
from .models import registered_data
from django.contrib import messages
import json,time
from django.http import JsonResponse
from paho.mqtt.client import Client
from fpdf import FPDF
mqtt_messages = []
data=[]
def on_message(client, userdata, msg):
    message = msg.payload.decode("utf-8")
    print(message)
    mqtt_messages.append(message)

def connect_to_mqtt():
    client = Client()
    client.on_message = on_message
    client.connect("192.168.225.13", 1883, 60)
    client.subscribe("authentic")
    client.loop_start()


# Create your views here.
def index(request):
    connect_to_mqtt()
    return render(request,"index.html")

def registration(request):
    if request.method == "POST":
        first_name=request.POST.get("first_name")
        last_name=request.POST.get("last_name")
        email=request.POST.get("email")
        phone=request.POST.get("contact_no")
        description=request.POST.get("description")
        uid=mqtt_messages[-1]
        registered_data.objects.create(first_name=first_name, last_name=last_name, email=email, uid=uid,
                                 description=description,phone=phone)
        mqtt_messages.pop()
        messages.success(request, f"Form Submitted Successfully \n {first_name}{last_name} your card id is {uid}")
    return render(request,"registration.html")



def scanning(request):
    if request.method=="POST":
        request.session["file_name"]=request.POST.get("file_name")
        request.session["event_name"]=request.POST.get("event_name")
        request.session["date"]=request.POST.get("date")
        request.session["venue"]=request.POST.get("venue")
        messages.success(request, f"File Created Successfully with name {request.session['file_name']}")
    return render(request,"scanning.html")

def process(request):
    file_name=request.session["file_name"]
    event_name=request.session["event_name"]
    date=request.session["date"]
    venue=request.session["venue"]
    return render(request,"process.html",{'file_name':file_name,'event_name':event_name,'date':date,'venue':venue})

def get_messages(request):
    return JsonResponse({'messages': mqtt_messages})


def pdf_creator(request):
    class PDF(FPDF):
        def header(self):
            self.image("Manipal_University.png",0,0,100)
            self.ln(20)
    pdf=PDF('P','mm','A4')
    pdf.add_page()
    pdf.set_font("helvetica","B",20)
    pdf.set_auto_page_break(auto=True,margin=15)
    pdf.cell(0,10,f"{request.session['event_name']}",align="C",ln=1)
    pdf.set_font("helvetica","", 16)
    pdf.cell(0,20, f"{request.session['venue']}",align="C",ln=1)
    pdf.set_font("helvetica", "", 12)
    pdf.cell(0,20, f"Date -->{request.session['date']}",align="L",ln=1)
    pdf.set_font("helvetica","",8)
    for i in mqtt_messages:
        results = registered_data.objects.raw(f"select id,first_name,last_name,email,description from attendance_registered_data where uid='{i}';")
        pdf.cell(40,10,f"{results[0].first_name} {results[0].last_name}",align="L")
        pdf.cell(90,10,f"{results[0].email}",align="L")
        pdf.cell(60,10,f"{results[0].description}",ln=1,align="L")
    pdf.output(f"{request.session['file_name']}.pdf")
    return JsonResponse({'messages': "Success"})

