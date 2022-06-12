from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import unittest
import json
import warnings
import time 
        
warnings.filterwarnings("ignore")

class TestStringMethods(unittest.TestCase):

	
	def setUp(self):

	
		self.driver = webdriver.Chrome('./chromedriver')
		self.driver.get("http://demowebshop.tricentis.com/login")

		loginbutton = self.driver.find_element_by_class_name("ico-login")
		loginbutton.click()
		

	def test_login(self):
		print("===============Test Login Functionality===============")
		driver = self.driver
		# Opening test_data file
		f = open('test_data.json')
		data = json.load(f)

		

		count = 1
		#Test case 1
		for i in data['login_data']:
			print("Running test cases ",count," of 3")
			self.doLogin(i, driver, True)
			count = count+1

		f.close()



	def test_addtocart(self):
		print("===============Test Add To Cart Functionality===============")
		driver = self.driver
		self.doLogin({"username":"vishwa.m@gmail.com", "password":"dummy123", "match":"match"}, driver, False)
		driver.find_elements_by_class_name("product-box-add-to-cart-button")[1].click()
		driver.find_element_by_class_name("ico-logout")
		time.sleep(2)

	def test_checkout(self):
		print("===============Test checkout Functionality===============")
		driver = self.driver
		self.doLogin({"username":"vishwa.m@gmail.com", "password":"dummy123", "match":"match"}, driver, False)
		shoppingcartbutton = driver.find_element_by_class_name("cart-label")
		shoppingcartbutton.click()

		#gotocartbutton = driver.find_element_by_class_name("cart-button")
		#gotocartbutton.click()
		
		time.sleep(5)
		driver.find_element_by_id("termsofservice").click()

		checkoutbutton = driver.find_element_by_id("checkout")
		checkoutbutton.click()

		time.sleep(10)

		el = driver.find_element_by_id('BillingNewAddress_CountryId')
		for option in el.find_elements_by_tag_name('option') :
			if option.text == "Australia":
				option.click() # select() in earlier versions of webdriver
				break

		time.sleep(5)

		driver.find_element_by_class_name("new-address-next-step-button").click()

		time.sleep(5)

		driver.find_element_by_id("PickUpInStore").click()
		driver.find_elements_by_class_name("new-address-next-step-button")[1].click()
		time.sleep(5)
		driver.find_element_by_id("paymentmethod_2").click()
		time.sleep(5)
		driver.find_element_by_class_name("payment-method-next-step-button").click()
		time.sleep(5)
		inputElement = driver.find_element_by_id("CardholderName")
		inputElement.send_keys('Test')
		inputElement = driver.find_element_by_id("CardNumber")
		inputElement.send_keys('4242424242424242')

		yr = driver.find_element_by_id('ExpireYear')
		for option in yr.find_elements_by_tag_name('option') :
			if option.text == "2024":
				option.click() # select() in earlier versions of webdriver
				break

		inputElement = driver.find_element_by_id("CardCode")
		inputElement.send_keys('423')
		driver.find_element_by_class_name("payment-info-next-step-button").click()

		time.sleep(5)

		driver.find_element_by_class_name("confirm-order-next-step-button").click()
		time.sleep(5)

		driver.find_element_by_class_name("order-completed-continue-button").click()
		time.sleep(5)

		driver.find_element_by_class_name("ico-logout")

	def doLogin(self, i, driver, logout):
		print("===============Test login Functionality===============")
		driver = self.driver
		self.driver.find_element_by_class_name("ico-login").click()
		email = driver.find_element_by_id("Email")
		email.send_keys(i['username'])
		passwd = driver.find_element_by_id("Password")
		passwd.send_keys(i['password'])
		time.sleep(1)
		submit = driver.find_element_by_class_name("login-button")
		submit.click()
		if driver.find_elements_by_css_selector(".ico-logout"):
			self.assertEqual("match", i['match'])
			if logout:
				driver.find_element_by_class_name("ico-logout").click()
				
		else: 
			time.sleep(5)
			error = driver.find_elements_by_css_selector(".validation-summary-errors ul li")[0].get_attribute('innerText')
			if i['error'] == "user wrong":
				self.assertEqual(error, i['match'])
			if i['error'] == "pass wrong":
				self.assertEqual(error, i['match'])

	
			




if __name__ == '__main__':
    unittest.main()





