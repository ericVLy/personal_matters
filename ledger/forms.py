from django.forms import ModelForm

from ledger.models import Ledger


class LedgerForm(ModelForm):
    class Meta:
        model = Ledger