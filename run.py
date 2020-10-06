import os, time
from selenium import webdriver
from dotenv import load_dotenv
from selenium.webdriver import ChromeOptions
from app.common.user_input import user_input
from app.common.load_file import load_file
from app.common.user_login import user_login
from app import SetupCreateFile
from app import SetupCheckUser

load_dotenv()


rs = user_input()
if rs['status'] == True:
	files = load_file()
	if files:
		# path = os.getcwd()+'app\assets\geckodriver.exe'
		path = 'app\\assets\\chromedriver.exe'
		# driver = webdriver.Firefox(executable_path=path)
		options = ChromeOptions()
		options.add_experimental_option("debuggerAddress","127.0.0.1:51510")
		driver = webdriver.Chrome(path)
		driver.maximize_window()
		driver.get(os.getenv('LOGIN_LINK'))
		if rs['option'] == '1':
			start = input("(Are you ready? yes or no): ")
			if start == 'yes':
				setup = SetupCreateFile(files, driver, rs['panel'])
				setup.process_file()
		else:
			path_result = open('app\\assets\\result.json', "a+")
			start = input("(Are you ready? yes or no): ")
			if start == 'yes':
				setup = SetupCheckUser(driver, files, path_result, rs['date_bulk'])
				setup.check_file()
	else:
		print("Something wrong")
else:
	print("Something wrong")