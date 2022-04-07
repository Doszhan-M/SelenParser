from browser import Browser
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
import time

class Parser(Browser):
    def __init__(self) -> None:
        super().__init__()

    def parse(self):
        # https://kolesa.kz/a/show/130822233
        # https://kolesa.kz/a/show/131074816
        self.driver.get("https://kolesa.kz/a/show/130822233")
        self.driver.set_window_size(1920, 1057)
        self.wait.until(EC.element_to_be_clickable((By.ID, "buy-on-credit")))
        price=self.driver.find_element(By.CLASS_NAME,"offer__price")
        self.driver.find_element(By.XPATH,"/html/body/main/div/div/div/section/div[1]/div[2]/div[1]/div/div/div[1]/div/div/button").click()
        time.sleep(5)
        phones_list=self.driver.find_element(By.CLASS_NAME,"seller-phones__phones-list")
        phones_list=phones_list.find_elements(By.TAG_NAME,"li")
        phones=[]
        for i in phones_list:
            phones.append(i.text)
        self.driver.find_element(By.ID,"initPay").click()
        self.driver.find_element(By.ID,"initPay").send_keys("1")
        return {
            "phones": phones,
            "price": price.text
        }



print(Parser().parse())