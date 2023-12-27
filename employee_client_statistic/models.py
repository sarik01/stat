from django.db import models


class Employee(models.Model):
    full_name = models.CharField(max_length=100)
    birthdate = models.DateField()

    objects = models.Manager()

    def __str__(self):
        return self.full_name


class Client(models.Model):
    full_name = models.CharField(max_length=100)
    birthdate = models.DateField()

    objects = models.Manager()

    def __str__(self):
        return self.full_name


class Product(models.Model):
    name = models.CharField(max_length=100)
    quantity = models.IntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)

    objects = models.Manager()

    def __str__(self):
        return self.name


class Order(models.Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE, related_name='orders')
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name='orders')
    products = models.ManyToManyField(Product)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateField()

    objects = models.Manager()

    def __str__(self):
        return f"Order {self.id} by {self.employee.full_name} for {self.client.full_name}"
