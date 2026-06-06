import time
import threading
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import TestModel


# ============================================================
# Question 1: Are Django signals synchronous or asynchronous?
# ============================================================
# Answer: By default, Django signals are executed SYNCHRONOUSLY.
# This means the signal handler runs completely before the code 
# after the .save() call continues.
#
# To prove this, I added a time.sleep(3) inside the signal handler.
# If signals were async, the save() would return immediately without
# waiting. But as we can see from the output, the total time taken
# is more than 3 seconds, which proves the signal blocks the caller.
# ============================================================


@receiver(post_save, sender=TestModel)
def question1_handler(sender, instance, **kwargs):
    """Signal handler that sleeps for 3 seconds to prove synchronous behavior."""
    print(f"[Q1] Signal started for: {instance.name}")
    time.sleep(3)
    print(f"[Q1] Signal finished after sleeping 3 seconds")


# ============================================================
# Question 2: Do Django signals run in the same thread?
# ============================================================
# Answer: Yes, by default Django signals run in the SAME THREAD
# as the caller. 
#
# To prove this, I printed the thread ID inside the signal handler
# and compared it with the thread ID printed just before calling 
# .save(). Both thread IDs are the same, which proves they run 
# in the same thread.
# ============================================================


@receiver(post_save, sender=TestModel)
def question2_handler(sender, instance, **kwargs):
    """Signal handler that prints thread ID to prove same-thread execution."""
    print(f"[Q2] Signal handler thread ID: {threading.current_thread().ident}")
    print(f"[Q2] Signal handler thread name: {threading.current_thread().name}")


# ============================================================
# Question 3: Do Django signals run in the same database transaction?
# ============================================================
# Answer: Yes, by default Django signals (like post_save) run in the
# SAME database transaction as the caller.
#
# To prove this, I used transaction.atomic() while saving. Inside the
# signal handler, I check if we are currently inside an atomic block
# using connection.in_atomic_block. It returns True, which proves 
# the signal is running within the same transaction.
#
# Also, if I raise an error inside the signal handler after save,
# the whole transaction rolls back and the object is NOT saved in
# the database. This further proves same-transaction behavior.
# ============================================================


from django.db import connection, transaction


@receiver(post_save, sender=TestModel)
def question3_handler(sender, instance, **kwargs):
    """Signal handler that checks if it runs inside the same DB transaction."""
    print(f"[Q3] Inside atomic block? {connection.in_atomic_block}")
