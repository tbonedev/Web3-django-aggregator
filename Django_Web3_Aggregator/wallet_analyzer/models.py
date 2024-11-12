from django.db import models

# Create your models here.
class Wallet(models.Model):
    address = models.CharField(max_length=255)


    class Meta:
        ordering = ('id', )
        verbose_name = 'Wallet'

    def __str__(self) -> str:
        return f"{self.address}"