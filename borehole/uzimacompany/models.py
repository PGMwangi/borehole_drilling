from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Registration(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=100)
    address = models.CharField(max_length=200)
    telephone = models.CharField(max_length=15)
    borehole_location = models.CharField(max_length=200)
    id_number = models.CharField(max_length=20)

    def __str__(self):
        return self.id_number

class Billing(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    client_category = models.CharField(max_length=100)
    drilling_type = models.CharField(max_length=100)
    pump_type = models.CharField(max_length=100)
    depth_height = models.CharField(max_length=100)
    tax_amount = models.DecimalField(max_digits=10, decimal_places=2)
    total_fees = models.DecimalField(max_digits=10, decimal_places=2)
    plumbing_cost = models.DecimalField(max_digits=10, decimal_places=2)
    total_revenue = models.DecimalField(max_digits=10, decimal_places=2)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    
    def __str__(self):
        return self.client_category

    # def __str__(self):
    #     if self.registration:
    #         return f"Billing - {self.registration.id_number}"
    #     else:
    #         return "Billing - No registration"
        

# class Payment(models.Model):
#     # Define the possible client categories
#     INDUSTRIAL = 'Industrial'
#     COMMERCIAL = 'Commercial'
#     DOMESTIC = 'Domestic'
    
#     CLIENT_CATEGORY_CHOICES = [
#         (INDUSTRIAL, 'Industrial'),
#         (COMMERCIAL, 'Commercial'),
#         (DOMESTIC, 'Domestic'),
#     ]
    
#     # Define the fields for the Payment model
#     user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='payments')
#     client_category = models.CharField(
#         max_length=10,
#         choices=CLIENT_CATEGORY_CHOICES,
#         default=DOMESTIC  # Set a default client category
#     )
#     survey_fees = models.DecimalField(max_digits=10, decimal_places=2)
#     authority_fees = models.DecimalField(max_digits=10, decimal_places=2)
#     payment_date = models.DateTimeField(auto_now_add=True)  # Automatically sets the date and time of the payment

#     # Define the string representation of the model
#     def __str__(self):
#         return f"{self.user.username} - {self.client_category} - {self.payment_date}"
