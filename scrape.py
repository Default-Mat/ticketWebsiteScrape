import os
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities


def showTickets(tickets):
    if len(tickets) == 0:
        print("####################################")
        print("\nThere are " + str(len(trains)) + " tickets available\n")
        print("####################################")

    else:
        print("####################################")
        print("There are " + str(len(trains)) + " tickets available\n")
        for i in tickets:
            train_type = i.find("span", class_='train-type')
            train_departure = i.find("div", class_='departure')
            train_entrance = i.find("div", class_='entrance')
            departure_time = train_departure.find("span", class_='titleModal')
            entrance_time = train_entrance.find("span", class_='titleModal')
            price = i.find("div", class_='price titleModal')
            print(train_type.text + ' ' + departure_time.text + ' ' + entrance_time.text)
            print(price.text + '\n')
        print("####################################")


while True:
    choice = input("\n1.shahrud-mashhad\n2.mashhad-shahrud\n3.others\n4.exit\nChoose: ")
    os.system('cls')

    if choice == '1':
        beg = "shahrud"
        dest = "mashhad"

    elif choice == '2':
        beg = "mashhad"
        dest = "shahrud"

    elif choice == '3':
        beg = input("enter the beginning point: ")
        dest = input("enter the destination: ")

    else:
        os.system('exit')
        break

    date = input("enter the date in yyyy-mm-dd format: ")

    url = "https://ghasedak24.com/search/train/" + beg + "-" + dest + "/" + date + "/1/0/0/1/"
    print("Please wait.......")

    capa = DesiredCapabilities.CHROME
    capa["pageLoadStrategy"] = "none"
    options = webdriver.ChromeOptions()
    options.headless = False
    driver = webdriver.Chrome(service=Service("c:/webdriver/chromedriver.exe"), desired_capabilities=capa,
                              options=options)
    wait = WebDriverWait(driver, 20)
    driver.get(url)

    try:
        wait.until(ec.text_to_be_present_in_element((By.CLASS_NAME, "train-type"), text_="ه"))
        driver.execute_script("window.stop();")
        soup = BeautifulSoup(driver.page_source, "html.parser")
        trains = soup.find_all("div", class_="panel panel-default tkpnl element-item trainPanel")
        showTickets(trains)
        driver.close()

    except:
        print("\nNo tickets available at the moment")
        driver.close()

    input("\npress enter to continue...")
    os.system('cls')
    continue