# Accuknox Django Trainee Assignment

## Project Setup

1. Make sure you have Python 3 and Django installed.
2. Navigate to the project folder:
   ```
   cd accuknox_project
   ```
3. Run migrations:
   ```
   python manage.py migrate
   ```

## Topic 1: Django Signals

### How to Run

After running migrations, use these commands to test each question:

```
python manage.py test_question1
python manage.py test_question2
python manage.py test_question3
```

### Question 1: Are Django signals synchronous or asynchronous?

**Answer:** By default, Django signals are **synchronous**.

I proved this by adding a `time.sleep(3)` inside the signal handler. If signals were async, the `.save()` call would return right away. But it waits for the full 3 seconds, which means the signal blocks the caller until it finishes.

### Question 2: Do Django signals run in the same thread?

**Answer:** Yes, Django signals run in the **same thread** as the caller.

I proved this by printing `threading.current_thread().ident` both in the caller and inside the signal handler. Both IDs are the same, so the signal is not running in any separate thread.

### Question 3: Do Django signals run in the same database transaction?

**Answer:** Yes, Django signals run in the **same database transaction** as the caller.

I proved this by wrapping `.save()` inside `transaction.atomic()` and checking `connection.in_atomic_block` inside the signal handler — it returns `True`. Also, if I raise an exception after the save inside the atomic block, the whole thing rolls back and the object is not saved. This proves they share the same transaction.

---

## Topic 2: Custom Classes in Python (Rectangle)

### How to Run

```
python rectangle.py
```

### Expected Output

```
Iterating over Rectangle instance:
{'length': 10}
{'width': 5}

Iterating again to show it works repeatedly:
{'length': 10}
{'width': 5}
```

### Explanation

The `Rectangle` class uses `__iter__` method with `yield` to make it iterable. When we loop over a Rectangle object, it first gives `{'length': value}` and then `{'width': value}`.
