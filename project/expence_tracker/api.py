from datetime import datetime, timedelta
from functools import reduce
from django.http import HttpResponse, JsonResponse
from django.http import HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa
from expence_tracker.models import ExpenseTracker
from expence_tracker.constants import prepare_date_time


def get_dash_board_details(request):
    ''' Monthly Expenses '''
    try:
        todays_date = datetime.today()
        today_expenses = get_expenses_obj()
        weekly_expenses = get_expenses_obj(todays_date-timedelta(days=7))
        one_month_ago = get_expenses_obj(todays_date-timedelta(days=30))
        one_year_ago = get_expenses_obj(todays_date-timedelta(days=30*12))
        all_expenses = [today_expenses, weekly_expenses,
                        one_month_ago, one_year_ago]
        return JsonResponse({'dashBoardData': all_expenses}, status=200)
    except Exception as e:
        return HttpResponse('something went wrong!!')


def get_expenses_obj(dateTime=datetime.today()-timedelta(days=1)):
    _expense_obj = ExpenseTracker.objects.filter(
        create_date__range=(dateTime, datetime.today())
    )
    if not _expense_obj.exists():
        return {
            'onOfExpense': 0,
            'totalAmout': 0
        }
    _total_amount = reduce(lambda sum, val: sum + val,
                           [_obj.amount for _obj in _expense_obj])
    _info = {
        'onOfExpense': len(_expense_obj),
        'totalAmout': _total_amount
    }
    return _info


def get_expenses_according_item(item, filterItem):
    params = {filterItem: item}
    _expense_tracker_obj = ExpenseTracker.objects.filter(
        **params
    )
    return _expense_tracker_obj


def get_expenses_by_date(startDate, endDate):

    pass


def render_pdf_view(request):
    data = request.GET
    item_type = data.get('value')
    filter_type = data.get('type')
    dateTime = data.get('datetime')

    if dateTime == 'null':
        _context_obj = get_expenses_according_item(item_type, filter_type)
    else:
        _ls = dateTime.split(',')
        startDate = prepare_date_time(_ls[0])
        endDate = prepare_date_time(_ls[1])
        filterItem = 'create_date__range'
        item = (startDate, endDate)
        _context_obj = get_expenses_according_item(item, filterItem)

    template_path = 'expence_tracker/generatePdf.html'
    context = {'context_obj': _context_obj}
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="report.pdf"'
    template = get_template(template_path)
    html = template.render(context)
    pisa_status = pisa.CreatePDF(
        html, dest=response)
    if pisa_status.err:
        return HttpResponse('We had some errors <pre>' + html + '</pre>')
    return response
