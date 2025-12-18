from django.http import HttpResponse
from django.contrib.auth.hashers import make_password


def healtCheck(request):
  return HttpResponse("Server is running, 200", status=200)
