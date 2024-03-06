from wagtail.snippets.models import register_snippet
from wagtail.snippets.views.snippets import SnippetViewSet, SnippetViewSetGroup


from ledger.models import Ledger


class LedgerSnippetViewSet(SnippetViewSet):
    model = Ledger
    menu_label = "Ledger"  # ditch this to use verbose_name_plural from model
    icon = "group"  # change as required
    # list_display = ("first_name", "last_name", "job_title", "thumb_image")
    # list_filter = {
    #     "job_title": ["icontains"],
    # }
    # list_export = ("first_name", "last_name", "job_title")



class LedgerSnippetViewSetGroup(SnippetViewSetGroup):
    menu_label = "Ledger"
    menu_icon = "utensils"  # change as required
    menu_order = 300  # will put in 4th place (000 being 1st, 100 2nd)
    items = (LedgerSnippetViewSet,)


register_snippet(LedgerSnippetViewSetGroup)