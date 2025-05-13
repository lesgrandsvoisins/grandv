from django.db import models

class Application(models.Model):
    title = models.CharField(max_length=100)
    source_name = models.CharField(max_length=100)
    description = models.TextField()
    icon = models.CharField(max_length=100, help_text="CSS class or icon name")
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.title
