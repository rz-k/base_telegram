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

class Message(models.Model):

    name = models.CharField(max_length=100, null=True, blank=True, db_index=True)

    text = models.TextField(null=True, blank=True)

    def __str__(self) -> str:
        return f"{self.name}"

class ChannelSponsor(models.Model):

    name = models.CharField(max_length=70,null=True,blank=True)

    chat_id = models.CharField(max_length=70,unique=True,null=True,blank=True)

    link = models.CharField(max_length=70,unique=True)

    other = models.BooleanField(default=False,null=True,blank=True)

    def __str__(self) -> str:
        return self.name
