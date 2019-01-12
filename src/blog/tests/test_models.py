"""Test for blog app"""
from datetime import date

from django.test import TestCase

from config.test_utils import get_concrete_field_names

from ..models import Post
from .factories import PostFactory


class PostModelTests(TestCase):
    """Tests for the Post model"""

    def test_post_concrete_fields(self):
        """Do we find the expected fields on the Post model?"""
        field_names = get_concrete_field_names(Post)
        expected_field_names = [
            "id",
            "title",
            "slug",
            "text",
            "pub_date",
        ]
        self.assertEqual(field_names, expected_field_names)

    def test_post_list_order(self):
        """Are posts ordered by primary-key?"""
        PostFactory(title="b", pub_date=date(2017, 1, 1))
        PostFactory(title="a", pub_date=date(2016, 1, 1))
        PostFactory(title="a", pub_date=date(2017, 1, 1))
        PostFactory(title="d", pub_date=date(2018, 1, 1))
        post_name_list = [
            (name, p_date.year)
            for name, p_date in Post.objects.values_list(
                "title", "pub_date"
            )
        ]
        expected_name_list = [
            ("b", 2017),
            ("a", 2016),
            ("a", 2017),
            ("d", 2018),
        ]
        self.assertEqual(post_name_list, expected_name_list)
