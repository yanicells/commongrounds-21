from django.db import models
from django.urls import reverse
from accounts.models import Profile


class CommissionType(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()

    class Meta:
        ordering = ['name']

    def __str__(self):
        return f'{self.name}'


class Commission(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    commission_type = models.ForeignKey(
        CommissionType,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )
    maker = models.ForeignKey(Profile, on_delete=models.CASCADE)
    people_required = models.PositiveIntegerField()
    status = models.CharField(max_length=10,
                              choices=['Open', 'Full'],
                              default="Open")
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.title}'

    def get_absolute_url(self):
        return reverse('commissions:request-detail', args=[str(self.pk)])

    class Meta:
        ordering = ['created_on']


class Job(models.Model):
    commission = models.ForeignKey(Commission, on_delete=models.CASCADE)
    role = models.CharField(max_length=255)
    manpower_required = models.PositiveIntegerField()
    status = models.CharField(max_length=10,
                              choices=['Open', 'Full'],
                              default="Open")
    applied_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.role}'

    class Meta:
        ordering = ['-status', 'role']
