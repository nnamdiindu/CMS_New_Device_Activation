import os
import time
from dotenv import load_dotenv
from selenium import webdriver
from selenium.webdriver.common.by import By


class NewActivation:
    def __init__(self):
        load_dotenv()
        self.driver = None

    def setup_driver(self):
        """Initialize Chrome driver with proper options"""
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_experimental_option("detach", True)  # Keeps browser open

        self.driver = webdriver.Chrome(options=chrome_options)
        self.driver.implicitly_wait(10)

    def login_to_device(self):
        try:
            self.driver.get("http://102.134.21.57:8083/#/device/olt")

            # Wait for page to load
            time.sleep(5)
            cookies_button = self.driver.find_element(By.XPATH, value='/html/body/div/div/div[3]/div/div[2]/button[1]')
            cookies_button.click()

            username_element = self.driver.find_element(By.XPATH, value='/html/body/div/div/div[1]/div[2]/div[2]/div/div[2]/div[1]/input')
            username_element.clear()
            username_element.send_keys(os.environ.get("USER"))

            password_element = self.driver.find_element(By.XPATH, value='/html/body/div/div/div[1]/div[2]/div[2]/div/div[2]/div[2]/input')
            password_element.clear()
            password_element.send_keys(os.environ.get("PASSWORD"))

            login_button = self.driver.find_element(By.XPATH, value='/html/body/div/div/div[1]/div[2]/div[2]/div/div[2]/div[3]/button')
            login_button.click()
            return True

        except Exception as e:
            print(f"Failed to login\nError: {e}")
            return False

    def search_olt(self, olt_name):
        time.sleep(10)
        device_tab = self.driver.find_element(By.XPATH, value='/html/body/div[1]/div/div[1]/div[1]/div[2]/div[2]')
        device_tab.click()

        time.sleep(5)
        olt_mqtt_dropdown = self.driver.find_element(By.XPATH, value='/html/body/div[1]/div/div[2]/div/div/div/div/div/ul/div[2]/li/div')
        olt_mqtt_dropdown.click()

        time.sleep(5)
        olt_list = self.driver.find_element(By.XPATH, value='/html/body/div[1]/div/div[2]/div/div/div/div/div/ul/div[2]/li/ul/div[1]/li')
        olt_list.click()

        time.sleep(5)
        list_display_format = self.driver.find_element(By.XPATH, value='/html/body/div[1]/div/div[2]/main/div/div[2]/div[1]/div[2]/div/div/label[2]/span/i')
        list_display_format.click()

        olt_description = self.driver.find_element(By.XPATH, value='/html/body/div[1]/div/div[2]/main/div/div[1]/form/div[1]/div/div/div[1]/input')
        olt_description.clear()
        olt_description.send_keys(olt_name)

        time.sleep(10)
        search_element = self.driver.find_element(By.XPATH, value='/html/body/div[1]/div/div[2]/main/div/div[1]/div/div/button[2]')
        search_element.click()

    def click_detail_button(self):
        rows = self.driver.find_elements(By.XPATH, '/html/body/div[1]/div/div[2]/main/div/div[2]/div[2]/div[1]/div[3]/table/tbody')
        print("Found rows:", len(rows))

        # Loop through each row
        for i in range(len(rows)):
            # Re-fetch rows each time (important because DOM may refresh after clicking)
            rows = self.driver.find_elements(By.XPATH,
                                             '/html/body/div[1]/div/div[2]/main/div/div[2]/div[2]/div[1]/div[3]/table/tbody')

            # Get the current row
            row = rows[i]

            # Find and click the Details button
            details_btn = row.find_element(By.CSS_SELECTOR, "button.detail-btn")
            details_btn.click()
            print(f"Clicked Details button in row {i + 1}")

            # Wait for modal/pop-up/details page (adjust selector)
            time.sleep(2)

            # Example: close modal if it appears (adjust selector to match your UI)
            try:
                close_btn = self.driver.find_element(By.CSS_SELECTOR, ".el-dialog__headerbtn")
                close_btn.click()
                time.sleep(1)
            except:
                pass


    def run_activation(self):
        self.setup_driver()
        if self.login_to_device():
            self.search_olt("unityhomes")
            self.click_detail_button()


def main():
    activation = NewActivation()
    activation.run_activation()


if __name__ == "__main__":
    main()
# rows = driver.find_elements(By.CSS_SELECTOR, "tbody tr.el-table__row")
# for row in rows:
#     details_element = driver.find_element(By.CSS_SELECTOR, value='body > div:nth-child(2) > div > div.layout-main > main > div > div.i-table-wrap > div.table-content > div.el-table.el-table--fit.el-table--enable-row-hover.el-table--enable-row-transition.el-table--medium > div.el-table__body-wrapper.is-scrolling-none > table > tbody > tr:nth-child(1) > td.el-table_1_column_10.el-table__cell > div > button')
#     details_element.click()












