from django.db import models


class Employee(models.Model):
    DEPARTMENTS = [
        "Engineering", "HR", "Finance", "Marketing",
        "Sales", "Operations", "IT Support",
    ]

    name = models.CharField(max_length=100)
    position = models.CharField(max_length=100)
    email = models.EmailField(blank=True, default="")
    phone = models.CharField(max_length=30, blank=True, default="")
    department = models.CharField(
        max_length=50,
        choices=[(d, d) for d in DEPARTMENTS],
        default="Operations",
    )
    salary = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    is_available = models.BooleanField(default=True)
    date_hired = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["id"]

    def soft_delete(self):
        self.is_available = False
        self.save(update_fields=["is_available"])

    def restore(self):
        self.is_available = True
        self.save(update_fields=["is_available"])

    def __str__(self):
        status = "" if self.is_available else " (inactive)"
        return f"{self.name} - {self.position}{status}"