from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.test import TestCase
from selenium import webdriver
from selenium.webdriver.common.by import By  # Importing By
from django.contrib.auth.models import User
from selenium.webdriver.firefox.options import Options
from selenium.common.exceptions import NoSuchElementException
from django.urls import reverse

class MySeleniumTests(TestCase):
    #fixtures = ["user-data.json"]

    @classmethod
    def setUpClass(cls):
        options=Options()
        super().setUpClass()
        cls.selenium = webdriver.Remote(
            command_executor='http://localhost:4444/wd/hub',
            options=options)
        #cls.test_user = User.objects.create_user('testuser', 'test@example.com', 'testpassword')
        cls.selenium.implicitly_wait(10)

    @classmethod
    def tearDownClass(cls):
        cls.selenium.quit()
        super().tearDownClass()

    def test_login(self):
        self.selenium.get(f"http://192.168.0.27/accounts/login/")

        # Locate the username and password fields and input the credentials
        username_input = self.selenium.find_element(By.NAME, "username")
        username_input.send_keys("usr1")  # Use the username of the programmatically created user

        password_input = self.selenium.find_element(By.NAME, "password")
        password_input.send_keys("sudosusudo")  # Use the password of the programmatically created user

        # Find and click the login button
        self.selenium.find_element(By.XPATH, '//input[@value="login"]').click()

        # Add assertions here to verify successful login, such as checking the URL or page content
        # Example:
        expected_url = "http://192.168.0.27/"
        self.assertEqual(self.selenium.current_url, expected_url)

    def test_no_access(self):
        self.selenium.get(f"http://192.168.0.27/products")

        try:
            # Attempt to find the button. find_elements returns a list.
            buttons = self.selenium.find_elements(By.XPATH, "//a[contains(@class, 'btn-primary') and contains(text(), 'Add New Product')]")

            # If the list is not empty, the button exists, and we should fail the test.
            if buttons:
                self.fail("Button 'Add New Product' should not be present.")
        except NoSuchElementException:
            # If no element is found, the test passes.
            pass
        
    def test_ad_login(self):
        self.selenium.get(f"http://192.168.0.27/")
        
        logout_url = "http://192.168.0.27/accounts/logout/?next=/"
        self.selenium.get(logout_url)
        
        self.selenium.get(f"http://192.168.0.27/accounts/login/")
        # Locate the username and password fields and input the credentials
        username_input = self.selenium.find_element(By.NAME, "username")
        username_input.send_keys("adi")  # Use the username of the programmatically created user

        password_input = self.selenium.find_element(By.NAME, "password")
        password_input.send_keys("nonotme")  # Use the password of the programmatically created user

        # Find and click the login button
        self.selenium.find_element(By.XPATH, '//input[@value="login"]').click()

        # Add assertions here to verify successful login, such as checking the URL or page content
        # Example:
        expected_url = "http://192.168.0.27/"
        self.assertEqual(self.selenium.current_url, expected_url)
        
        self.selenium.get(f"http://192.168.0.27/products")

        self.selenium.find_element(By.XPATH, "//a[contains(@class, 'btn-primary') and contains(text(), 'Add New Product')]").click()
        expected_url = "http://192.168.0.27/product/create_product/"
        self.assertEqual(self.selenium.current_url, expected_url)
        
        
class MyUnitTests(TestCase):

    def test_homepage_view(self):
        # Make a GET request to the homepage
        response = self.client.get(reverse('index'))  # Replace 'home' with your view name

        # Check that the response is 200 OK
        self.assertEqual(response.status_code, 200)

        # Check if the correct template was used
        self.assertTemplateUsed(response, 'aintdoinit/index.html')  # Replace with your actual template
        
    def test_products_view(self):
        # Make a GET request to the homepage
        response = self.client.get(reverse('products'))  # Replace 'home' with your view name

        # Check that the response is 200 OK
        self.assertEqual(response.status_code, 200)

        # Check if the correct template was used
        self.assertTemplateUsed(response, 'aintdoinit/product_list.html')  # Replace with your actual template
        
    def test_cart_view(self):
        # Make a GET request to the homepage
        response = self.client.get(reverse('cart_view'))  # Replace 'home' with your view name

        # Check that the response is 200 OK
        self.assertEqual(response.status_code, 200)

        # Check if the correct template was used
        self.assertTemplateUsed(response, 'aintdoinit/cart_view.html')  # Replace with your actual template

