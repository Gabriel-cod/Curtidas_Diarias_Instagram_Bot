from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions
from selenium.common.exceptions import *
from time import sleep

def iniciar_driver():
    chrome_options = Options()
    arguments = ['--lang=pt-BR', '--start-maximized', '--incognito']
    for argument in arguments:
        chrome_options.add_argument(argument)

    chrome_options.add_experimental_option('prefs', {
        'download.prompt_for_download': False,
        'profile.default_content_setting_values.notifications': 2,
        'profile.default_content_setting_values.automatic_downloads': 1,
    })
    driver = webdriver.Chrome(service=ChromeService(
        ChromeDriverManager().install()), options=chrome_options)

    wait = WebDriverWait(
        driver=driver,
        timeout=10,
        poll_frequency=1,
        ignored_exceptions=[
            NoSuchElementException,
            ElementNotInteractableException,
            ElementNotSelectableException,
            ElementNotVisibleException
        ]
    )
    
    return driver, wait


driver, wait = iniciar_driver()

email = '<<< email do Intagram do usuário >>>'
senha = '<<< senha do Instagram do usuário >>>'

# Processo de autenticação e login
driver.get("https://www.instagram.com/")

email_field = wait.until(expected_conditions.element_to_be_clickable((By.XPATH, "//input[@name='username']")))
email_field.send_keys(email); sleep(2)

password_field = driver.find_element(By.XPATH, "//input[@name='password']")
password_field.send_keys(senha); sleep(2)

entrar_button = wait.until(expected_conditions.element_to_be_clickable((By.XPATH, "//button[@type='submit']")))
entrar_button.click(); sleep(15)

while True:
    # acessar o perfil e aguardar até que o primeiro post seja visível e clicável
    driver.get('<<< url do perfil a ser monitorado >>>'); sleep(10)

    posts = wait.until(expected_conditions.visibility_of_any_elements_located((By.XPATH, "//div[@class='_aagu']")))
    sleep(1)
    posts[0].click(); sleep(5)

    # Descobrir se post ja foi curtido
    curtido_button = driver.find_element(By.XPATH, "//span[@class='_aamw']//div//div//span//*[local-name()='svg']"); sleep(2)
    status_curtir_button = curtido_button.get_attribute('color')
    if status_curtir_button in 'rgb(255, 48, 64)': # coração vermelho
        sleep(86400)
    else: # coração branco
        curtir_button = driver.find_element(By.XPATH, "//span[@class='_aamw']//div//div"); sleep(1)
        curtir_button.click()
        sleep(86400)
