from django.db import models
from django.urls import reverse

# Create your models here.

class Mail(models.Model):
    message_id = models.CharField(max_length=20)
    thread_id = models.CharField(max_length=20)
    snippet = models.TextField(null=True)
    
    def __str__(self):
        return self.message_id


# class Response
#     reply_email
#     reply_text



class ErrorLog(models.Model):
    status_code = models.PositiveIntegerField(null=True)
    error_stack = models.TextField(null=True)

    def __str__(self):
        return f"{self.status_code} - {self.error_stack[:100]}"
    
    def get_absolute_url(self):
        return reverse("errors_detail_view", args=[self.pk])