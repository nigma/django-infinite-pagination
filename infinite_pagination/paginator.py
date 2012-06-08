#-*- coding: utf-8 -*-

from django.core.paginator import Paginator, Page, PageNotAnInteger, EmptyPage


class InfinitePaginator(Paginator):
    """
    Paginator for efficiently paginating large object collections on systems
    where using standard Django pagination is impractical because of significant
    ``count(*)`` query overhead.

    It uses a single query to retrieve objects for the current page and
    check the availability of successive page.
    """

    def __init__(self, object_list, per_page, orphans=None,
                 allow_empty_first_page=True):
        super(InfinitePaginator, self).__init__(object_list, per_page,
            orphans=0, allow_empty_first_page=allow_empty_first_page)
        del self._num_pages, self._count

    def validate_number(self, number):
        """Validates the given 1-based page number."""
        try:
            number = int(number)
        except (TypeError, ValueError):
            raise PageNotAnInteger("That page number is not an integer")
        if number < 1:
            raise EmptyPage("That page number is less than 1")
        return number

    def page(self, number):
        """
        Returns a Page object for the given 1-based page number.

        Retrieves objects for the given page number plus 1 additional to check
        if there are more objects after this page.
        """
        number = self.validate_number(number)
        offset = (number - 1) * self.per_page

        # this page objects + 1 extra
        window_items = list(self.object_list[offset:offset + self.per_page +1])
        page_items = window_items[:self.per_page]

        if not page_items:
            if number == 1 and self.allow_empty_first_page:
                pass
            else:
                raise EmptyPage("That page contains no results")

        has_next = len(window_items) > len(page_items)
        return InfinitePage(page_items, number, self, has_next)

    def _get_count(self):
        raise NotImplementedError
    count = property(_get_count)

    def _get_num_pages(self):
        raise NotImplementedError
    num_pages = property(_get_num_pages)

    def _get_page_range(self):
        raise NotImplementedError
    page_range = property(_get_page_range)


class InfinitePage(Page):

    def __init__(self, object_list, number, paginator, has_next):
        super(InfinitePage, self).__init__(object_list, number, paginator)
        self._has_next = has_next

    def __repr__(self):
        return "<Page %s>" % self.number

    def has_next(self):
        return self._has_next

    def end_index(self):
        """
        Returns the 1-based index of the last object on this page,
        relative to total objects found (hits).
        """
        return (
            (self.number - 1) * self.paginator.per_page + len(self.object_list)
        )

__all__ = ["InfinitePaginator", "InfinitePage"]
