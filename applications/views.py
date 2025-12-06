import os
import json
import datetime
import requests
from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status
from .models import StudentApplication, JobApplication, Contact
from .serializers import StudentApplicationSerializer, JobApplicationSerializer, ContactSerializer


LOG_DIR = "logs"
LOG_FILE = os.path.join(LOG_DIR, "api_logs.json")

if not os.path.exists(LOG_DIR):
    os.makedirs(LOG_DIR)

def write_log(method, path, status_code, data=None):
    log_entry = {
        "time": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "method": method,
        "path": path,
        "status": status_code,
        "data": data
    }

    logs = []
    if os.path.exists(LOG_FILE):
        try:
            with open(LOG_FILE, "r", encoding="utf-8") as f:
                content = f.read()
                logs = json.loads(content) if content.strip() else []
        except json.JSONDecodeError:
            logs = []

    logs.append(log_entry)

    with open(LOG_FILE, "w", encoding="utf-8") as f:
        json.dump(logs, f, indent=4, ensure_ascii=False)



TELEGRAM_BOT_TOKEN = "8554504621:AAEBFe9_0u_RtgH_PoGK4zbfKhL8eZX1bJ4"
TELEGRAM_CHAT_ID = "-5003090635"

def send_to_telegram(message):
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": TELEGRAM_CHAT_ID,
        "text": message,
        "parse_mode": "HTML"
    }
    requests.post(url, data=payload)






class StudentApplicationCreateView(generics.CreateAPIView):
    queryset = StudentApplication.objects.all()
    serializer_class = StudentApplicationSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)

        data = serializer.validated_data

        message = (
            f"📚 Новая заявка ученика:\n"
            f"Имя: {data['full_name']}\n"
            f"Фамилия: {data.get('last_name', '-')}\n"
            f"Возраст: {data.get('age', '-')}\n"
            f"Язык: {data.get('language', '-')}\n"
            f"Телефон: {data['phone_number']}"
        )
        send_to_telegram(message)

        write_log("POST", request.path, 201, request.data)

        return Response(serializer.data, status=status.HTTP_201_CREATED)




class JobApplicationCreateView(generics.CreateAPIView):
    queryset = JobApplication.objects.all()
    serializer_class = JobApplicationSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)

        data = serializer.validated_data

        message = (
            f"🧑‍💼 Новая заявка на работу:\n"
            f"Имя: {data['full_name']}\n"
            f"Фамилия: {data.get('last_name', '-')}\n"
            f"Возраст: {data.get('age', '-')}\n"
            f"Кем работал: {data.get('previous_position', '-')}\n"
            f"Кем хочет работать: {data.get('desired_position', '-')}\n"
            f"Телефон: {data['phone_number']}\n"
            f"Соц сеть: {data.get('social_network', '-')}"
        )
        send_to_telegram(message)

        write_log("POST", request.path, 201, request.data)

        return Response(serializer.data, status=status.HTTP_201_CREATED)




class ContactListCreateAPIView(generics.ListCreateAPIView):
    queryset = Contact.objects.all()
    serializer_class = ContactSerializer

    def list(self, request, *args, **kwargs):
        response = super().list(request, *args, **kwargs)

        # LOG
        write_log("GET", request.path, 200)

        return response

    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)

        # LOG
        write_log("POST", request.path, response.status_code, request.data)

        return response
