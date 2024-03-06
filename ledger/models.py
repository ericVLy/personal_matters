from django.contrib.contenttypes.fields import GenericRelation
from django.db import models
from django.utils.translation import gettext as _
from modelcluster.fields import ParentalKey
from modelcluster.models import ClusterableModel
from wagtail.admin.panels import (
    FieldPanel,
    FieldRowPanel,
    InlinePanel,
    MultiFieldPanel,
    PublishingPanel,
)
from wagtail.contrib.forms.models import AbstractEmailForm, AbstractFormField
from wagtail.contrib.settings.models import (
    BaseGenericSetting,
    BaseSiteSetting,
    register_setting,
)
from wagtail.fields import RichTextField, StreamField
from wagtail.models import (
    Collection,
    DraftStateMixin,
    LockableMixin,
    Page,
    PreviewableMixin,
    RevisionMixin,
    TranslatableMixin,
    WorkflowMixin,
)
from wagtail.search import index

from .choices import receipt_disbursement_choices, transaction_category_choices, transaction_status_choices

# Create your models here.


class Ledger(
    WorkflowMixin,
    DraftStateMixin,
    LockableMixin,
    RevisionMixin,
    PreviewableMixin,
    index.Indexed,
    ClusterableModel,
):

    transaction_time = models.DateTimeField(verbose_name="交易时间")
    transaction_category = models.CharField(verbose_name="交易分类", max_length=255, choices=transaction_category_choices)
    counterparty = models.CharField(verbose_name="交易对方", max_length=255, blank=True, null=True)
    counterparty_account = models.CharField(verbose_name="对方账号", max_length=255, blank=True, null=True)
    product_description = models.CharField(verbose_name="商品说明", max_length=255, blank=True, null=True)
    receipt_disbursement = models.CharField(verbose_name="收/支", max_length=255, choices=receipt_disbursement_choices)
    amount = models.PositiveBigIntegerField(verbose_name="金额", )
    receipt_payment_method = models.CharField(verbose_name="收/付款方式", max_length=255, blank=True, null=True)
    transaction_status = models.CharField(verbose_name="交易状态", max_length=255, choices=transaction_status_choices)
    transaction_order_number = models.CharField(verbose_name="交易订单号", max_length=255, blank=True, null=True)
    merchant_order_number = models.CharField(verbose_name="商家订单号", max_length=255, blank=True, null=True)
    remarks = models.CharField(verbose_name="备注", max_length=255, blank=True, null=True)

    panels = [
        MultiFieldPanel(
            [
                FieldRowPanel(
                    [
                        FieldPanel("amount"),
                        FieldPanel("receipt_disbursement"),
                    ]
                )
            ],
            "Amount",
        ),
        FieldPanel("transaction_time"),
        FieldPanel("transaction_category"),
        FieldPanel("counterparty"),
        FieldPanel("counterparty_account"),
        FieldPanel("product_description"),
        FieldPanel("receipt_payment_method"),
        FieldPanel("transaction_status"),
        FieldPanel("transaction_order_number"),
        FieldPanel("merchant_order_number"),
        FieldPanel("remarks"),
        PublishingPanel(),
    ]

    search_fields = [
        index.SearchField("transaction_time"),
        index.FilterField("transaction_category"),
    ]

