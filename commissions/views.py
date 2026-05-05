from django.views.generic import DetailView, ListView, CreateView, UpdateView
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.db.models import Sum
from accounts.mixins import RoleRequiredMixin
from .models import *
from .forms import *


class CommissionListView(ListView):
    model = Commission
    template_name = 'commissions/commission_list.html'
    context_object_name = 'commissions'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            context['created'] = Commission.objects.filter(
                maker=self.request.user.profile)
            context['applied'] = Commission.objects.filter(
                jobs__applications__applicant=self.request.user.profile)
            context['commission_list'] = Commission.objects.all().exclude(
                jobs__applications__applicant=self.request.user.profile).exclude(
                maker=self.request.user.profile).distinct()

        else:
            context['commission_list'] = Commission.objects.all()
        return context


class CommissionDetailView(DetailView):
    model = Commission
    template_name = 'commissions/commission_detail.html'
    context_object_name = 'commission'
    fail_application_url = reverse_lazy('commissions:commission-list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        total_manpower = self.object.jobs.all().aggregate(
            total=Sum("manpower_required")
        )["total"]
        context['total_manpower'] = total_manpower
        total_existing_manpower = Commission.objects.filter(
            pk=self.object.pk, jobs__applications__status="Accepted").distinct().count()
        context['open_manpower'] = total_manpower - total_existing_manpower

        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()

        job_id = request.POST.get("button")

        if job_id:
            job = Job.objects.get(id=job_id)

            if job.applications.filter(applicant=request.user.profile).exists():
                return redirect("commissions:commission-detail", pk=self.object.pk)

            accepted = job.applications.filter(status="Accepted").count()

            if accepted >= job.manpower_required:
                job.applications.create(
                    applicant=self.request.user.profile,
                    status="Rejected")
            else:
                job.applications.create(
                    applicant=self.request.user.profile,
                    status="Accepted")

        accepted = job.applications.filter(status="Accepted").count()
        job.open_positions = job.manpower_required - accepted
        job.save()
        if job.open_positions <= 0:
            job.status = 'Full'
        job.save()
        if not job.commission.jobs.filter(status='Open').exists():
            job.commission.status = 'Full'
            print(job.commission.status)
        job.commission.save()
        print(job.commission.status)
        return redirect("commissions:commission-detail", pk=self.object.pk)


# class JobCreateView(CreateView, RoleRequiredMixin):
#     pass


class CommissionCreateView(CreateView, RoleRequiredMixin):
    model = Commission
    template_name = 'commissions/commission_create.html'
    form_class = CommissionForm
    success_url = reverse_lazy('commissions:commission-list')
    context_object_name = 'field'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['commission_form'] = CommissionForm()
        context['job_form'] = JobForm()
        return context

    def post(self, request, *args, **kwargs):
        commission_form = CommissionForm(request.POST)
        job_form = JobForm(request.POST)
        if commission_form.is_valid() and job_form.is_valid():
            commission = commission_form.save(commit=False)
            job = job_form.save(commit=False)
            job.commission = commission
            commission.maker = Profile.objects.get(user=request.user)
            commission.save()
            job.open_positions = job.manpower_required
            job.save()

            commission.people_required = commission.jobs.all().aggregate(
                total=Sum("manpower_required")
            )["total"]
            commission.save()

            return redirect(self.success_url)
        else:
            self.object_list = self.get_queryset(**kwargs)
            context = self.get_context_data(**kwargs)
            context['commission_form'] = commission_form
            context['job_form'] = job_form
            return self.render_to_response(context)


class CommissionUpdateView(UpdateView, RoleRequiredMixin):
    model = Commission
    template_name = 'commissions/commission_update.html'
    form_class = CommissionForm
    success_url = reverse_lazy('commissions:commission-list')
    context_object_name = 'field'
    # it doesn't make sense to put the status update here because it only update when you update
    # the form so to update it in real time, I added that feature in the detail view
