from django.shortcuts import render
from django.views.generic import FormView


from .forms import LedgerForm


# Create your views here.


class LedgerFormView(FormView):
    form_class = LedgerForm
