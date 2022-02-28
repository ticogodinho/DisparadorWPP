# -*- coding: iso-8859-1 -*-

import pandas as pd
import pyperclip
from selenium import webdriver
from time import sleep
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By

driver = webdriver.Chrome()
ac = ActionChains(driver)

driver.get("https://chrome.google.com/webstore/detail/wa-web-plus-for-whatsapp/ekcgkejcjdcmonfpmnljobemcbpnkamh")
while len(driver.find_elements(By.CLASS_NAME, 'g-c-Hf')) < 1:
    sleep(0.5)
driver.find_element(By.CLASS_NAME, "g-c-Hf").click()
print("\n\n==> **CLIQUE EM ADICIONAR EXTENÇÃO <==")
while len(driver.window_handles) < 2:
    sleep(0.5)
driver.switch_to.window(driver.window_handles[0])
sleep(0.3)
driver.get("https://web.whatsapp.com/")

while len(driver.find_elements(By.ID, "side")) < 1:
    sleep(0.5)

planilha = input("\n\n==> ** DIGITE O NOME DA PLANILHA DA SEGMENTAÇÃO DOS CONTATOS (SEM A EXTENÇÃO): ")

contatos = pd.read_csv(f"C:\\Users\\g.luiz.REDEGERAIS\\Desktop\\Projeto Whatsapp\\{planilha}.csv")
sleep(2)

with open('TEXTO.txt', 'r', encoding='utf-8') as txt:
    linhas_txt = txt.readlines()
    mensagem = ''
    for linha in linhas_txt:
        mensagem = (mensagem + linha)
    sleep(1)

    for i, Contatos in enumerate(contatos['Contatos']):  # Dispara as Msgs
        numContato = str(contatos.loc[i, 'Contatos'])

        ac.key_down(Keys.CONTROL).key_down(Keys.ALT).send_keys("s").key_up(Keys.CONTROL).key_up(Keys.ALT).perform()
        sleep(0.5)

        while len(driver.find_elements(By.CSS_SELECTOR, 'input[placeholder="Número de telefone"]')) < 0:
            sleep(0.1)
        driver.find_element(By.CSS_SELECTOR, 'input[placeholder="Número de telefone"]').send_keys(numContato)
        sleep(0.1)
        driver.find_element(By.CSS_SELECTOR, 'input[placeholder="Número de telefone"]').send_keys(Keys.ENTER)

        if i < 3:
            sleep(1)
        sleep(1.7)

        if len(driver.find_elements(By.CLASS_NAME, "_3J6wB")) > 0:
            ac.send_keys(Keys.ESCAPE).perform()
            sleep(0.1)
            ac.send_keys(Keys.ESCAPE).perform()
            sleep(0.1)
        else:
            pyperclip.copy(mensagem)
            while len(driver.find_elements(
                    By.XPATH, '//*[@id="main"]/footer/div[1]/div/span[2]/div/div[2]/div[1]/div/div[2]')) == 0:
                sleep(0.1)
            driver.find_element(
                By.XPATH, '//*[@id="main"]/footer/div[1]/div/span[2]/div/div[2]/div[1]/div/div[2]').click()
            ac.key_down(Keys.CONTROL).send_keys('v').key_up(Keys.CONTROL).perform()
            sleep(0.2)
            ac.send_keys(Keys.ENTER).perform()

    print("\n\n ==> **MENSAGENS DISPARADAS** <==")
