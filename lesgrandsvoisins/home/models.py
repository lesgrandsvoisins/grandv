from django.db import models
from wagtail.models import Page, Orderable
from wagtail.fields import RichTextField, StreamField
from wagtail.admin.panels import FieldPanel, InlinePanel, MultiFieldPanel
from lesgrandsvoisins.admin.models import Application
from wagtail.snippets.models import register_snippet
from wagtail import blocks
import re


@register_snippet
class Footer(models.Model):
    contents = StreamField([
      ('content', blocks.RichTextBlock()),
    ], blank=True)

    class Meta:
        verbose_name_plural = 'Footers'

def GetCommonContext(context):
  context["footers"] = Footer.objects.all()
  return context

class HomePage(Page):
  content = RichTextField(blank=True)
  subtitle = RichTextField(blank=True, max_length=1024)
  intro = RichTextField(blank=True)


  content_panels = Page.content_panels + [ FieldPanel("content"), FieldPanel("intro"), FieldPanel("subtitle"),  ]

  def get_context(self, request, *args, **kwargs):
    context = super().get_context(request, *args, **kwargs)
    context["apps"] = Application.objects.all().order_by("title")
    context = GetCommonContext(context)
    return context

class ContentPage(Page):
  content = RichTextField(blank=True)
  subtitle = RichTextField(blank=True, max_length=1024)
  intro = RichTextField(blank=True)

  content_panels = Page.content_panels + [ FieldPanel("content"), FieldPanel("intro"), FieldPanel("subtitle"),  ]

  def get_context(self, request, *args, **kwargs):
    context = super().get_context(request, *args, **kwargs)
    context += GetCommonContext(context)
    return context
  