import time
import threading
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import TestModel


# Question 1: Are Django signals synchronous or asynchronous?

# Answer: By default, Django signals are executed SYNCHRONOUSLY.
# This means the signal handler runs completely before the code 
# after the .save() call continues.



@receiver(post_save, sender=TestModel)
def question1_handler(sender, instance, **kwargs):
    """Signal handler that sleeps for 3 seconds to prove synchronous behavior."""
    print(f"[Q1] Signal started for: {instance.name}")
    time.sleep(3)
    print(f"[Q1] Signal finished after sleeping 3 seconds")


# Question 2: Do Django signals run in the same thread?

# Answer: Yes, by default Django signals run in the SAME THREAD
# as the caller. 



@receiver(post_save, sender=TestModel)
def question2_handler(sender, instance, **kwargs):
    """Signal handler that prints thread ID to prove same-thread execution."""
    print(f"[Q2] Signal handler thread ID: {threading.current_thread().ident}")
    print(f"[Q2] Signal handler thread name: {threading.current_thread().name}")


# Question 3: Do Django signals run in the same database transaction?

# Answer: Yes, by default Django signals (like post_save) run in the
# SAME database transaction as the caller.


from django.db import connection, transaction


@receiver(post_save, sender=TestModel)
def question3_handler(sender, instance, **kwargs):
    """Signal handler that checks if it runs inside the same DB transaction."""
    print(f"[Q3] Inside atomic block? {connection.in_atomic_block}")
