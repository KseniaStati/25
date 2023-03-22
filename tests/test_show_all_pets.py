import pytest
from settings import valid_email, valid_password
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

#'''Проверка карточек питомцев'''
def test_show_all_pets():
   # Устанавливаем неявное ожидание
   pytest.driver.implicitly_wait(10)
   # Вводим email
   pytest.driver.find_element(By.ID,'email').send_keys(valid_email)
   # Вводим пароль
   pytest.driver.find_element(By.ID,'pass').send_keys(valid_password)
   # Нажимаем на кнопку входа в аккаунт
   pytest.driver.find_element(By.CSS_SELECTOR,'button[type="submit"]').click()
   # Проверяем, что мы оказались на главной странице
   assert pytest.driver.current_url == 'https://petfriends.skillfactory.ru/all_pets'
   images = pytest.driver.find_elements(By.CSS_SELECTOR,'.card-deck .card-img-top')
   names = pytest.driver.find_elements(By.CSS_SELECTOR,'.card-deck .card-title')
   descriptions = pytest.driver.find_elements(By.CSS_SELECTOR,'.card-deck .card-text')
   assert names[0].text != ''
   pytest.driver.save_screenshot("all_pets.png")


   # for i in range(len(names)):
   #    assert images[i].get_attribute('src') != '', "у некоторых питомцев нет фото"        #Проверяем есть ли картинка
   #    assert names[i].text != ''   , "у некоторых питомцев нет имени"                       #Проверяем есть ли текст
   #    assert descriptions[i].text != ''
   #    assert ',' in descriptions[i].text
   #    parts = descriptions[i].text.split(", ")
   #    assert len(parts[0]) > 0
   #    assert len(parts[1]) > 0

