from django.template import Template, Context
from correx.tests import ChangeTestCase
from correx.models import Change

class ChangeTemplateTagTests(ChangeTestCase):

    def render(self, t, **c):
        ctx = Context(c)
        out = Template(t).render(ctx)
        return ctx, out

    def testGetChangeList(self):
        """
        Tests the tag for pulling the most recently published changes.
        """
        self.createSomeChanges()
        t = "{% load correx_tags %}{% get_latest_changes 1 as latest_changes %}"
        match = Change.objects.get(pk=6)
        ctx, out = self.render(t, c=match)
        self.assertEqual(out, "")
        self.assertEqual(list(ctx["latest_changes"]), [match])

    def testGetChangeListByUser(self):
        """
        Tests the tag for pulling the most recent changes by a particular user.
        """
        self.createSomeChanges()
        t = "{% load correx_tags %}{% get_changes_for_user Otis 1 as latest_changes %}"
        match = Change.objects.get(pk=6)
        ctx, out = self.render(t, c=match)
        self.assertEqual(out, "")
        self.assertEqual(list(ctx["latest_changes"]), [match])

    def testGetChangeListBySite(self):
        """
        Tests the tag for pulling the most recent changes for a particular site.
        """
        self.createSomeChanges()
        t = "{% load correx_tags %}{% get_changes_for_site 1881 1 as latest_changes %}"
        match = Change.objects.get(pk=6)
        ctx, out = self.render(t, c=match)
        self.assertEqual(out, "")
        self.assertEqual(list(ctx["latest_changes"]), [match])

    def testGetChangeListByApp(self):
        """
        Tests the tag for pulling the most recent changes for a particular app.
        """
        self.createSomeChanges()
        t = "{% load correx_tags %}{% get_changes_for_app tests 1 as latest_changes %}"
        match = Change.objects.get(pk=6)
        ctx, out = self.render(t, c=match)
        self.assertEqual(out, "")
        self.assertEqual(list(ctx["latest_changes"]), [match])

"""
    def testGetChangeListByApp(self):
        self.createSomeChanges()
        t = "{% load correx_tags %}{% get_latest_changes tests 1 %}"
        match = Change.objects.filter(content_app='tests')[0]
        ctx, out = self.render(t, c=match)
        self.assertEqual(out, "")
        self.assertEqual(list(ctx["latest_changes"]), [match])
"""