from correx.models import Change
from correx.tests import ChangeTestCase

class CorrexModelTests(ChangeTestCase):

    def testSave(self):
        """ 
        Save a set of sample changes.
        """
        for c in self.createSomeChanges():
            self.failIfEqual(c.pub_date, None)