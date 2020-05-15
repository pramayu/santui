import os
import csv
import time
from tqdm import tqdm
from datetime import datetime
from selenium.webdriver.common.keys import Keys


class SetupCreateFile():
	def __init__(self, files, driver, panel=None):
		self.driver 	= driver
		self.files 		= files
		self.panel 		= panel

	def choose_service(self, lt_service):
		time.sleep(2)
		fr_service = self.driver.find_element_by_id("tdserviceinfo1").text
		fl_service = fr_service.split()[0]
		if len(lt_service) == 2:
			sd_service = self.driver.find_element_by_id("tdserviceinfo2").text
			fl_service = f"{fl_service},{sd_service.split()[0]}"
		return fl_service

	def select_panel(self, kap, rn_port):
		rn_panl = ""
		if kap == '8':
			panel = self.driver.find_elements_by_class_name("label")[3].text
			if rn_port == panel:
				rn_panl = rn_port
			else:
				rn_panl = panel
		else:
			panel = self.driver.find_elements_by_class_name("label")[3].text
			pnl_1 = "".join(panel.split("|")[0].split("-")[-1:])
			pnl_1 = pnl_1 if len(pnl_1) == 1 else pnl_1[-1:]
			# pnl_2 = "".join(panel.split("|")[1].split("-")[-1:])
			# pnl_2 = pnl_2 if len(pnl_2) == 1 else pnl_2[-1:]
			if pnl_1 == self.panel:
				panel = panel.split("|")[0]
				if rn_port == panel:
					rn_panl = rn_port
				else:
					rn_panl = panel
			else:
				panel = panel.split("|")[1]
				if rn_port == panel:
					rn_panl = rn_port
				else:
					rn_panl = panel

		
		return rn_panl

	def choose_odpportx(self):
		kap = self.driver.find_elements_by_css_selector("td.column_number a")[0].text
		self.driver.find_element_by_link_text(f"{kap}").click()

		time.sleep(1)
		if self.panel == '1':
			fl_panel_odd 	= self.driver.find_elements_by_css_selector("tr.odd td")[0].text
			fl_panel_even 	= self.driver.find_elements_by_css_selector("tr.even td")[0].text
			if "-".join(fl_panel_odd.split("-")[:-1])[-1:] == self.panel:
				rn_port = "-".join(fl_panel_odd.split("-")[:-1])
				lt_port = "".join(fl_panel_odd.split("-")[-1:])
			else:
				rn_port = "-".join(fl_panel_even.split("-")[:-1])
				lt_port = "".join(fl_panel_even.split("-")[-1:])
			rn_panl = self.select_panel(kap, rn_port)
			result = {
				'rn_port': rn_port,
				'rn_panl': rn_panl,
				'lt_port': lt_port
			}
			return result
		if self.panel == '2':
			fl_panel_odd 	= self.driver.find_elements_by_css_selector("tr.odd td")[0].text
			fl_panel_even 	= self.driver.find_elements_by_css_selector("tr.even td")[0].text
			if "-".join(fl_panel_even.split("-")[:-1])[-1:] == self.panel:
				rn_port = "-".join(fl_panel_even.split("-")[:-1])
				lt_port = "".join(fl_panel_even.split("-")[-1:])
			else:
				rn_port = "-".join(fl_panel_odd.split("-")[:-1])
				lt_port = "".join(fl_panel_odd.split("-")[-1:])
			rn_panl = self.select_panel(kap, rn_port)
			result = {
				'rn_port': rn_port,
				'rn_panl': rn_panl,
				'lt_port': lt_port
			}
			return result


	def collect_odpport_panel(self, odp_name):
		self.driver.get(os.getenv('ODP_LINK'))
		time.sleep(2)
		self.driver.find_elements_by_id("filter")[5].click()
		self.driver.find_elements_by_id("deviceLocation")[0].send_keys(odp_name)
		self.driver.find_elements_by_id("deviceLocation")[0].send_keys(Keys.ENTER)
		time.sleep(1)
		rn_port = self.choose_odpportx()
		return rn_port

	def create_file(self, fl_service, panel_port, port, service):
		sfx_name = datetime.now().strftime("%Y%m%d%H%M%S")
		filename = f"UPDATE_STP_IMMEDIATE_{sfx_name}.csv"
		pathfile = os.getcwd()+'\\app\\output\\'+filename
		lt_port = port if len(panel_port['lt_port']) == 1 else f"0{port}"
		with open(pathfile, 'w', newline='') as file:
			thewriter = csv.writer(file, delimiter='|')
			thewriter.writerow(['SERVICE_NAME','SERVICE_NUMBER','ODP_PANEL','PORT_NAME'])
			chk_service = f'0{service}' if service[0] == '3' else service
			thewriter.writerow([f'{fl_service}',f'{chk_service}',f'{panel_port["rn_panl"]}',f'{panel_port["rn_port"]}-{lt_port}'])
		time.sleep(6)
		pathfile = os.getcwd()+'\\app\\output\\'+filename
		self.driver.get(os.getenv('UPLOAD_LINK'))
		self.driver.find_elements_by_class_name("select2-selection")[0].click()
		time.sleep(2)
		self.driver.find_elements_by_css_selector("li.select2-results__option")[1].click()
		time.sleep(5)
		self.driver.find_elements_by_class_name("select2-selection")[1].click()
		time.sleep(2)
		self.driver.find_elements_by_css_selector("li.select2-results__option")[1].click()
		time.sleep(2)
		file_input = self.driver.find_element_by_name("file")
		file_input.send_keys(pathfile)
		time.sleep(2)
		self.driver.find_elements_by_class_name("btn-warning")[1].click()
		time.sleep(2)

	def collect_service(self, service, odp_name, port):
		time.sleep(3)
		self.driver.get(os.getenv('SERVICE_LINK'))
		self.driver.find_element_by_id('servid').clear()
		if service[0] == '3':
			self.driver.find_element_by_id('servid').send_keys(f"0{service}")
		else:
			self.driver.find_element_by_id('servid').send_keys(service)
		self.driver.find_element_by_id('servid').send_keys(Keys.ENTER)
		time.sleep(3)
		lt_service = self.driver.find_elements_by_name("selecteds")
		fl_service = self.choose_service(lt_service)
		time.sleep(1)
		panel_port = self.collect_odpport_panel(odp_name)
		if len(panel_port) != 0:
			self.create_file(fl_service, panel_port, port, service)

	

	def process_file(self):
		loop = tqdm(total = len(self.files))
		for file in self.files:
			try:
				self.collect_service(file['SERVICE'], file['ODP'], file['PORT'])
				loop.set_description(f"Latest Service {file['SERVICE']}".format(file))
				loop.update(1)
			except Exception as e:
				print(e)
				pass
				
