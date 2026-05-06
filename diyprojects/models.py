from django.db import models
from django.urls import reverse
from accounts.models import Profile
from django.core.validators import MaxValueValidator, MinValueValidator


class ProjectCategory(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()

    class Meta:
        ordering = ['name']
        verbose_name_plural = 'Project categories'

    def __str__(self):
        return f'{self.name}'


class Project(models.Model):
    title = models.CharField(max_length=255)
    category = models.ForeignKey(
        ProjectCategory,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )
    creator = models.ForeignKey(
        Profile,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )
    description = models.TextField()
    materials = models.TextField()
    steps = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_on']

    def __str__(self):
        return f'{self.title}'

    def get_absolute_url(self):
        return reverse("diyprojects:project-detail", args=[str(self.pk)])


class Favorite(models.Model):
    project = models.ForeignKey(
        Project,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )
    profile = models.ForeignKey(
        Profile,
        on_delete=models.CASCADE
    )
    date_favorited = models.DateField(auto_now_add=True)
    status =  models.CharField(
        max_length=20,
        choices =
        [('Backlog', 'Backlog'),
        ('To-Do', 'To-Do'),
        ('Done', 'Done'),
        ],
        default='Backlog'
    )

    class Meta:
        unique_together = ('project', 'profile')

    def __str__(self):
        return f"{self.profile} - {self.project} ({self.status})"


class ProjectReview(models.Model):
    project = models.ForeignKey(
        Project,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        )
    reviewer = models.ForeignKey(
        Profile,
        on_delete=models.CASCADE
    )
    comment = models.TextField()
    image = models.ImageField(
        upload_to='diyprojects/project_review/', blank=True, null=True)

    def __str__(self):
        return f"{self.reviewer} - {self.project} ({self.comment})"


class ProjectRating(models.Model):
    project = models.ForeignKey(
        Project,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        )
    profile = models.ForeignKey(
        Profile,
        on_delete=models.CASCADE
    )
    score = models.IntegerField(
        validators = [
            MinValueValidator(1),
            MaxValueValidator(10)
        ]
    )

    def __str__(self):
        return f"{self.profile} - {self.project} ({self.score})"
