from django.db import models

class Application(models.Model):
    title = models.CharField(max_length=100)
    url = models.URLField()
    description = models.TextField()
    icon = models.CharField(max_length=100, help_text="CSS class or icon name <a href='https://feathericons.com/'>feathericons.com</a>")
    is_active = models.BooleanField(default=True)

    def domain(self):
        return self.url[8:]

    def __str__(self):
        return self.title
