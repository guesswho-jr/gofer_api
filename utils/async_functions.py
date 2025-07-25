from rest_framework.response import Response
from django.http import JsonResponse
from asgiref.sync import sync_to_async

Response = sync_to_async(Response)
JSONResponseAsync = sync_to_async(JsonResponse)