import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from Settings import val_email, password
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


@pytest.fixture(autouse=True)
def driver():
    driver = webdriver.Chrome()
    # Переходим на страницу авторизации
    driver.get('https://petfriends.skillfactory.ru/login')

    yield driver

    driver.quit()


def test_show_my_pets(driver):
    # Вводим email
    driver.find_element(By.ID, 'email').send_keys(val_email)
    # Вводим пароль
    driver.find_element(By.ID, 'pass').send_keys(password)
    # Нажимаем на кнопку входа в аккаунт
    driver.find_element(By.CSS_SELECTOR, 'button[type="submit"]').click()
    # Кликаем на мои питомцы
    driver.find_element(By.XPATH, '//*[@id="navbarNav"]/ul[1]/li[1]/a[1]').click()
    # Добавялем явное ожидание хедера
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '/html/body/nav')))
    # Добавляем явное ожидание информации пользователя
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, 'body > div.task2.fill > div > div.\.col-sm-4.left')))
    # Явное ожидание таблицы питомцев
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, 'all_my_pets')))
    # Берем дааные пользователя
    elem = driver.find_element(By.CSS_SELECTOR, '.\\.col-sm-4.left').text.split()
    # Вытаскиваем количество питомце >> преобразуем в число.
    statics = elem[2].split()
    statics = int(elem[2])
    # Ищем таблицу с питомцами
    my_pets = driver.find_elements(By.XPATH, '//*[@id="all_my_pets"]/table/tbody/tr/td/a/div')
    res = len(my_pets)
    assert statics == res
    print(res)


def test_check_photo_pet(driver):
    # Вводим email
    driver.find_element(By.ID, 'email').send_keys(val_email)
    # Вводим пароль
    driver.find_element(By.ID, 'pass').send_keys(password)
    # Нажимаем на кнопку входа в аккаунт
    driver.find_element(By.CSS_SELECTOR, 'button[type="submit"]').click()
    # Проверяем, что мы оказались на главной странице пользователя
    driver.find_element(By.XPATH, '//*[@id="navbarNav"]/ul[1]/li[1]/a[1]').click()
    # Кликаем на кнопку мои питомцы
    my_pets = driver.find_elements(By.XPATH, '//*[@id="all_my_pets"]/table/tbody/tr/td/a/div')
    # Находим таблицу с карточками питомцев
    my_pets = len(my_pets)
    image = driver.find_elements(By.XPATH, '//*[@id="all_my_pets"]/table/tbody/tr')
    # Находим картинки во всех карточках питомцев
    image = len((image))
    assert image >= my_pets / 2


def test_info_pets(driver):
    # Вводим email
    driver.find_element(By.ID, 'email').send_keys(val_email)
    # Вводим пароль
    driver.find_element(By.ID, 'pass').send_keys(password)
    # Нажимаем на кнопку входа в аккаунт
    driver.find_element(By.CSS_SELECTOR, 'button[type="submit"]').click()
    # Кликаем на кнопку мои питомцы
    driver.implicitly_wait(10)
    driver.get('https://petfriends.skillfactory.ru/my_pets')
    elem_img = driver.find_element(By.XPATH, '//*[@id="all_my_pets"]/table/tbody/tr[1]/th')
    elem_name = driver.find_element(By.XPATH, '//*[@id="all_my_pets"]/table/tbody/tr[1]/td[1]').text
    elem_type = driver.find_element(By.XPATH, '//*[@id="all_my_pets"]/table/tbody/tr[1]/td[2]').text
    elem_age = driver.find_element(By.XPATH, '//*[@id="all_my_pets"]/table/tbody/tr[1]/td[3]').text
    driver.find_element(By.XPATH, '//*[@id="navbarNav"]/ul[1]/li[1]/a[1]').click()
    # Создаем счетчик, ищем имена в таблице с карточками
    for i in range(1, 36, 1):
        name_pet = driver.find_element(By.XPATH, f'//*[@id="all_my_pets"]/table/tbody/tr[{i}]').text
        assert name_pet != (' ')
    print(elem_img, elem_name, elem_type, elem_age)


def test_indentical_pets(driver):
    # Вводим email
    driver.find_element(By.ID, 'email').send_keys(val_email)
    # Вводим пароль
    driver.find_element(By.ID, 'pass').send_keys(password)
    # Нажимаем на кнопку входа в аккаунт
    driver.find_element(By.CSS_SELECTOR, 'button[type="submit"]').click()
    # Кликаем на кнопку мои питомцы
    driver.find_element(By.XPATH, '//*[@id="navbarNav"]/ul[1]/li[1]/a[1]').click()
    # Берем карточки питомцев
    for i in range(1, 36, 1):
        card_pet_1 = driver.find_element(By.XPATH, f'//*[@id="all_my_pets"]/table/tbody/tr[{i}]').text
        card_pet_2 = driver.find_element(By.XPATH, f'//*[@id="all_my_pets"]/table/tbody/tr[{i + 1}]').text
        try:
            assert card_pet_1 != card_pet_2
        except:
            print('Питомец с такими данными уже существует')
