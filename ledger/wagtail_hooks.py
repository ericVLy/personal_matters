from wagtail.snippets.models import register_snippet
from wagtail.snippets.views.snippets import SnippetViewSet, SnippetViewSetGroup, CreateView

from ledger.models import Ledger



class LedgerSnippetsCreateView(CreateView):
    template_name = "templates/wagtailsnippets/snippets/create.html"


class LedgerSnippetViewSet(SnippetViewSet):
    model = Ledger
    add_view_class = LedgerSnippetsCreateView
    menu_label = "Ledger"  # ditch this to use verbose_name_plural from model
    icon = "clipboard-list"  # change as required
    # list_display = ("first_name", "last_name", "job_title", "thumb_image")
    # list_filter = {
    #     "job_title": ["icontains"],
    # }
    list_export = ("transaction_time", 
                   "transaction_category", 
                   "counterparty",
                   "counterparty_account",
                   "product_description",
                   "receipt_disbursement",
                   "amount",
                   "receipt_payment_method",
                   "transaction_status",
                   "transaction_order_number",
                   "merchant_order_number",
                   "remarks"
                   )



class LedgerSnippetViewSetGroup(SnippetViewSetGroup):
    menu_label = "Ledger"
    menu_icon = "folder"  # change as required
    menu_order = 300  # will put in 4th place (000 being 1st, 100 2nd)
    items = (LedgerSnippetViewSet,)


register_snippet(LedgerSnippetViewSetGroup)