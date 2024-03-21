# from django.contrib.contenttypes.fields import GenericRelation
from django.contrib import messages
from django.db import models
from django.shortcuts import redirect, render
from django.utils.translation import gettext as _
from modelcluster.fields import ParentalKey
from modelcluster.models import ClusterableModel
from modelcluster.contrib.taggit import ClusterTaggableManager

from wagtail.admin.panels import (
    FieldPanel,
    FieldRowPanel,
    # InlinePanel,
    MultiFieldPanel,
    PublishingPanel,
)
# from wagtail.contrib.forms.models import AbstractEmailForm, AbstractFormField
# from wagtail.contrib.settings.models import (
#     BaseGenericSetting,
#     BaseSiteSetting,
#     register_setting,
# )
# from wagtail.fields import RichTextField, StreamField
from wagtail.models import (
    # Collection,
    DraftStateMixin,
    LockableMixin,
    Page,
    PreviewableMixin,
    RevisionMixin,
    # TranslatableMixin,
    WorkflowMixin,
)
from wagtail.search import index
from wagtail.contrib.routable_page.models import RoutablePageMixin, route

from taggit.models import Tag, TaggedItemBase


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


class LedgerPageTag(TaggedItemBase):

    content_object = ParentalKey(
        "LedgerPage", related_name="tagged_items", on_delete=models.CASCADE
    )


class LedgerIndexPage(RoutablePageMixin, Page):
    introduction = models.TextField(help_text="Text to describe the page", blank=True)
    content_panels = Page.content_panels + [
        FieldPanel("introduction"),
    ]
    subpage_types = ["LedgerPage"]

    def children(self):
        return self.get_children().specific().live()

    @route(r"^tags/$", name="tag_archive")
    @route(r"^tags/([\w-]+)/$", name="tag_archive")
    def tag_archive(self, request, tag=None):

        try:
            tag = Tag.objects.get(slug=tag)
        except Tag.DoesNotExist:
            if tag:
                msg = 'There are no ledger posts tagged with "{}"'.format(tag)
                messages.add_message(request, messages.INFO, msg)
            return redirect(self.url)

        posts = self.get_posts(tag=tag)
        print('-'*20)
        print(tag)
        print('-'*20)
        context = {"self": self, "tag": tag, "posts": posts}
        return render(request, "ledger/ledger_index_page.html", context)
    
    def get_context(self, request):
        context = super().get_context(request)
        context["posts"] = (
            LedgerPage.objects.descendant_of(self).live().order_by("-date_published")
        )
        return context

    def serve_preview(self, request, mode_name):
        # Needed for previews to work
        return self.serve(request)

    # Returns the child LedgerPage objects for this LedgerPageIndex.
    # If a tag is used then it will filter the posts by tag.
    def get_posts(self, tag=None):
        posts = LedgerPage.objects.live().descendant_of(self)
        if tag:
            posts = posts.filter(tags__name=tag)
        return posts

    # Returns the list of Tags for all child posts of this LedgerPage.
    def get_child_tags(self):
        tags = []
        for post in self.get_posts():
            # Not tags.append() because we don't want a list of lists
            tags += post.get_tags
        tags = sorted(set(tags))
        # print(tags)
        return tags


class LedgerPage(Page):
    introduction = models.TextField(help_text="Text to describe the page", blank=True)
    transaction_time_start = models.DateTimeField()
    transaction_time_end = models.DateTimeField()
    tags = ClusterTaggableManager(through=LedgerPageTag, blank=True)
    date_published = models.DateField("Date article published", blank=True, null=True)

    content_panels = Page.content_panels + [
        FieldPanel("introduction"),
        FieldPanel("transaction_time_start"),
        FieldPanel("transaction_time_end"),
        FieldPanel("date_published"),
        FieldPanel("tags"),
    ]

    @property
    def get_tags(self):
        """
        Similar to the authors function above we're returning all the tags that
        are related to the blog post into a list we can access on the template.
        We're additionally adding a URL to access LedgerPage objects with that tag
        """
        tags = self.tags.all()
        base_url = self.get_parent().url
        for tag in tags:
            tag.url = f"{base_url}tags/{tag.slug}/"
        return tags
    
    # Specifies parent
    parent_page_types = ["LedgerIndexPage"]

    # Specifies what content types can exist as children of LedgerPage.
    # Empty list means that no child content types are allowed.
    subpage_types = []