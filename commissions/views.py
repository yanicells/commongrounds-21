from django.views.generic import DetailView, ListView

from .models import *


class CommissionListView(ListView):
    model = Commission
    template_name = 'commissions/request_list.html'
    context_object_name = 'commissions'
    # if logged in, show groups--- always show all commissions at the end with the ones in groups filtered out
    # link rin somewhere sa taas to create a commission
    print(Commission.objects.count())

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            # groups
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
    template_name = 'commissions/request_detail.html'
    context_object_name = 'commission'
