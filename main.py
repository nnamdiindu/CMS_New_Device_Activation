import os
import time
import logging
from dotenv import load_dotenv
from selenium import webdriver
from selenium.common import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


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
            logger.info("Clicking on Reject cookies button")
            cookies_button = self.driver.find_element(By.XPATH, value='/html/body/div/div/div[3]/div/div[2]/button[1]')
            cookies_button.click()

            logger.info("Inserting email adddress in input field")
            username_element = self.driver.find_element(By.XPATH, value='/html/body/div/div/div[1]/div[2]/div[2]/div/div[2]/div[1]/input')
            username_element.clear()
            username_element.send_keys(os.environ.get("USER"))

            logger.info("Inserting password in password field")
            password_element = self.driver.find_element(By.XPATH, value='/html/body/div/div/div[1]/div[2]/div[2]/div/div[2]/div[2]/input')
            password_element.clear()
            password_element.send_keys(os.environ.get("PASSWORD"))

            logger.info("Clicking on login button")
            login_button = self.driver.find_element(By.XPATH, value='/html/body/div/div/div[1]/div[2]/div[2]/div/div[2]/div[3]/button')
            login_button.click()
            logger.info("Logging in..")
            return True

        except Exception as e:
            print(f"Failed to login\nError: {e}")
            return False

    def search_olt(self, olt_name):
        time.sleep(10)
        logger.info("Logged in successfully")
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

        time.sleep(5)
        olt_status = self.driver.find_element(By.XPATH, value='/html/body/div[1]/div/div[2]/main/div/div[1]/form/div[5]/div/div/div/input')
        olt_status.click()
        time.sleep(5)
        olt_status.send_keys(Keys.ARROW_DOWN)
        olt_status.send_keys(Keys.ENTER)


    def click_detail_button(self):
        time.sleep(5)
        number_of_olts_online = self.driver.find_element(By.XPATH, value='/html/body/div[1]/div/div[2]/main/div/div[2]/div[1]/div[1]/div[3]/div/div[1]/span[2]').text
        logger.info(f"OLT Online: {number_of_olts_online}")

        # Wait until table is visible
        table = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "div.el-table__body-wrapper table.el-table__body"))
        )

        # Get all rows inside tbody
        rows = table.find_elements(By.CSS_SELECTOR, "tbody tr.el-table__row")

        # TODO: Loop through each OLT to perform tasks
        # Loop through each row
        for i, row in enumerate(rows, start=1):

            # find the Details button inside this row
            details_button = row.find_element(By.CSS_SELECTOR, "button.detail-btn")

            logger.info(f"Clicking Details button in row {i}")
            details_button.click()

            # TODO: Handle modal / popup / new page here if it appears
            self.device_configuration()


    def device_configuration(self):
        time.sleep(5)
        onu_manage_button = self.driver.find_element(By.XPATH, value='/html/body/div/div/div[2]/main/div/div[2]/span[1]/button')
        onu_manage_button.click()

        time.sleep(5)
        serial_number_input_field = self.driver.find_element(By.XPATH, value='//*[@id="pane-onu"]/div/div[1]/form/div[4]/div/div/input')
        serial_number_input_field.clear()
        serial_number_input_field.send_keys("CDTC1D3E5885")

        time.sleep(5)
        search_button = self.driver.find_element(By.CSS_SELECTOR, value='#pane-onu > div > div.header-search > div > button.el-button.el-button--primary.el-button--medium')
        search_button.click()

        try:
            visible_rows = self.get_table_rows_of_devices()

            if len(visible_rows) > 0:
                print(f"✅ Table exists with {len(visible_rows)} row(s).")
            else:
                print("⚠️ Table exists but has no rows.")
                self.driver.back()
                time.sleep(5)
                self.driver.back()

        except NoSuchElementException:
            print("❌ No table found inside the div.")
            self.driver.back()

    def get_table_rows_of_devices(self):
        # Try both possible scrolling states
        selectors = [
            ".el-table__body-wrapper.is-scrolling-none tbody tr",
            ".el-table__body-wrapper.is-scrolling-left tbody tr",
            ".el-table__body-wrapper tbody tr"  # fallback
        ]

        for selector in selectors:
            try:
                rows = self.driver.find_elements(By.CSS_SELECTOR, selector)
                if rows:
                    visible_rows = [row for row in rows if row.is_displayed()]
                    print(f"Found {len(visible_rows)} visible rows with selector: {selector}")
                    return visible_rows
            except Exception as e:
                print(f"Selector '{selector}' failed: {e}")
                continue

        return []


    def run_activation(self):
        self.setup_driver()
        if self.login_to_device():
            self.search_olt("sunshine")
            self.click_detail_button()


def main():
    activation = NewActivation()
    activation.run_activation()


if __name__ == "__main__":
    main()













