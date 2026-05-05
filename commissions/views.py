from django.views.generic import DetailView, ListView, CreateView, UpdateView
from django.shortcuts import redirect
from django.urls import reverse_lazy
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
            commission.maker = Profile.objects.get(user=request.user)
            commission.save()

            job = job_form.save(commit=False)
            job.commission = commission
            job.save()

            return redirect(self.success_url)
        else:
            self.object_list = self.get_queryset(**kwargs)
            context = self.get_context_data(**kwargs)
            context['commission_form'] = commission_form
            context['job_form'] = job_form
            return self.render_to_response(context)


class CommissionUpdateView(UpdateView, RoleRequiredMixin):
    pass
