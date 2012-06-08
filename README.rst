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

License
-------

`django-infinite-pagination` is released under the BSD license.

Other Resources
---------------

- `GitHub repository <https://github.com/nigma/django-infinite-pagination>`_
- `PyPi Package site <http://pypi.python.org/pypi/django-infinite-pagination>`_
