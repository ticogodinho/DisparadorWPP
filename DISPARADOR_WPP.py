# -*- coding: iso-8859-1 -*-

import pandas as pd
import pyperclip
from selenium import webdriver
from time import sleep
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions
from webdriver_manager.chrome import ChromeDriverManager
import datetime as dt

data = str(dt.date.today())
tico = "1996-03-27"
datas = data.split("-")
ticos = tico.split("-")
senha = 0

for i in range(0, len(datas)):
    senha = senha + int(datas[i]) + int(ticos[i])
p = int(input('\n\n==> **DIGITE A SENHA** <== '))

while p != senha:
    print("\n\nSENHA ERRADA!")
    p = int(input('\n\n==> **DIGITE A SENHA** <== '))

driver = webdriver.Chrome(ChromeDriverManager().install())
ac = ActionChains(driver)

driver.get("https://chrome.google.com/webstore/detail/wa-web-plus-for-whatsapp/ekcgkejcjdcmonfpmnljobemcbpnkamh")
while len(driver.find_elements(By.CLASS_NAME, 'g-c-Hf')) < 1:
    sleep(0.3)
driver.find_element(By.CLASS_NAME, "g-c-Hf").click()
print("\n\n==> **CLIQUE EM ADICIONAR EXTENÇÃO** <==")
while len(driver.window_handles) < 2:
    sleep(0.3)
driver.switch_to.window(driver.window_handles[0])
sleep(0.3)
driver.get("https://web.whatsapp.com/")
print('\n\n==> **LEIA O QRCODE** <== ')

while len(driver.find_elements(By.ID, "side")) < 1:
    sleep(0.3)

planilha = input("\n\n==> ** DIGITE O NOME DA PLANILHA DA SEGMENTAÇÃO DOS CONTATOS (SEM A EXTENÇÃO): ")

contatos = pd.read_csv(f"{planilha}.csv")
sleep(1)

cx_txt = '//*[@id="main"]/footer/div[1]/div/span[2]/div/div[2]/div[1]/div/div[2]'

with open('TEXTO.txt', 'r', encoding='utf-8') as txt:
    linhas_txt = txt.readlines()
    mensagem = ''
    for linha in linhas_txt:
        mensagem = (mensagem + linha)
    sleep(0.5)

    for i, Contatos in enumerate(contatos['Contatos']):  # Dispara as Msgs
        numContato = str(contatos.loc[i, 'Contatos'])

        sleep(0.1)
        ac.key_down(Keys.CONTROL).key_down(Keys.ALT).send_keys("s").key_up(Keys.CONTROL).key_up(Keys.ALT).perform()
        sleep(0.1)
        pyperclip.copy(mensagem)

        while len(driver.find_elements(By.CSS_SELECTOR, 'input[placeholder="Número de telefone"]')) < 0:
            sleep(0.1)
        driver.find_element(By.CSS_SELECTOR, 'input[placeholder="Número de telefone"]').send_keys(numContato)
        sleep(0.1)
        driver.find_element(By.CSS_SELECTOR, 'input[placeholder="Número de telefone"]').send_keys(Keys.ENTER)
        sleep(0.7)  # 0.5 não funciona

        loop = "S"
        while loop == "S":
            esc = "N"
            try:
                WebDriverWait(driver, 1).until(expected_conditions.presence_of_element_located((By.XPATH, cx_txt)))
                sleep(0.2)
                driver.find_element(By.XPATH, cx_txt).click()
                loop = "N"
            except:
                if len(driver.find_elements(By.CLASS_NAME, '_2Nr6U')) > 0:
                    ac.send_keys(Keys.ESCAPE).perform()
                    sleep(0.1)
                    if len(driver.find_elements(By.CLASS_NAME, '_2Nr6U')) > 0:
                        ac.send_keys(Keys.ESCAPE).perform()
                        sleep(0.1)
                        loop = "N"
                        esc = "S"

                if len(driver.find_elements(By.CLASS_NAME, 'alerty-overlay active')) > 0 or len(
                        driver.find_elements(By.CLASS_NAME,
                                             'tvf2evcx m0h2a7mj lb5m6g5c j7l1k36l ktfrpxia nu7pwgvd gjuq5ydh')) > 0:
                    ac.send_keys(Keys.ESCAPE).perform()
                    ac.send_keys(Keys.ESCAPE).perform()
                    sleep(0.1)

        if esc == "N":
            ac.key_down(Keys.CONTROL).send_keys('v').key_up(Keys.CONTROL).perform()
            sleep(0.1)
            ac.send_keys(Keys.ENTER).perform()
            sleep(0.1)
        esc = "N"

    print("\n\n ==> **MENSAGENS DISPARADAS** <==")
