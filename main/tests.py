from django.test import TestCase, Client

class mainTest(TestCase):
    def test_main_url_is_exist(self):
        response = Client().get('/main/')
        self.assertEqual(response.status_code, 200)

    def test_main_using_main_template(self):
        response = Client().get('/main/')
        self.assertTemplateUsed(response, 'main.html')

    def test_header_content(self):
        response = Client().get('/main/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Welcome to Asdos Tracker!")
        self.assertContains(response, "A place where you can track your asdos log")

    def test_player_information(self):
        response = Client().get('/main/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Asdos Information")
        self.assertContains(response, "Name:")
        self.assertContains(response, "Class:")

    # def test_footer_content(self):
    #     response = Client().get('/main/')
    #     self.assertEqual(response.status_code, 200)
    #     self.assertContains(response, "2023 Alif Bintang (2206029153). Pemrograman Berbasis Platform Gasal 23/24.")