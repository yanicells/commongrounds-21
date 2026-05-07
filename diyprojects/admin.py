from django.contrib import admin

from .models import Project, ProjectCategory, Favorite, ProjectRating, ProjectReview


class ProjectCategoryAdmin(admin.ModelAdmin):
    model = ProjectCategory


class ProjectAdmin(admin.ModelAdmin):
    model = Project


class FavoriteAdmin(admin.ModelAdmin):
    model = Favorite


class ProjectRatingAdmin(admin.ModelAdmin):
    model = ProjectRating


class ProjectReviewAdmin(admin.ModelAdmin):
    model = ProjectReview


admin.site.register(ProjectCategory, ProjectCategoryAdmin)
admin.site.register(Project, ProjectAdmin)
admin.site.register(Favorite, FavoriteAdmin)
admin.site.register(ProjectRating, ProjectRatingAdmin)
admin.site.register(ProjectReview, ProjectReviewAdmin)
