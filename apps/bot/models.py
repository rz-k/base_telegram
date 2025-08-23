from django.db import models


class BotUpdateStatus(models.Model):
    is_update = models.BooleanField(
        default=False
    )
    update_msg = models.TextField(default="bot is updated !")

    def save(self, *args, **kwargs):
        self.id = 1
        return super().save(*args, **kwargs)

    def __str__(self):
        return str(f"Bot status is: {self.is_update}")
