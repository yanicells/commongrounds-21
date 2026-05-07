from django.views.generic import DetailView, ListView, CreateView, UpdateView
from django.shortcuts import redirect
from django.contrib.auth.views import redirect_to_login
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
                maker=self.request.user.profile).order_by('status', '-created_on')
            context['applied'] = Commission.objects.filter(
                jobs__applications__applicant=self.request.user.profile).distinct().order_by('status', '-created_on')
            context['commission_list'] = Commission.objects.all().exclude(
                jobs__applications__applicant=self.request.user.profile).exclude(
                maker=self.request.user.profile).distinct().order_by('status', '-created_on')

        else:
            context['commission_list'] = Commission.objects.all().order_by(
                'status', '-created_on')
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
            pk=self.object.pk, jobs__applications__status='1').count()
        context['open_manpower'] = total_manpower - total_existing_manpower
        return context

    def post(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect_to_login(request.get_full_path())

        self.object = self.get_object()

        job_id = request.POST.get('button')

        if job_id:
            job = Job.objects.get(id=job_id)

            if job.applications.filter(applicant=request.user.profile).exists():
                return redirect('commissions:commission-detail', pk=self.object.pk)

            accepted = job.applications.filter(status='1').count()

            if accepted >= job.manpower_required:
                job.applications.create(
                    applicant=self.request.user.profile,
                    status='2')
            else:
                job.applications.create(
                    applicant=self.request.user.profile,
                    status='1')

        accepted = job.applications.filter(status='1').count()
        job.open_positions = job.manpower_required - accepted
        job.save()
        if job.open_positions <= 0:
            job.status = '1'
        job.save()
        if job.commission.status == '0' and not job.commission.jobs.filter(status='0').exists():
            job.commission.status = '1'
        job.commission.save()
        return redirect('commissions:commission-detail', pk=self.object.pk)


class JobCreateView(RoleRequiredMixin, CreateView):
    model = Job
    template_name = 'commissions/commission_update.html'
    form_class = JobForm
    required_role = 'Commission Maker'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = JobForm()
        context['field'] = Commission.objects.get(id=self.kwargs['pk'])
        return context

    def post(self, request, *args, **kwargs):
        job_form = JobForm(request.POST)
        if job_form.is_valid():
            job = job_form.save(commit=False)
            job.commission = Commission.objects.get(id=self.kwargs['pk'])
            job.commission.people_required += job.manpower_required
            job.commission.status = '0'
            job.open_positions = job.manpower_required
            job.save()
            job.commission.save()

            return redirect("commissions:commission-detail", pk=self.kwargs['pk'])
        else:
            self.object_list = self.get_queryset(**kwargs)
            context = self.get_context_data(**kwargs)
            context['form'] = job_form
            return self.render_to_response(context)


class CommissionCreateView(RoleRequiredMixin, CreateView):
    model = Commission
    template_name = 'commissions/commission_create.html'
    form_class = CommissionForm
    success_url = reverse_lazy('commissions:commission-list')
    required_role = 'Commission Maker'

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
                total=Sum('manpower_required')
            )["total"]
            commission.save()

            return redirect(commission.get_absolute_url())
        else:
            self.object_list = self.get_queryset(**kwargs)
            context = self.get_context_data(**kwargs)
            context['commission_form'] = commission_form
            context['job_form'] = job_form
            return self.render_to_response(context)


class CommissionUpdateView(RoleRequiredMixin, UpdateView):
    model = Commission
    template_name = 'commissions/commission_update.html'
    form_class = CommissionForm
    context_object_name = 'field'
    required_role = 'Commission Maker'

    def form_valid(self, form):
        commission = form.save(commit=False)
        if commission.status == '0' and not commission.jobs.filter(status='0').exists():
            commission.status = '1'
        commission.save()
        return redirect(commission.get_absolute_url())
