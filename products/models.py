from django.db import models


# Create your models here.
class Product(models.Model):
    CATEGORIES=[
        ('hospital_equipment','Hospital Equipment'),
        ('blood_pressure','Blood Pressure'),
        ('accessories','Accessories'),
        ('personal','Personal')
    ]
    name=models.CharField(max_length=255)
    product_image=models.ImageField(upload_to='product_images/', null=True, blank=True)
    category=models.CharField(max_length=100, choices=CATEGORIES)
    used_for=models.CharField(max_length=255)
    description=models.TextField()
    price=models.DecimalField(max_digits=10,decimal_places=2)
    discount=models.DecimalField(max_digits=5,decimal_places=2,default=0.00)
    sku=models.CharField(max_length=100,unique=True)
    stock_quantity=models.PositiveIntegerField()
    product_ref=models.CharField(max_length=50, unique=True, null=True, blank=True)
    created_at=models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
    
    def get_discounted_price(self):
        if self.discount > 0:
            discounted_price = self.price - (self.price * self.discount / 100)
            return round(discounted_price, 2)
        return self.price
    
    def save(self, *args, **kwargs):
        self.product_ref = f"{self.name.lower().replace(' ', '-')}-{self.sku[:8]}"
        super().save(*args, **kwargs)

    

class AdditionalInformation(models.Model):
    product=models.ForeignKey(Product, on_delete=models.CASCADE, related_name='additional_info')
    key=models.CharField(max_length=100)
    value=models.CharField(max_length=255)

    def __str__(self):
        return f"{self.key}: {self.value}"