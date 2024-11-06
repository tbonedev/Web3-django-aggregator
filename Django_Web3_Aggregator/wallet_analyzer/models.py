from django.db import models

# Create your models here.
class Wallet(models.Model):
    class Meta:
        ordering = ('id', )
        verbose_name = 'Wallet'
    address = models.CharField(max_length=255)

    def __str__(self) -> str:
        return f"{self.address}"