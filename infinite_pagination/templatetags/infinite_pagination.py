#-*- coding: utf-8 -*-

from __future__ import absolute_import
import copy

from django.template import Library

from ..paginator import InfinitePaginator

register = Library()

PAGE = "page"


@register.inclusion_tag("pagination/infinite_pagination.html", takes_context=True)
def paginate(context):
    try:
        paginator = context["paginator"]
        page_obj = context["page_obj"]
    except KeyError:
        return {}
    assert isinstance(paginator, InfinitePaginator)

    tag_context = copy.copy(context) # reuse original context
    tag_context["is_paginated"] = page_obj.has_other_pages()

    if "request" in context:
        getvars = context["request"].GET.copy()
        if PAGE in getvars:
            del getvars[PAGE]
        if len(getvars.keys()) > 0:
            tag_context["getvars"] = "&%s" % getvars.urlencode()
        else:
            tag_context["getvars"] = ""
    return tag_context
