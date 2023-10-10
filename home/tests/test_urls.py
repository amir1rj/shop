from django.test import TestCase
from django.urls import reverse, resolve

from home.views import Home


class TestUrls(TestCase):
    def test_home(self):
        url = reverse('home:main')
        self.assertEquals(resolve(url).func.view_class,Home)