from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, LogoutView
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.views.generic import DeleteView, CreateView, UpdateView
from django.views.generic.base import View
from django.urls import reverse_lazy

from FakeCSVproject.app.forms import SchemaForm, ColumnForm
from FakeCSVproject.app.models import Schema, Column, Dataset
from FakeCSVproject.app.tasks import generate_csv_file


class MyLoginView(LoginView):
    form_class = AuthenticationForm
    redirect_authenticated_user = True
    template_name = 'login.html'


class MyLogoutView(LogoutView):
    next_page = '/'


class SchemasView(LoginRequiredMixin, View):
    login_url = 'login'

    def get(self, request):
        schemas = Schema.objects.filter(user=request.user)
        context = {
            'schemas': schemas,
        }
        return render(request, 'schemas.html', context=context)


class SchemaDeleteView(LoginRequiredMixin, DeleteView):
    login_url = 'login'
    model = Schema
    template_name = 'schema_confirm_delete.html'
    success_url = reverse_lazy('schemas')


class SchemaUpdateView(LoginRequiredMixin, UpdateView):
    login_url = 'login'
    model = Schema
    form_class = SchemaForm
    template_name = 'edit_schema.html'

    def get_context_data(self, **kwargs):
        columns = Column.objects.filter(schema=self.object).order_by('order')
        context = super(SchemaUpdateView, self).get_context_data(**kwargs)
        context['columns'] = columns
        return context

    def get_success_url(self):
        return reverse_lazy('add_columns', kwargs={'id_schema': self.object.id})


class SchemaCreateView(LoginRequiredMixin, CreateView):
    login_url = 'login'
    model = Schema
    form_class = SchemaForm
    template_name = 'create_schema.html'

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['is_add'] = True
        return kwargs

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(SchemaCreateView, self).form_valid(form)

    def get_success_url(self):
        return reverse_lazy('add_columns', kwargs={'id_schema': self.object.id})


class ColumnCreateView(LoginRequiredMixin, CreateView):
    login_url = 'login'
    model = Column
    form_class = ColumnForm
    template_name = 'create_column.html'

    def get_success_url(self):
        return reverse_lazy('add_columns', kwargs={'id_schema': self.kwargs['id_schema']})

    def form_valid(self, form):
        obj = form.save(commit=False)
        obj.schema = Schema.objects.get(pk=self.kwargs['id_schema'])
        obj.save()
        return super(ColumnCreateView, self).form_valid(form)

    def get_context_data(self, **kwargs):
        schema = Schema.objects.get(pk=self.kwargs['id_schema'])
        columns = Column.objects.filter(schema=schema).order_by('order')
        context = super(ColumnCreateView, self).get_context_data(**kwargs)
        context['columns'] = columns
        return context

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['is_add'] = True
        return kwargs


class ColumnDeleteView(LoginRequiredMixin, DeleteView):
    login_url = 'login'
    model = Column
    template_name = 'column_confirm_delete.html'

    def get_success_url(self):
        schema = Schema.objects.filter(columns__id=self.object.id).first()
        return reverse_lazy('add_columns', kwargs={'id_schema': schema.id})


class ColumnUpdateView(LoginRequiredMixin, UpdateView):
    login_url = 'login'
    model = Column
    form_class = ColumnForm
    template_name = 'edit_column.html'

    def get_success_url(self):
        schema = Schema.objects.filter(columns__id=self.object.id).first()
        return reverse_lazy('add_columns', kwargs={'id_schema': schema.id})


class DatasetsView(LoginRequiredMixin, View):
    login_url = 'login'

    def get(self, request):
        datasets = Dataset.objects.filter(user=request.user).order_by('-id')
        context = {
            'datasets': datasets,
        }
        return render(request, 'datasets.html', context=context)


class DatasetDeleteView(LoginRequiredMixin, DeleteView):
    login_url = 'login'
    model = Dataset
    template_name = 'dataset_confirm_delete.html'
    success_url = reverse_lazy('datasets')


@login_required
def create_datasets(request):
    if request.method == 'POST':
        raws = int(request.POST.get('input-rows'))
        user = request.user
        schemas = Schema.objects.filter(user=user)
        for schema in schemas:
            dataset = Dataset.objects.create(user=user, schema=schema)
            generate_csv_file.apply_async(args=[schema.id, raws, dataset.id])
        return HttpResponseRedirect(reverse_lazy('datasets'))
    return HttpResponseRedirect(reverse_lazy('datasets'))


@login_required()
def check_status(request):
    if request.method == 'GET':
        parameters_dict = dict(request.GET.lists())
        data = []
        if not parameters_dict:
            return JsonResponse(data, safe=False)
        all_dataset_id = parameters_dict['all_dataset_id[]']
        for dataset_id in all_dataset_id:
            dataset = Dataset.objects.get(id=int(dataset_id))
            data_dataset_id = {
                'dataset_id': dataset_id,
                'dataset_status': dataset.status
            }
            if dataset.status == 'Ready':
                data_dataset_id['csv_file'] = str(dataset.csv_file)
            data.append(data_dataset_id)
        return JsonResponse(data, safe=False)
