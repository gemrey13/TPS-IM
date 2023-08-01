from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_delete
from django.dispatch import receiver

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

class Customer(models.Model):
    name = models.CharField(max_length=100)
    contact_number = models.CharField(max_length=20)
    address = models.TextField()

    def __str__(self):
        return self.name

class DailyScrapEntry(models.Model):
    date = models.DateField()
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True, blank=True)
    staff_responsible = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    scraps = models.ManyToManyField(ScrapItem, through='ScrapEntryDetail')

    def __str__(self):
        return f"Date: {self.date}"

class ScrapEntryDetail(models.Model):
    daily_scrap_entry = models.ForeignKey(DailyScrapEntry, on_delete=models.CASCADE)
    scrap_item = models.ForeignKey(ScrapItem, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"Daily Scrap Entry: {self.daily_scrap_entry}, Scrap Item: {self.scrap_item}, Quantity: {self.quantity}"

@receiver(post_delete, sender=ScrapEntryDetail)
def delete_empty_daily_scrap_entry(sender, instance, **kwargs):
    # Check if the related DailyScrapEntry has any other ScrapEntryDetail objects
    has_other_scrap_entries = ScrapEntryDetail.objects.filter(daily_scrap_entry=instance.daily_scrap_entry).exists()

    # If there are no other ScrapEntryDetail objects, delete the DailyScrapEntry
    if not has_other_scrap_entries:
        instance.daily_scrap_entry.delete()

class Transaction(models.Model):
    date = models.DateField()
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True, blank=True)
    staff_responsible = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
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
