import pytest
from settings import valid_email, valid_password
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options

"""

element = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "myDynamicElement"))
)
WebDriverWait — это специальный класс WebDriver, который помогает нам в реализации явных ожиданий. 
Для того чтобы экземпляр этого класса заработал в проекте, мы передаём в него 2 аргумента:

*Переменную с текущим веб-драйвером.
*Время максимального ожидания в секундах.

То есть запись WebDriverWait(driver, 10) означает, что мы настроили для веб-драйвера driver ожидание некоторого условия, 
указанного в аргументах функции until, в течение 10 секунд. Если в течение 10 секунд это условие выполнено не будет, 
то возникнет исключение, которые мы можем обработать в тесте.
"""



"""
Тесты связанные с питомцами пользователя:

Присутствуют все питомцы.
Хотя бы у половины питомцев есть фото.
У всех питомцев есть имя, возраст и порода.
У всех питомцев разные имена.
В списке нет повторяющихся питомцев. (Сложное задание).

"""


"""
Проверяем что зашли на страницу МОИ ПИТОМЦЫ. Сохраняем скриншот
"""
@pytest.fixture()
def test_show_my_pets():
   # Ищем и вводим свой email
   element = WebDriverWait(pytest.driver, 10).until(EC.presence_of_element_located((By.ID, "email")))
   pytest.driver.find_element(By.ID,'email').send_keys(valid_email)

   #Ищем и вводим свой пароль
   element = WebDriverWait(pytest.driver, 10).until(EC.presence_of_element_located((By.ID, "pass")))
   pytest.driver.find_element(By.ID,'pass').send_keys(valid_password)

   # Нажимаем на кнопку входа в аккаунт
   element = WebDriverWait(pytest.driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, "button[type='submit']")))
   pytest.driver.find_element(By.CSS_SELECTOR,'button[type="submit"]').click()

   # Нажимаем на ссылку "Мои питомцы"
   element = WebDriverWait(pytest.driver, 10).until(EC.presence_of_element_located((By.LINK_TEXT, "Мои питомцы")))
   pytest.driver.find_element(By.LINK_TEXT, "Мои питомцы").click()

   #Делаем скриншот
   pytest.driver.save_screenshot("my_pets.png")

   # Проверяем что мы оказались на странице "Мои питомцы"
   assert pytest.driver.current_url == 'https://petfriends.skillfactory.ru/my_pets', "Ошибка, находимся не на странице Мои питомцы!"

"""
Присутствуют все мои питомцы
"""
def test_all_my_pets_my_pets(test_show_my_pets):

   # Сохраняем в переменную statistic элементы статистики количества моих питомцев
   element = WebDriverWait(pytest.driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, ".\\.col-sm-4.left")))
   statistic = pytest.driver.find_elements(By.CSS_SELECTOR,".\\.col-sm-4.left")

   # Сохраняем в переменную pets количесвто элементов карточек питомцев
   element = WebDriverWait(pytest.driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, ".table.table-hover tbody tr")))
   my_pets = pytest.driver.find_elements(By.CSS_SELECTOR,'.table.table-hover tbody tr')

   # Получаем количество питомцев из данных статистики
   number = statistic[0].text.split('\n')
   number = number[1].split(' ')
   number = int(number[1])

   # Получаем количество карточек питомцев
   number_of_pets = len(my_pets)

   # Проверяем что количество питомцев из статистики совпадает с количеством карточек питомцев
   assert number == number_of_pets, "Количество питомцев не совпадает"

