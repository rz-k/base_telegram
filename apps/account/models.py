from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _


class User(AbstractUser):

    user_id = models.BigIntegerField(
        unique=True,
        verbose_name=_("user id")
    )

    step = models.CharField(
        max_length=30,
        default="home",
        verbose_name=_("current step")
    )

    is_send_ads = models.BooleanField(
        default=False,
        verbose_name=_("Advertising status")
    )

    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = ["user_id"]

    def __str__(self):
        return str(self.user_id)
