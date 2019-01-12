"""Test for blog app"""
from django.test import TestCase

from config.test_utils import get_concrete_field_names

from ..models import NewsLink, Startup, Tag
from .factories import StartupFactory, TagFactory


class TagModelTests(TestCase):
    """Tests for the Tag model"""

    def test_concrete_fields(self):
        """Do we find the expected fields on the Tag model?"""
        field_names = get_concrete_field_names(Tag)
        expected_field_names = ["id", "name", "slug"]
        self.assertEqual(field_names, expected_field_names)

    def test_list_order(self):
        """Are tags ordered by primary-key?

        This test is actually dependent on the database and whether the
        field is unique. In SQLite3, the order will be alphabetical if
        the name field is unique.

        Will pass regardless if/once Meta ordering is defined.

        """
        TagFactory(name="b")
        TagFactory(name="D")
        TagFactory(name="c")
        TagFactory(name="a")
        tag_name_list = list(
            Tag.objects.values_list("name", flat=True)
        )
        expected_name_list = ["b", "D", "c", "a"]
        self.assertEqual(tag_name_list, expected_name_list)


class StartupModelTests(TestCase):
    """Tests for the Startup model"""

    def test_concrete_fields(self):
        """Do we find the expected fields on the Startup model?"""
        field_names = get_concrete_field_names(Startup)
        expected_field_names = [
            "id",
            "name",
            "slug",
            "description",
            "founded_date",
            "contact",
            "website",
        ]
        self.assertEqual(field_names, expected_field_names)

    def test_list_order(self):
        """Are Startups ordered by primary-key?

        This test is actually dependent on the database and whether the
        field is unique. In SQLite3, the order will be alphabetical if
        the name field is unique.

        Will pass regardless if/once Meta ordering is defined.

        """
        StartupFactory(name="b")
        StartupFactory(name="D")
        StartupFactory(name="c")
        StartupFactory(name="a")
        startup_name_list = list(
            Startup.objects.values_list("name", flat=True)
        )
        expected_name_list = ["b", "D", "c", "a"]
        self.assertEqual(
            startup_name_list, expected_name_list
        )


class NewsLinkModelTests(TestCase):
    """Tests for the NewsLink model"""

    def test_concrete_fields(self):
        """Do we find the expected fields on the NewsLink model?"""
        field_names = get_concrete_field_names(NewsLink)
        expected_field_names = [
            "id",
            "title",
            "slug",
            "pub_date",
            "link",
        ]
        self.assertEqual(field_names, expected_field_names)

    def test_newslink_startup_fk(self):
        """Does NewsLink have a Foreign Key to Startup?

        https://docs.djangoproject.com/en/2.1/ref/models/fields/#field-attribute-reference

        Let's have fun with this one! This is not how you'd write this test
        normally, but it does demonstrate some interesting field properties.

        """
        startup_field = NewsLink._meta.get_field("startup")
        # check nature of field
        self.assertFalse(startup_field.auto_created)
        self.assertTrue(startup_field.is_relation)
        self.assertTrue(startup_field.many_to_one)
        self.assertIs(startup_field.related_model, Startup)
        # the checks below are technically redundant
        self.assertTrue(startup_field.concrete)
        self.assertFalse(startup_field.one_to_one)
        self.assertFalse(startup_field.one_to_many)
        self.assertFalse(startup_field.many_to_many)
