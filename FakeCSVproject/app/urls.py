from django.urls import path

from FakeCSVproject.app.views import MyLoginView, SchemasView, MyLogoutView, SchemaDeleteView, SchemaCreateView, \
    ColumnCreateView, SchemaUpdateView, ColumnDeleteView, ColumnUpdateView, DatasetsView, create_datasets, \
    DatasetDeleteView, check_status

urlpatterns = [
    path('login/', MyLoginView.as_view(), name='login'),
    path('logout/', MyLogoutView.as_view(), name='logout'),
    path('', SchemasView.as_view(), name='schemas'),
    path('delete/<pk>/', SchemaDeleteView.as_view(), name='delete_schema'),
    path('edit/<pk>/', SchemaUpdateView.as_view(), name='edit_schema'),
    path('create/', SchemaCreateView.as_view(), name='create_schema'),
    path('create/<id_schema>/add_columns/', ColumnCreateView.as_view(), name='add_columns'),
    path('delete_column/<pk>/', ColumnDeleteView.as_view(), name='delete_column'),
    path('edit_column/<pk>/', ColumnUpdateView.as_view(), name='edit_column'),
    path('datasets/', DatasetsView.as_view(), name='datasets'),
    path('delete_dataset/<pk>/', DatasetDeleteView.as_view(), name='delete_dataset'),
    path('create_datasets/', create_datasets, name='create_datasets'),
    path('check_status/', check_status, name='check_status'),
]
