#-*- coding: utf-8 -*-

from __future__ import absolute_import
import copy

from django.core.paginator import InvalidPage
from django.http import Http404
from django.template import Library
from django.utils.translation import ugettext as _

from ..paginator import InfinitePaginator

register = Library()

PAGE_VAR = "page"

@register.assignment_tag(takes_context=True)
def autopaginate(context, object_list, per_page=15, page=None):
    """
    Takes a queryset and returns page slice.

    It also sets context ``paginator`` and ``page_obj`` variables for purpose
    of pagination links rendering.
    """

    page_number = page or context.get(PAGE_VAR)
    if "request" in context and not page_number:
        request = context["request"]
        page_number = request.GET.get(PAGE_VAR)
    page_number = page_number or 1

    try:
        page_number = int(page_number)
    except ValueError:
        raise Http404(_(u"Page can not be converted to an int."))

    paginator = InfinitePaginator(object_list=object_list, per_page=per_page)
    try:
        page_obj = paginator.page(page_number)
    except InvalidPage:
        raise Http404(_(u"Invalid page (%(page_number)s)") % {"page_number": page_number})

    context.update({
        "paginator": paginator,
        "page_obj": page_obj
    })
    return page_obj.object_list


@register.inclusion_tag("pagination/infinite_pagination.html", takes_context=True)
def paginate(context):
    try:
        page_obj = context["page_obj"]
    except KeyError:
        return {}

    tag_context = copy.copy(context) # reuse original context
    tag_context["is_paginated"] = page_obj.has_other_pages()

    if "request" in context:
        getvars = context["request"].GET.copy()
        if PAGE_VAR in getvars:
            del getvars[PAGE_VAR]
        if len(getvars.keys()) > 0:
            tag_context["getvars"] = "&%s" % getvars.urlencode()
        else:
            tag_context["getvars"] = ""
    return tag_context
