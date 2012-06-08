Infinite Pagination for Django
==============================

This is a very simple helper for Django 1.4 that does one thing: efficiently
paginates large object collections on systems where using standard Django
Paginator is impractical because of significant ``count(*)`` query
overhead (i.e. PostgreSQL).

Under the hood it uses a single query to retrieve objects for the current page
and check for availability of a successive page.

The ``InfinitePaginator`` is a replacement for Django
``django.core.paginator.Paginator``.

Quick Start
-----------

Include ``django-infinite-pagination`` in your requirements file
(or ``pip install django-infinite-pagination``) and add ``infinite_pagination``
to ``INSTALLED APPS``.

Then set the ``paginator_class`` attribute of your ``ListView``-based view to
``InfinitePaginator`` and specify ``paginate_by`` attribute::

    class ArticleListView(ListView):
        model = Article
        paginate_by = 10
        paginator_class = InfinitePaginator

To display pagination links in a template load the ``infinite_pagination``
template tags and put ``{% paginate %}`` in the place you would like the
pagination links to show up::

    {% load infinite_pagination %}

    {% for object in object_list %}
        {{ object }}
    {% endfor %}

    {% paginate %}


A generic ``pagination/infinite_pagination.html`` template that works well with
Twitter Bootstrap stylesheet is provided by this application. Adjust it to your
requirements.

Paginating in Templates
-----------------------

Sometimes application views cannot be modified and the pagination can only be
done at the template level. The ``autopaginate`` template tag is provided
as a last resort of applying pagination to object lists inside templates::

    {% load infinite_pagination %}

    {% autopaginate object_list per_page=10 as paginated_list %}

    {% for object in paginated_list %}
        {{ object }}
    {% endfor %}

    {% paginate %}


The ``autopaginate`` tag takes a queryset and a number of items per page
as input and returns a page slice for displaying in a template. Current page
number is retrieved from template context or ``page`` request GET params.
It can also be specified as an optional tag param::

    {% autopaginate object_list per_page=10 page=2 as paginated_list %}

The tag also sets ``paginator`` and ``page_obj`` template context variables for
the ``paginate`` tag that uses them to render navigation links.

License
-------

`django-infinite-pagination` is released under the BSD license.

Other Resources
---------------

- `GitHub repository <https://github.com/nigma/django-infinite-pagination>`_
- `PyPi Package site <http://pypi.python.org/pypi/django-infinite-pagination>`_
