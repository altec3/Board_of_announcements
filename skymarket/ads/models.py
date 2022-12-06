from django.db import models

from users.models import User


class Ad(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length=200)
    description = models.TextField(max_length=1000, blank=True)
    price = models.PositiveIntegerField()
    author = models.ForeignKey(User, related_name="ads", on_delete=models.CASCADE)
    image = models.ImageField(upload_to="ads/%Y/%m/%d/", null=True)

    class Meta:
        verbose_name = "Объявление"
        verbose_name_plural = "Объявления"
        ordering = ['created_at']

    def __str__(self):
        return self.title

    @property
    def phone(self):
        return str(self.author.phone) if self.author.phone else None

    @property
    def author_first_name(self):
        return self.author.first_name if self.author.first_name else None

    @property
    def author_last_name(self):
        return self.author.last_name if self.author.last_name else None


class Comment(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    ad = models.ForeignKey(Ad, related_name="comments", on_delete=models.CASCADE)
    text = models.TextField(max_length=1000)
    author = models.ForeignKey(User, related_name="comments", on_delete=models.SET_NULL, null=True)

    class Meta:
        verbose_name = "Комментарий"
        verbose_name_plural = "Комментарии"
        ordering = ['created_at']

    def __str__(self):
        text = str(self.text)
        return text if len(text) <= 20 else text[:20] + "..."
