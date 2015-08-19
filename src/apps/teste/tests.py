# -*- coding:utf-8 -*-

from time import sleep

from django.contrib.auth import get_user_model
from django.contrib.staticfiles.testing import StaticLiveServerTestCase

from splinter import Browser

class TestSpliter(StaticLiveServerTestCase):

    @classmethod
    def setUpClass(cls):
        super(TestSpliter, cls).setUpClass()
        cls.browser = Browser("firefox")
        # cls.browser = Browser("phantomjs")
        # cls.browser = Browser("chrome")

    @classmethod
    def tearDownClass(cls):
        cls.browser.quit()
        super(TestSpliter, cls).tearDownClass()

    def setUp(self):
        self.create_superuser()

    def create_superuser(self):
        User = get_user_model()
        User.objects.create_superuser(username="adrianomargarin",
                                      email="teste@exemplo.com",
                                      password="123456")

    def login(self):
        self.browser.visit("%s%s" % (self.live_server_url, "/admin/login"))
        self.browser.fill_form({"username": "adrianomargarin",
                                "password": "123456"})
        button = self.browser.find_by_value("Log in")
        button.click()

    def test_search_google(self):
        self.browser.visit("http://google.com")
        self.browser.fill("q", "splinter - python acceptance testing for web applications")
        button = self.browser.find_by_name("btnG")
        button.click()

        self.assertTrue(self.browser.is_text_present("splinter.readthedocs.org"))

    def test_login_admin_django(self):
        self.login()

        self.assertTrue(self.browser.find_link_by_href("/admin/logout/"))

    def test_create_group(self):
        self.login()
        add = self.browser.find_link_by_href("/admin/auth/group/add/")
        add.click()
        self.browser.fill_form({"name": "Grupo 1"})
        self.browser.find_by_name("_save").click()

        self.assertTrue(self.browser.find_link_by_href("/admin/auth/group/1/"))
