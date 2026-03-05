from django.db import models
from django.urls import reverse


class CommissionType(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()

    class Meta:
        ordering = ['name']

    def __str__(self):
        return f'{self.name}'


class Commission(models.Model):
    title = models.CharField(max_length=255)
    commission_type = models.ForeignKey(
        CommissionType,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )
    description = models.TextField()
<<<<<<< HEAD
    people_required = models.PositiveIntegerField()
=======
    people_required = models.IntegerField()
>>>>>>> 9693708 (fix: urls and missing model field)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.title}'

    def get_absolute_url(self):
        return reverse('commissions:request-detail', args=[str(self.pk)])

    class Meta:
        ordering = ['created_on']
