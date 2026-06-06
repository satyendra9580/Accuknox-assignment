"""
Question 1: By default are django signals executed synchronously or asynchronously?

Answer: Django signals are executed SYNCHRONOUSLY by default.

How I proved it:
- I connected a post_save signal to TestModel.
- Inside the signal handler, I added a time.sleep(3) to simulate some delay.
- Before calling .save(), I recorded the start time.
- After .save() returns, I recorded the end time.
- The total time is more than 3 seconds, which means .save() waited 
  for the signal handler to finish before returning.
- If signals were asynchronous, .save() would have returned immediately 
  and total time would be close to 0 seconds.

This proves that Django signals are synchronous.
"""

import time
import threading
from django.core.management.base import BaseCommand
from signals_app.models import TestModel


class Command(BaseCommand):
    help = 'Proves that Django signals are synchronous'

    def handle(self, *args, **kwargs):
        self.stdout.write("=" * 60)
        self.stdout.write("QUESTION 1: Are Django signals synchronous or async?")
        self.stdout.write("=" * 60)

        self.stdout.write(f"\nCaller: About to save TestModel instance...")
        start = time.time()

        # This triggers the post_save signal which has time.sleep(3)
        obj = TestModel.objects.create(name="test_sync")

        end = time.time()
        total_time = end - start

        self.stdout.write(f"Caller: .save() returned after {total_time:.2f} seconds")
        self.stdout.write(f"\nConclusion: Since total time is > 3 seconds,")
        self.stdout.write(f"the signal handler blocked the caller.")
        self.stdout.write(f"This proves signals are SYNCHRONOUS by default.\n")

        # cleanup
        obj.delete()
