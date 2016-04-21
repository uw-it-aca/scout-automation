from django.test import LiveServerTestCase, Client

class bar(LiveServerTestCase):

    def test_something(self):
        print "It works"
