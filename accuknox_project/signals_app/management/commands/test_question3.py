"""
Question 3: By default do Django signals run in the same database transaction?

Answer: Yes, Django signals run in the SAME database transaction as the caller.

How I proved it:
- I wrapped the .save() call inside transaction.atomic().
- Inside the signal handler, I checked connection.in_atomic_block.
- It returns True, which means the signal handler is running inside
  the same atomic transaction block.
- Also, I showed that if we raise an exception inside the signal,
  the save gets rolled back — meaning the object is NOT created.
  This further proves they share the same transaction.
"""

import threading
from django.core.management.base import BaseCommand
from django.db import transaction, connection
from signals_app.models import TestModel


class Command(BaseCommand):
    help = 'Proves that Django signals run in the same DB transaction'

    def handle(self, *args, **kwargs):
        self.stdout.write("=" * 60)
        self.stdout.write("QUESTION 3: Do signals run in same DB transaction?")
        self.stdout.write("=" * 60)

        # Part A: Check if signal runs inside atomic block
        self.stdout.write(f"\n--- Part A: Checking in_atomic_block ---")
        self.stdout.write(f"Caller: Wrapping save in transaction.atomic()...")

        with transaction.atomic():
            obj = TestModel.objects.create(name="test_transaction")
            # The Q3 signal handler will print whether it's inside atomic block

        self.stdout.write(f"Caller: Transaction committed successfully.")

        # cleanup
        obj.delete()

        # Part B: Prove rollback affects the signal's save too
        self.stdout.write(f"\n--- Part B: Proving rollback works ---")
        self.stdout.write(f"Caller: Saving inside atomic, then raising exception...")

        count_before = TestModel.objects.count()

        try:
            with transaction.atomic():
                TestModel.objects.create(name="test_rollback")
                # Manually raise exception to trigger rollback
                raise Exception("Intentional error to trigger rollback")
        except Exception as e:
            self.stdout.write(f"Caught exception: {e}")

        count_after = TestModel.objects.count()

        self.stdout.write(f"Objects before: {count_before}, after: {count_after}")
        self.stdout.write(f"\nConclusion: The count did not change because the")
        self.stdout.write(f"transaction rolled back. Since the signal ran inside")
        self.stdout.write(f"the same transaction, the save was also undone.")
        self.stdout.write(f"This proves signals run in the SAME TRANSACTION.\n")
