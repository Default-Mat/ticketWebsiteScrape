import os
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.common import TimeoutException
import smtplib
import ssl


# def create_driver():
#     capa = DesiredCapabilities.CHROME
#     capa["pageLoadStrategy"] = "none"
#     op = webdriver.ChromeOptions()
#     # op.add_argument('--headless=new')
#     op.add_experimental_option("detach", True)
#     driver = webdriver.Chrome(desired_capabilities=capa, options=op)
#     return driver
#
#
# def retry_connection(driver):
#     driver.close()
#     driver = create_driver()
#     print('Connection error acquired')
#     time.sleep(3.0)
#     print('Retrying.........')
#     return driver


def sendMail(Sender, Password, Receiver, Message):
    context = ssl.create_default_context()
    smtp = smtplib.SMTP('smtp-mail.outlook.com', 587)
    smtp.ehlo()
    smtp.starttls(context=context)
    smtp.ehlo()
    smtp.login(Sender, Password)
    smtp.sendmail(Sender, Receiver, Message.encode("utf-8"))
    print('email sent!')


def chooseOption():
    choice = input("\n1.shahrud-mashhad\n2.mashhad-shahrud\n3.others\n4.exit\nChoose: ")

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
        exit()

    date = input("enter the date in yyyy-mm-dd format: ")

    options = {"beg": beg, "dest": dest, "date": date}
    return options


def ghasedak_sc(options, driver):
    url = f"https://ghasedak24.com/search/train/{options['beg']}-{options['dest']}/{options['date']}/0/1/0/0/1"
    driver.get(url)
    wait = WebDriverWait(driver, 10)
    wait.until(ec.text_to_be_present_in_element((By.CLASS_NAME, "train-type"), text_="ه"))
    driver.execute_script("window.stop();")
    soup = BeautifulSoup(driver.page_source, "html.parser")
    trains = soup.find_all("div", class_="panel panel-default tkpnl element-item trainPanel")
    foundTickets = ghasedak_showTickets(trains)
    return foundTickets


def respina_sc(options, driver):
    url = f"https://respina24.ir/train/{options['beg']}-{options['dest']}?firstDate={options['date']}" \
          f"&countPassenger=1&typeTicket=3&isCoupe=0&ishotel=0"
    driver.get(url)
    wait = WebDriverWait(driver, 10)
    wait.until(ec.text_to_be_present_in_element((By.CLASS_NAME, "train-name"), text_="ستاره"))
    driver.execute_script("window.stop();")
    soup = BeautifulSoup(driver.page_source, "html.parser")
    trains = soup.find_all("div", class_="train-list ng-scope")
    foundTickets = respina_showTickets(trains)
    return foundTickets


def ghasedak_showTickets(tickets):
    if len(tickets) == 0:
        return "no tickets"

    else:
        string = f"There are {str(len(tickets))} tickets available in ghasedak24\n" \
                 "####################################\n\n"

        for i in tickets:
            train_type = i.find("span", class_='train-type')
            train_departure = i.find("div", class_='departure')
            train_entrance = i.find("div", class_='entrance')
            departure_time = train_departure.find("span", class_='titleModal')
            entrance_time = train_entrance.find("span", class_='titleModal')
            price = i.find("div", class_='price titleModal')
            string += f"{train_type.text} {departure_time.text} {entrance_time.text}\n{price.text}\n\n"

        string += '####################################\n\n'

    return string


def respina_showTickets(tickets):
    if len(tickets) == 0:
        return "no tickets"

    else:
        string = f"There are {str(len(tickets))} tickets available in respina24\n" \
                 "####################################\n\n"

        for i in tickets:
            train_type = i.find("span", class_='tt ng-binding ng-scope')
            train_time = i.find_all("div", class_='train-time ng-binding')
            departure_time = train_time[0]
            entrance_time = train_time[1]
            price = i.find("span", class_='price ng-binding')
            string += f"{train_type.text} {departure_time.text} {entrance_time.text}\n{price.text}\n\n"

        string += '####################################\n\n'

    return string


def main():
    options = chooseOption()
    print("Scraping initiated.......\n")

    sender = 'example@outlook.com'
    password = "example@outlook.com's password"
    receiver = 'example@gmail.com'

    while True:
        capa = DesiredCapabilities.CHROME
        capa["pageLoadStrategy"] = "none"
        op = webdriver.ChromeOptions()
        op.add_argument('--headless=new')
        op.add_experimental_option("detach", True)
        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), desired_capabilities=capa, options=op)

        message = f"""From: From Person <example@outlook.com>
To: To Person <example@gmail.com>
Subject: SMTP e-mail test\n\n"""

        working_sites = 0

        try:
            ghasedak_foundTickets = ghasedak_sc(options, driver)

            if ghasedak_foundTickets == "no tickets":
                print("There are 0 tickets available in ghasedak24")
            else:
                message += f"""{ghasedak_foundTickets}"""
                print(ghasedak_foundTickets)
            working_sites += 1

        except TimeoutException:
            print("\nGhasedak24 is not available at the moment")

        try:
            respina_foundTickets = respina_sc(options, driver)

            if respina_foundTickets == "no tickets":
                print("There are 0 tickets available in respina24")
            else:
                message += f"""{respina_foundTickets}"""
                print(respina_foundTickets)
            working_sites += 1

        except TimeoutException:
            print("\nRespina24 is not available at the moment")

        driver.close()
        if working_sites > 0:
            print('sending details to email.......')
            sendMail(sender, password, receiver, message)
        break


if __name__ == '__main__':
    main()

