import django_filters
from b2c_client_orders.models import B2COrder
from orders.models import City


class B2COrderFilter(django_filters.FilterSet):
    status = django_filters.CharFilter(field_name='status', lookup_expr='exact')
    order_date = django_filters.DateFilter(field_name='order_date', lookup_expr='exact')
    phone_number_client = django_filters.CharFilter(field_name='phone_number_client', lookup_expr='icontains')
    phone_number_employee = django_filters.CharFilter(field_name='assigned_employees__user__phone', lookup_expr='icontains')
    city = django_filters.ModelChoiceFilter(queryset=City.objects.all(), field_name='city', lookup_expr='exact')

    # order_time = django_filters.TimeFilter(field_name='order_time', lookup_expr='exact')
    # order_name = django_filters.CharFilter(field_name='order_name', lookup_expr='icontains')
    # address = django_filters.CharFilter(field_name='address', lookup_expr='icontains')
    # name_client = django_filters.CharFilter(field_name='name_client', lookup_expr='icontains')
    # price = django_filters.NumberFilter(field_name='price', lookup_expr='exact')


    class Meta:
        model = B2COrder
        fields = ['status',
                  'order_date',
                  'phone_number_client',
                  'phone_number_employee',
                 ]
