from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import redirect_to_login
from django.shortcuts import get_object_or_404, redirect, render
from django.views.generic import CreateView, DetailView, ListView

from accounts.decorators import role_required
from accounts.mixins import RoleRequiredMixin

from .forms import ProductForm, TransactionForm
from .models import Product, Transaction


class ProductListView(ListView):
    model = Product
    template_name = 'merchstore/product_list.html'
    context_object_name = 'products'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user.is_authenticated and hasattr(self.request.user, 'profile'):
            context['my_products'] = Product.objects.filter(
                owner=self.request.user.profile)
            context['all_products'] = Product.objects.exclude(
                owner=self.request.user.profile)
        else:
            context['all_products'] = Product.objects.all()
        return context


class ProductDetailView(DetailView):
    model = Product
    template_name = 'merchstore/product_detail.html'
    context_object_name = 'product'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = TransactionForm()
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()

        if not request.user.is_authenticated:
            return redirect_to_login(request.get_full_path())

        form = TransactionForm(request.POST)
        if form.is_valid():
            transaction = form.save(commit=False)

            if self.object.owner == request.user.profile:
                form.add_error(None, "You cannot purchase your own product.")

            elif transaction.amount > self.object.stock:
                form.add_error('amount', "Not enough stock available.")

            else:
                transaction.buyer = request.user.profile
                transaction.product = self.object
                transaction.status = 'On cart'

                self.object.stock -= transaction.amount
                if self.object.stock == 0:
                    self.object.status = 'Out of stock'

                self.object.save()
                transaction.save()
                return redirect('merchstore:cart')

        context = self.get_context_data()
        context['form'] = form
        return self.render_to_response(context)


class ProductCreateView(RoleRequiredMixin, CreateView):
    model = Product
    form_class = ProductForm
    template_name = 'merchstore/product_form.html'
    required_role = 'Market Seller'

    def form_valid(self, form):
        product = form.save(commit=False)
        product.owner = self.request.user.profile
        if product.stock == 0:
            product.status = 'Out of stock'
        product.save()
        return redirect(product.get_absolute_url())


@role_required('Market Seller')
def product_update_view(request, pk):
    product = get_object_or_404(Product, pk=pk)

    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            updated_product = form.save(commit=False)

            if updated_product.stock == 0:
                updated_product.status = 'Out of stock'
            elif updated_product.status == 'Out of stock' and updated_product.stock > 0:
                updated_product.status = 'Available'

            updated_product.save()
            return redirect(updated_product.get_absolute_url())
    else:
        form = ProductForm(instance=product)

    return render(request, 'merchstore/product_form.html', {'form': form, 'product': product})


class CartView(LoginRequiredMixin, ListView):
    model = Transaction
    template_name = 'merchstore/cart.html'

    def get_queryset(self):
        return Transaction.objects.filter(buyer=self.request.user.profile).order_by('product__owner')


class TransactionListView(LoginRequiredMixin, ListView):
    model = Transaction
    template_name = 'merchstore/transaction_list.html'

    def get_queryset(self):
        return Transaction.objects.filter(product__owner=self.request.user.profile).order_by('buyer')
