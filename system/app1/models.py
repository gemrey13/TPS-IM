from django.db import models
from django.contrib.auth.models import User


class ScrapType(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name

class ScrapItem(models.Model):
    RFID = models.CharField(max_length=100, unique=True)
    weight = models.DecimalField(max_digits=10, decimal_places=2)
    scrap_type = models.ForeignKey(ScrapType, on_delete=models.CASCADE)

    def __str__(self):
        return f"RFID: {self.RFID}, Type: {self.scrap_type}, Weight: {self.weight} kg"

class DailyScrapEntry(models.Model):
    date = models.DateField()
    scraps = models.ManyToManyField(ScrapItem, through='ScrapEntryDetail')

    def __str__(self):
        return f"Date: {self.date}"

class ScrapEntryDetail(models.Model):
    daily_scrap_entry = models.ForeignKey(DailyScrapEntry, on_delete=models.CASCADE)
    scrap_item = models.ForeignKey(ScrapItem, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"Daily Scrap Entry: {self.daily_scrap_entry}, Scrap Item: {self.scrap_item}, Quantity: {self.quantity}"

class Transaction(models.Model):
    date = models.DateField()
    scraps = models.ManyToManyField(ScrapItem, through='TransactionDetail')

    def __str__(self):
        return f"Transaction Date: {self.date}"

class TransactionDetail(models.Model):
    transaction = models.ForeignKey(Transaction, on_delete=models.CASCADE)
    scrap_item = models.ForeignKey(ScrapItem, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"Transaction: {self.transaction}, Scrap Item: {self.scrap_item}, Quantity: {self.quantity}"


class UserProfile(models.Model):
    USER_TYPES = (
        ('owner', 'Owner'),
        ('staff', 'Staff'),
    )
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    user_type = models.CharField(max_length=10, choices=USER_TYPES)

    def __str__(self):
        return f"{self.user.username} - {self.user_type}"