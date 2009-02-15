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
        Tests the most recent live change from the entire test set and verifies that it matches.
        """
        self.createSomeChanges()
        t = "{% load correx_tags %}{% get_latest_changes all_apps 1 %}"
        match = Change.objects.get(pk=6)
        ctx, out = self.render(t, c=match)
        self.assertEqual(out, "")
        self.assertEqual(list(ctx["latest_changes"]), [match])

    def testGetChangeListByApp(self):
        self.createSomeChanges()
        t = "{% load correx_tags %}{% get_latest_changes tests 1 %}"
        match = Change.objects.filter(content_app='tests')[0]
        ctx, out = self.render(t, c=match)
        self.assertEqual(out, "")
        self.assertEqual(list(ctx["latest_changes"]), [match])
