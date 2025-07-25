from typing import Any
from django.core.management.base import BaseCommand
from django.utils import timezone
from story.models import Story

class Command(BaseCommand):
    help = "Delete stories everyday"
    def handle(self, *args: Any, **options: Any):
        expiration = timezone.now() - timezone.timedelta(days=1)
        Story.objects.filter(created_at__lt = expiration).delete()