class SetupCheckUser():
	def __init__(self, driver, files, result, date_bulk):
		self.driver = driver
		self.files = files
		self.result = result
		self.date_bulk = date_bulk

	def gass_check(self):
		self.driver.get(os.getenv('CHECK_LINK'))
		self.driver.find_elements_by_class_name("select2-selection")[0].click()
		time.sleep(2)
		self.driver.find_elements_by_css_selector("li.select2-results__option")[1].click()
		time.sleep(5)
		self.driver.find_elements_by_class_name("select2-selection")[1].click()
		time.sleep(2)
		self.driver.find_elements_by_css_selector("li.select2-results__option")[1].click()
		self.driver.find_elements_by_id("filter")[1].click()
		self.driver.find_element_by_name("datetime").send_keys(self.date_bulk)
		self.driver.find_elements_by_class_name("btn-warning")[0].click()
		time.sleep(3)

	def run_check(self, _id):
		time.sleep(2)
		self.driver.find_element_by_xpath("//input[@type='search']").send_keys("art.t")
		time.sleep(2)
		self.driver.find_element_by_xpath("//select[@name='datatable_tabletools_length']/option[text()='All']").click()
		time.sleep(2)
		self.driver.find_element_by_link_text(f"{_id}").click()
		time.sleep(2)
		x = self.driver.find_elements_by_css_selector("td a")[10].text
		r = self.driver.find_elements_by_tag_name("td")[94].text
		self.result.write(f"{x.split('|')[1]} {r}\n")
		time.sleep(1.5)
		self.driver.find_elements_by_css_selector("div.jarviswidget-ctrls a.jarviswidget-toggle-btn")[1].click()

	def check_file(self):
		self.gass_check()
		loop = tqdm(total = len(self.files))
		for file in self.files:
			try:
				self.run_check(file['ID'])
				loop.set_description(f"Latest Service {file['ID']}".format(file))
				loop.update(1)
			except Exception as e:
				print(e)
				pass
