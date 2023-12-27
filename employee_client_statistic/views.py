from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from employee_client_statistic.models import Employee, Client, Order
from django.db.models import Sum
from datetime import datetime

from employee_client_statistic.serializers import EmployeeSerializer, ClientSerializer


class EmployeeStatistics(APIView):
    """
    Retrieve statistics for a specific employee.

    Parameters:
    - pk: ID of the employee.
    - month: (optional) Month for filtering (default: 1).
    - year: (optional) Year for filtering (default: current year).

    Example:
    /statistics/employee/1/?month=1&year=2023
    """

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter('month', in_=openapi.IN_QUERY, type=openapi.TYPE_INTEGER,
                              description='Month for filtering (default: 1)'),
            openapi.Parameter('year', in_=openapi.IN_QUERY, type=openapi.TYPE_INTEGER,
                              description='Year for filtering (default: current year)'),
        ],
        responses={200: EmployeeSerializer()},
    )
    def get(self, request, id, format=None):
        try:
            employee = Employee.objects.get(id=id)
        except Employee.DoesNotExist:
            return Response({"error": "Employee not found"}, status=status.HTTP_404_NOT_FOUND)

        month = int(request.query_params.get('month', 1))
        year = int(request.query_params.get('year', datetime.now().year))

        orders = Order.objects.filter(employee=employee, date__month=month, date__year=year) \
            .prefetch_related('products')

        total_products_sold = orders.aggregate(total_products=Sum('products__quantity'))['total_products']
        total_clients = orders.values('client').distinct().count()
        total_sales = orders.aggregate(total_sales=Sum('price'))['total_sales']

        result = {
            "full_name": employee.full_name,
            "total_clients": total_clients,
            "total_products_sold": total_products_sold,
            "total_sales": total_sales
        }

        return Response(result)


class AllEmployeesStatistics(APIView):

    def get(self, request, format=None):
        month = int(request.query_params.get('month', 1))
        year = int(request.query_params.get('year', datetime.now().year))

        employees = Employee.objects.all()
        employee_statistics = []

        orders = Order.objects.filter(date__month=month, date__year=year) \
            .select_related('employee') \
            .prefetch_related('employee__orders', 'employee__orders__products')

        for employee in employees:
            employee_orders = [order for order in orders if order.employee == employee]
            total_products_sold = orders.aggregate(total_products=Sum('products__quantity'))['total_products']
            total_clients = len(set(order.client for order in employee_orders))
            total_sales = sum(order.price for order in employee_orders)

            employee_stat = {
                "id": employee.id,
                "full_name": employee.full_name,
                "total_clients": total_clients,
                "total_products_sold": total_products_sold,
                "total_sales": total_sales
            }

            employee_statistics.append(employee_stat)

        return Response(employee_statistics)


class ClientStatistics(APIView):
    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter('month', in_=openapi.IN_QUERY, type=openapi.TYPE_INTEGER,
                              description='Month for filtering (default: 1)'),
            openapi.Parameter('year', in_=openapi.IN_QUERY, type=openapi.TYPE_INTEGER,
                              description='Year for filtering (default: current year)'),
        ],
        responses={200: ClientSerializer()},
    )
    def get(self, request, id, format=None):
        try:
            client = Client.objects.get(id=id)
        except Client.DoesNotExist:
            return Response({"error": "Client not found"}, status=status.HTTP_404_NOT_FOUND)

        month = int(request.query_params.get('month', 1))
        year = int(request.query_params.get('year', datetime.now().year))

        orders = Order.objects.filter(client=client, date__month=month, date__year=year) \
            .prefetch_related('products')

        total_products_bought = orders.aggregate(total_products=Sum('products__quantity'))['total_products']
        total_sales = orders.aggregate(total_sales=Sum('price'))['total_sales']

        result = {
            "id": client.id,
            "full_name": client.full_name,
            "total_products_bought": total_products_bought,
            "total_sales": total_sales
        }

        return Response(result)
