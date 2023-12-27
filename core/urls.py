from django.contrib import admin
from django.urls import path
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

from employee_client_statistic.views import EmployeeStatistics, ClientStatistics, \
    AllEmployeesStatistics

schema_view = get_schema_view(
    openapi.Info(
        title="Your API",
        default_version="v1",
        description="Your API description",
        terms_of_service="https://www.yourapp.com/terms/",
        contact=openapi.Contact(email="contact@yourapp.com"),
        license=openapi.License(name="Your License"),
    ),
    public=True,
    permission_classes=[permissions.AllowAny],
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('statistics/employees/', AllEmployeesStatistics.as_view(), name='employee-list'),
    path('statistics/employee/<int:id>/', EmployeeStatistics.as_view(), name='employee-statistics'),
    path('statistics/client/<int:id>/', ClientStatistics.as_view(), name='client-statistics'),
    path('docs/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]
