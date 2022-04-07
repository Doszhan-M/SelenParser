import os
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


chrome_options = Options()
# chrome_options.add_argument("--headless") # headless mode. Comment this line for interactive debugging
# suggested options. Good for containers. Not so for macs
# chrome_options.add_argument("--headless")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")
chrome_options.add_experimental_option('prefs', {
    # Change default directory for downloads
    "download.default_directory": os.path.abspath(os.getcwd()),
    "download.prompt_for_download": False,  # To auto download the file
    "download.directory_upgrade": True,
    "plugins.always_open_pdf_externally": True  # It will not show PDF directly in chrome
})
chrome_options.add_argument(
    "user-agent=Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.69 Safari/537.36")
driver = webdriver.Chrome(options=chrome_options)
wait = WebDriverWait(driver, 5)  # create a wait object. Will raise exception after certain amount


def start():
    driver.get(f"file:///home/lenovo/Документы/kol.kz/page.html")
    # wait.until(EC.presence_of_element_located(
    #     (By.XPATH, "/html/body/div[4]/div[1]/div[2]/div[2]/div[1]/div/div/table")))

    table = driver.find_element(
        By.XPATH, "/html/body/div[4]/div[1]/div[2]/div[2]/div[1]/div/div/table")
    rows = table.find_elements(By.TAG_NAME, "tr")
    clear_rows = rows.copy()

    remove = True
    for row in rows:
        className = row.get_attribute("class")
        if remove:
            if className == 'head item-info-table':
                remove = False
            else:
                clear_rows.remove(row)

    temp_dict = {}
    temp_key = ''
    for index, row in enumerate(clear_rows):
        className = row.get_attribute("class")
        if className == 'head item-info-table':
            temp_dict[row.text] = index
            temp_key = row.text
        else:
            temp_dict[temp_key] = temp_dict[temp_key] + 1

    result = {}
    for key in temp_dict.keys():
        result[key] = {}

    temp_list = []
    for key in result.keys():
        while temp_dict[key] != 0:
            columns = clear_rows[temp_dict[key]].find_elements(By.TAG_NAME, "td")
            temp_dict[key] = temp_dict[key] - 1
            if len(columns) == 2 and columns not in temp_list:
                result[key].update({columns[0].text: columns[-1].text})
                temp_list.append(columns)

    for row in rows:
        className = row.get_attribute("class")
        if className == 'head item-info-table':
            break
        columns = row.find_elements(By.TAG_NAME, "td")
        if len(columns) == 2:
            result.update({columns[0].text: columns[-1].text})

    print(result)


start()
driver.quit()


a = {
    'Основания для включения НП в Список налогоплательщиков, признанных банкротами':
    [{'Дата решения суда': ''},
     {
        'Номер решения суда':
        'Решение СМЭС г.Алматы №7527-21-00-2/10685 30 ноября 2021 года с/з отдел взимание № -019090202005/018-вн от 11.01.2022'}],
    'Основания для включения НП в Список ЮЛ, имеющих задолженность более 150 МРП (07.02.2022)':
    [{'Штраф, тенге': '27 170 431,00'},
     {'Пени, тенге': '2 904 485 300,01'},
     {'Сумма основного долга, тенге': '5 570 969 775,51'},
     {
        'Общая сумма налоговой задолженности, не погашенная по истечении 4 месяцев со дня её возникновения':
        '8 502 625 506,52'}],
    
    'Наименование/ФИО налогоплательщика': 'Товарищество с ограниченной ответственностью "НЕМОС"',
    'ИИН/БИН': '160540019486', 
    'РНН': '600700743175',
    'Фамилия, имя, отчество руководителя': 'ГУРЬЕВ СЕРГЕЙ ГЕННАДЬЕВИЧ',
    
    'ИИН руководителя': '580111301922', 
    'РНН руководителя': '600810271319',
    'Код в стране инкорпорации руководителя': ''
    }
