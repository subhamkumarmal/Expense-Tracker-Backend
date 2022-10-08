import imp
from django.conf.urls import url
from expence_tracker.api import *
from views import InitialExpenceDetails
urlpatterns = [
    url(r'expense-tracker-details/', InitialExpenceDetails.as_view()),
    url(r'^get-dash-board-details/', get_dash_board_details),
    url(r'^render-pdf-view/',render_pdf_view)
]
