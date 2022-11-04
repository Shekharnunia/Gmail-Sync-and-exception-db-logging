"""inbox_utility URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from gmail_messages import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path("sync/", views.SyncMail.as_view(), name="sync_mail"),
    path("mails/", views.MailList.as_view(), name="mail_list"),
    path("support/", views.SupportMail.as_view(), name="support"),
    path("errors/<int:pk>/delete/", views.ErrorLogDelete.as_view(), name="errors_delete_view"),
    path("errors/<int:pk>/", views.ErrorLogDetail.as_view(), name="errors_detail_view"),
    path("errors/", views.ErrorLogList.as_view(), name="errors_list"),
    path("test/", views.messages_list_test, name="message_list_test"),
    path("", views.messages_list, name="message_list"),
]
