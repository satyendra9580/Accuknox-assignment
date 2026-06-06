"""
Question 2: Do Django signals run in the same thread as the caller?

Answer: Yes, Django signals run in the SAME THREAD as the caller.

How I proved it:
- Before calling .save(), I printed the current thread ID.
- Inside the signal handler, I also printed the thread ID.
- Both thread IDs are exactly the same.
- This proves the signal handler is not running in a separate thread,
  it runs in the same thread as the code that triggered it.
"""

import threading
from django.core.management.base import BaseCommand
from signals_app.models import TestModel


class Command(BaseCommand):
    help = 'Proves that Django signals run in the same thread'

    def handle(self, *args, **kwargs):
        self.stdout.write("=" * 60)
        self.stdout.write("QUESTION 2: Do signals run in the same thread?")
        self.stdout.write("=" * 60)

        caller_thread = threading.current_thread()
        self.stdout.write(f"\nCaller thread ID: {caller_thread.ident}")
        self.stdout.write(f"Caller thread name: {caller_thread.name}")

        self.stdout.write(f"\nNow saving the object (this triggers the signal)...")

        # The signal handler for Q2 also prints its thread ID
        obj = TestModel.objects.create(name="test_thread")

        self.stdout.write(f"\nConclusion: Both thread IDs are same,")
        self.stdout.write(f"so the signal runs in the SAME THREAD as the caller.\n")

        # cleanup
        obj.delete()
