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
    maker = models.ForeignKey(Profile,
                              on_delete=models.CASCADE,
                              related_name='commissions')
    people_required = models.PositiveIntegerField(default=1)
    status = models.CharField(max_length=10,
                              choices=[('0', 'Open'), ('1', 'Full')],
                              default='0')
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.title}'

    def get_absolute_url(self):
        return reverse('commissions:commission-detail', args=[str(self.pk)])

    class Meta:
        ordering = ['created_on']


class Job(models.Model):
    commission = models.ForeignKey(
        Commission, on_delete=models.CASCADE, related_name='jobs')
    role = models.CharField(max_length=255)
    manpower_required = models.PositiveIntegerField(default=1)
    open_positions = models.IntegerField()
    status = models.CharField(max_length=10,
                              choices=[('0', 'Open'), ('1', 'Full')],
                              default='0')
    applied_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.commission.title}'

    class Meta:
        ordering = ['status', '-manpower_required', 'role']


class JobApplication(models.Model):
    job = models.ForeignKey(Job, on_delete=models.CASCADE,
                            related_name='applications')
    applicant = models.ForeignKey(Profile,
                                  on_delete=models.CASCADE,
                                  related_name='application')
    status = models.CharField(max_length=10,
                              choices=[('0', 'Pending'),
                                       ('1', 'Accepted'),
                                       ('2', 'Rejected')],
                              default='0')
    applied_on = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['status', '-applied_on']
