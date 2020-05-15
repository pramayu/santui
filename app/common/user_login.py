import os
def user_login(driver, username, password):
	try:
		driver.get(os.getenv('LOGIN_LINK'))
		driver.find_element_by_name("email").send_keys(username)
		driver.find_element_by_name("password").send_keys(password)
		driver.find_element_by_class_name("btn-primary").click()
		return True
	except Exception as e:
		return False