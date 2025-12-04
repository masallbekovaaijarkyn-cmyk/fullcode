from django.db import models

# Для учеников
class StudentApplication(models.Model):
    full_name = models.CharField("Имя", max_length=255)
    last_name = models.CharField("Фамилия", max_length=255, blank=True, null=True)
    age = models.IntegerField("Возраст", blank=True, null=True)
    language = models.CharField("Язык", max_length=255, blank=True, null=True)
    phone_number = models.CharField("Телефон", max_length=20)

    def __str__(self):
        return self.full_name

# Для работы
class JobApplication(models.Model):
    full_name = models.CharField("Имя", max_length=255)
    last_name = models.CharField("Фамилия", max_length=255, blank=True, null=True)
    age = models.IntegerField("Возраст", blank=True, null=True)
    previous_position = models.CharField("Кем работал", max_length=255, blank=True, null=True)
    desired_position = models.CharField("Кем хочет работать", max_length=255, blank=True, null=True)
    phone_number = models.CharField("Телефон", max_length=20)
    social_network = models.CharField("Соц сеть", max_length=255, blank=True, null=True)

    def __str__(self):
        return self.full_name

class Contact(models.Model):
    name = models.CharField(max_length=255)
    phone = models.CharField(max_length=20)
    message = models.TextField()

    def __str__(self):
        return self.name