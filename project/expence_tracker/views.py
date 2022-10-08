# -*- coding: utf-8 -*-
from telnetlib import STATUS
from django.utils import timezone
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from django.db import transaction
from rest_framework.views import APIView
import json

from expence_tracker.models import ExpenseTracker
from expence_tracker.constants import prepare_date_time

# Create your views here.


class InitialExpenceDetails(APIView):

    authentication_classes = []
    permission_classes = []

    def post(self, request):
        payloads = request.data
        createdDate = prepare_date_time(payloads.get('createDate')) if payloads.get(
            'createDate') else timezone.now()
        expenseDic = payloads.get('data')
        amount = float(expenseDic.get('amount'))
        category = expenseDic.get('category')
        description = expenseDic.get('description')
        paymentType = expenseDic.get('paymentType')

        if not all([amount, category, description, paymentType]):
            return JsonResponse({'message': 'You are missing with data, Please try again!!'},
                                status=500)
        try:
            with transaction.atomic():
                ExpenseTracker.objects.create(
                    amount=amount,
                    category=category,
                    description=description,
                    paymentType=paymentType,
                    create_date=createdDate
                )
                return JsonResponse({'message': 'Expenses has been successfully save !!'},
                                    status=200)

        except Exception as e:
            return JsonResponse({'message': 'Something went wrong!!'}, status=500)

    def get(self, request):
        data = request.GET
        selectedDate = data.get('dateTime').split(',') if (
            data.get('dateTime') != 'undefined') else timezone.now()
        startDate = prepare_date_time(selectedDate[0])
        endDate = prepare_date_time(selectedDate[1])

        try:
            expenseTrackerObj = ExpenseTracker.objects.filter(
                create_date__range=(startDate, endDate)
            )\
            .values('amount', 'category', 'description', 'paymentType', 'create_date')\
            .order_by('-id')
            return JsonResponse({'message': 'successfully!!', 'expensesListObj': list(expenseTrackerObj)},
                                safe=False,status=200)
        except Exception as e:
            return JsonResponse({'message': 'faild while getting data!!'},
                                status=200)
