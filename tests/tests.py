#-*- coding: utf-8 -*-

from django.core.paginator import EmptyPage
from django.test.testcases import TestCase

from infinite_pagination.paginator import InfinitePaginator

from .models import Article


class InfinitePaginatorTestCase(TestCase):

    def setUp(self):
        for x in range(25):
            Article.objects.create(title=str(x))
        self.paginator = InfinitePaginator(Article.objects.all(), 10)

    def tearDown(self):
        Article.objects.all().delete()

    def test_pagination(self):
        page1 = self.paginator.page(1)
        page2 = self.paginator.page(2)
        page3 = self.paginator.page(3)

        self.assertEqual(page1.object_list, list(Article.objects.all()[0:10]))
        self.assertEqual(page2.object_list, list(Article.objects.all()[10:20]))
        self.assertEqual(page3.object_list, list(Article.objects.all()[20:25]))

    def test_first_page(self):
        page = self.paginator.page(1)
        self.assertEqual(page.number, 1)
        self.assertTrue(page.has_next())
        self.assertFalse(page.has_previous())
        self.assertTrue(page.has_other_pages())
        self.assertEqual(page.next_page_number(), 2)
        self.assertEqual(page.end_index(), 10)

    def test_second_page(self):
        page = self.paginator.page(2)
        self.assertEqual(page.number, 2)
        self.assertTrue(page.has_next())
        self.assertTrue(page.has_previous())
        self.assertTrue(page.has_other_pages())
        self.assertEqual(page.previous_page_number(), 1)
        self.assertEqual(page.next_page_number(), 3)
        self.assertEqual(page.end_index(), 20)

    def test_last_page(self):
        page = self.paginator.page(3)
        self.assertEqual(page.number, 3)
        self.assertFalse(page.has_next())
        self.assertTrue(page.has_previous())
        self.assertTrue(page.has_other_pages())
        self.assertEqual(page.previous_page_number(), 2)
        self.assertEqual(page.end_index(), 25)

    def test_invalid_page(self):
        self.assertRaises(EmptyPage, lambda: self.paginator.page(4))

    def test_single_page(self):
        paginator = InfinitePaginator(Article.objects.all(), 100)
        page = paginator.page(1)
        self.assertEqual(page.number, 1)
        self.assertFalse(page.has_next())
        self.assertFalse(page.has_previous())
        self.assertFalse(page.has_other_pages())
        self.assertEqual(page.end_index(), 25)

    def test_empty_page(self):
        paginator = InfinitePaginator(Article.objects.none(), 100)
        page = paginator.page(1)
        self.assertEqual(page.object_list, [])
        self.assertEqual(page.number, 1)
        self.assertFalse(page.has_next())
        self.assertFalse(page.has_previous())
        self.assertFalse(page.has_other_pages())
        self.assertEqual(page.end_index(), 0)


class TemplateTagTestCase(TestCase):

    def setUp(self):
        for x in range(25):
            Article.objects.create(title=str(x))

    def tearDown(self):
        Article.objects.all().delete()

    def test_init_page(self):
        resp = self.client.get("/articles/?param=x")
        self.assertIn("""<a>&larr; Previous</a>""", resp.content)
        self.assertIn("""<a href="?page=2&amp;param=x">Next &rarr;</a>""", resp.content)
        self.assertIn("""<li>0</li>""", resp.content)
        self.assertNotIn("""<li>10</li>""", resp.content)
        self.assertNotIn("""<li>20</li>""", resp.content)

    def test_first_page(self):
        resp = self.client.get("/articles/?page=1&param=x")
        self.assertIn("""<a>&larr; Previous</a>""", resp.content)
        self.assertIn("""<a href="?page=2&amp;param=x">Next &rarr;</a>""", resp.content)
        self.assertIn("""<li>0</li>""", resp.content)
        self.assertNotIn("""<li>10</li>""", resp.content)
        self.assertNotIn("""<li>20</li>""", resp.content)

    def test_second_page(self):
        resp = self.client.get("/articles/?page=2&param=x")
        self.assertIn("""<a href="?page=1&amp;param=x">First</a>""", resp.content)
        self.assertIn("""<a href="?page=1&amp;param=x">&larr; Previous</a>""", resp.content)
        self.assertIn("""<a href="?page=3&amp;param=x">Next &rarr;</a>""", resp.content)
        self.assertIn("""<li>10</li>""", resp.content)
        self.assertNotIn("""<li>0</li>""", resp.content)
        self.assertNotIn("""<li>20</li>""", resp.content)

    def test_last_page(self):
        resp = self.client.get("/articles/?page=3&param=x")
        self.assertIn("""<a href="?page=1&amp;param=x">First</a>""", resp.content)
        self.assertIn("""<a href="?page=2&amp;param=x">&larr; Previous</a>""", resp.content)
        self.assertIn("""<a>Next &rarr;</a>""", resp.content)
        self.assertIn("""<li>20</li>""", resp.content)
        self.assertNotIn("""<li>10</li>""", resp.content)
