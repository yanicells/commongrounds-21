
from django.contrib.auth.views import redirect_to_login
from django.shortcuts import get_object_or_404, redirect, render
from django.db.models import Avg
from django.views.generic import CreateView, DetailView, ListView

from accounts.decorators import role_required
from accounts.mixins import RoleRequiredMixin

from .forms import ProjectForm, ProjectRatingForm, ProjectReviewForm, FavoriteForm
from .models import Project, ProjectReview, ProjectRating, Favorite


class ProjectListView(ListView):
    model = Project
    template_name = 'diyprojects/project_list.html'
    context_object_name = 'projects'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user.is_authenticated and hasattr(self.request.user, 'profile'):
            profile = self.request.user.profile
            context['created_projects'] = Project.objects.filter(
                creator=profile)
            context['favorited_projects'] = Project.objects.filter(
                favorite__profile=profile)
            context['reviewed_projects'] = Project.objects.filter(
                projectreview__reviewer=profile).distinct()
            context['all_projects'] = Project.objects.exclude(
                creator=profile
            ).exclude(
                favorite__profile=profile
            ).exclude(
                projectreview__reviewer=profile
            )

        else:
            context['created_projects'] = Project.objects.none()
            context['favorited_projects'] = Project.objects.none()
            context['reviewed_projects'] = Project.objects.none()
            context['all_projects'] = Project.objects.all()

        return context


class ProjectDetailView(DetailView):
    model = Project
    template_name = 'diyprojects/project_detail.html'
    context_object_name = 'project'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['average_rating'] = ProjectRating.objects.filter(
            project=self.get_object()
        ).aggregate(Avg('score'))['score__avg']

        context['reviews'] = ProjectReview.objects.filter(
            project=self.get_object())
        context['review_form'] = ProjectReviewForm()
        context['rating_form'] = ProjectRatingForm()
        context['favorite_form'] = FavoriteForm()
        context['favorite_count'] = Favorite.objects.filter(
            project=self.get_object()
        ).count()

        if self.request.user.is_authenticated:
            context['is_favorited'] = Favorite.objects.filter(
                project=self.get_object(),
                profile=self.request.user.profile
            ).exists()
            context['favorites'] = Favorite.objects.filter(
                project=self.get_object(),
                profile=self.request.user.profile
            ).first()

        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        action = request.POST.get('action')

        if not request.user.is_authenticated:
            return redirect_to_login(request.get_full_path())

        if action == 'favorite':
            favorite = Favorite.objects.filter(
                project=self.object,
                profile=request.user.profile
            ).first()

            form = FavoriteForm(request.POST, instance=favorite)

            if form.is_valid():
                favorite = form.save(commit=False)
                favorite.project = self.object
                favorite.profile = request.user.profile
                favorite.save()

            return redirect(request.path)

        elif action == 'unfavorite':
            favorite = Favorite.objects.filter(
                project=self.object,
                profile=request.user.profile
            )

            if favorite.exists():
                favorite.delete()

            return redirect(request.path)

        elif action == 'review':
            form = ProjectReviewForm(request.POST, request.FILES)

            if form.is_valid():
                review = form.save(commit=False)
                review.project = self.object
                review.reviewer = request.user.profile
                review.save()

            return redirect(request.path)

        elif action == 'rate':
            rating = ProjectRating.objects.filter(
                project=self.object, profile=request.user.profile).first()
            form = ProjectRatingForm(request.POST, instance=rating)

            if form.is_valid():
                rating = form.save(commit=False)
                rating.project = self.object
                rating.profile = request.user.profile
                rating.save()

            return redirect(request.path)

        return redirect(request.path)


class ProjectCreateView(RoleRequiredMixin, CreateView):
    model = Project
    form_class = ProjectForm
    template_name = 'diyprojects/project_form.html'
    required_role = 'Project Creator'

    def form_valid(self, form):
        project = form.save(commit=False)
        project.creator = self.request.user.profile
        project.save()
        return redirect(project.get_absolute_url())


@role_required('Project Creator')
def project_update_view(request, pk):
    project = get_object_or_404(Project, pk=pk)

    if request.method == 'POST':
        form = ProjectForm(request.POST, instance=project)

        if form.is_valid():
            updated_project = form.save(commit=False)
            updated_project.creator = project.creator
            updated_project.save()
            return redirect(updated_project.get_absolute_url())

    else:
        form = ProjectForm(instance=project)

    return render(request, 'diyprojects/project_form.html', {'form': form, 'project': project})
