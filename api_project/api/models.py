from django.db import models

class GeneratedAns(models.Model):
    topic = models.CharField(max_length=256)
    content = models.TextField()
    # created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.topic