"""
Хотя бы у половины питомцев есть фото.
"""
def test_photo_has_half_pets(test_show_my_pets):

   # Сохраняем в переменную ststistic элементы статистики
   element = WebDriverWait(pytest.driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, ".\\.col-sm-4.left")))
   statistic = pytest.driver.find_elements(By.CSS_SELECTOR,".\\.col-sm-4.left")

   # Сохраняем в переменную images элементы с атрибутом img
   images = pytest.driver.find_elements(By.CSS_SELECTOR,'.table.table-hover img')

   # Получаем количество питомцев из данных статистики
   number = statistic[0].text.split('\n')
   number = number[1].split(' ')
   number = int(number[1])

   # Находим половину от количества питомцев
   half = number // 2

   # Находим количество питомцев с фотографией
   number_а_photos = 0
   for i in range(len(images)):
      if images[i].get_attribute('src') != '':
         number_а_photos += 1

   # Проверяем что количество питомцев с фотографией больше или равно половине количества питомцев
   assert number_а_photos >= half
   print(f'количество фото: {number_а_photos}')
   print(f'Половина от числа питомцев: {half}')

"""
У всех питомцев есть имя, возраст и порода.
"""

def test_pet_have_name_age_animal_type(test_show_my_pets):
   element = WebDriverWait(pytest.driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, ".table.table-hover tbody tr")))
   # Сохраняем в переменную pet_data элементы с данными о питомцах
   pet_data = pytest.driver.find_elements(By.CSS_SELECTOR, '.table.table-hover tbody tr')

   # Перебираем данные из pet_data, оставляем имя, возраст, и породу остальное меняем на пустую строку
   # и разделяем по пробелу. Находим количество элементов в получившемся списке и сравниваем их
   # с ожидаемым результатом
   for i in range(len(pet_data)):
      data_pet = pet_data[i].text.replace('\n', '').replace('×', '')
      split_data_pet = data_pet.split(' ')
      result = len(split_data_pet)
      assert result == 3

"""
У всех питомцев разные имена.
"""

def test_all_pets_have_different_names(test_show_my_pets):
   # Сохраняем в переменную pet_data элементы с данными о питомцах
   element = WebDriverWait(pytest.driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, ".table.table-hover tbody tr")))
   pet_data = pytest.driver.find_elements(By.CSS_SELECTOR,'.table.table-hover tbody tr')

   # Перебираем данные из pet_data, оставляем имя, возраст, и породу остальное меняем на пустую строку
   # и разделяем по пробелу.Выбераем имена и добавляем их в список pets_name.
   pets_name = []
   for i in range(len(pet_data)):
      data_pet = pet_data[i].text.replace('\n', '').replace('×', '')
      split_data_pet = data_pet.split(' ')
      pets_name.append(split_data_pet[0])

   # Перебираем имена и если имя повторяется то прибавляем к счетчику k единицу.
   # Проверяем, если r == 0 то повторяющихся имен нет.
   k = 0
   for i in range(len(pets_name)):
      if pets_name.count(pets_name[i]) > 1:
         k += 1
   assert k == 0
   print(k)
   print(pets_name)

"""
В списке нет повторяющихся питомцев. (Сложное задание).
"""

def test_no_duplicate_pets(test_show_my_pets):
   element = WebDriverWait(pytest.driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, ".table.table-hover tbody tr")))

   # Сохраняем в переменную pet_data элементы с данными о питомцах
   pet_data = pytest.driver.find_elements(By.CSS_SELECTOR,'.table.table-hover tbody tr')

   # Перебираем данные из pet_data, оставляем имя, возраст, и породу остальное меняем на пустую строку
   # и разделяем по пробелу.
   list_data = []
   for i in range(len(pet_data)):
      data_pet = pet_data[i].text.replace('\n', '').replace('×', '')
      split_data_pet = data_pet.split(' ')
      list_data.append(split_data_pet)

   # Склеиваем имя, возраст и породу, получившиеся склееные слова добавляем в строку
   # и между ними вставляем пробел
   line = ''
   for i in list_data:
      line += ''.join(i)
      line += ' '

   # Получаем список из строки line
   list_line = line.split(' ')

   # Превращаем список в множество
   set_list_line = set(list_line)

   # Находим количество элементов списка и множества
   a = len(list_line)
   b = len(set_list_line)

   # Из количества элементов списка вычитаем количество элементов множества
   result = a - b

   # Если количество элементов == 0 значит карточки с одинаковыми данными отсутствуют
   assert result == 0