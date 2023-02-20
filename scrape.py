import os
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
import smtplib
import ssl
import time


def showTickets(tickets):
    if len(tickets) == 0:
        return "no tickets"

    else:
        string = f"""There are {str(len(tickets))} tickets available
####################################\n\n"""

        for i in tickets:
            train_type = i.find("span", class_='train-type')
            train_departure = i.find("div", class_='departure')
            train_entrance = i.find("div", class_='entrance')
            departure_time = train_departure.find("span", class_='titleModal')
            entrance_time = train_entrance.find("span", class_='titleModal')
            price = i.find("div", class_='price titleModal')
            string += f"{train_type.text} {departure_time.text}" \
                      f" {entrance_time.text}\n{price.text}\n\n"
    return string


def sendMail(Sender, Password, Receiver, Message):
    context = ssl.create_default_context()
    smtp = smtplib.SMTP('smtp-mail.outlook.com', 587)
    smtp.ehlo()
    smtp.starttls(context=context)
    smtp.ehlo()
    smtp.login(Sender, Password)
    smtp.sendmail(Sender, Receiver, Message.encode("utf-8"))
    print('email sent!')


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

url = "https://ghasedak24.com/search/train/" + beg + "-" + dest + "/" + date + "/1/0/0/1/"
print("Scraping initiated.......")

sender = 'matin.arno4646@outlook.com'
password = '34129093428198matin'
receiver = 'matin.geralt6565@gmail.com'

while True:
    capa = DesiredCapabilities.CHROME
    capa["pageLoadStrategy"] = "none"
    options = webdriver.ChromeOptions()
    options.add_argument('--headless=new')
    driver = webdriver.Chrome(desired_capabilities=capa, options=options)
    wait = WebDriverWait(driver, 30)
    driver.get(url)

    message = f"""From: From Person <matin.arno4646@outlook.com>
To: To Person <matin.geralt6565@gmail.com>
Subject: SMTP e-mail test\n\n"""

    try:
        wait.until(ec.text_to_be_present_in_element((By.CLASS_NAME, "train-type"), text_="ه"))
        driver.execute_script("window.stop();")
        soup = BeautifulSoup(driver.page_source, "html.parser")
        trains = soup.find_all("div", class_="panel panel-default tkpnl element-item trainPanel")
        foundTickets = showTickets(trains)
        driver.close()
        if foundTickets == "no tickets":
            print("There are 0 tickets available")

        else:
            message += f"""{foundTickets}
####################################"""
            sendMail(sender, password, receiver, message)

    except:
        print("\nNo tickets available at the moment")
        driver.close()

    time.sleep(3600)