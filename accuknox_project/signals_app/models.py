from django.db import models


class TestModel(models.Model):
    """Simple model to test signals with post_save."""
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name
