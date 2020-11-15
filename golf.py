import time
import sys
import datetime
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from time import sleep
import configparser
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

# Read credentials from config.txt
configParser = configparser.RawConfigParser()   
configFilePath = r'config.txt'
configParser.read(configFilePath)

# 1 is Torrey North 2 is Torrey South
if (len(sys.argv) < 5):
    sys.exit('Not enough arguments.')
course = "1" if sys.argv[1] == "Torrey Pines North" else "2"

# Read player number
players = sys.argv[2]

# if length of args == 5 then set wait flag to true
if (len(sys.argv) == 6):
    waitFlag = True
    waitTime = datetime.datetime.strptime(sys.argv[5], "%H:%M")
else:
    waitFlag = False

# Read date
dateToPlay = datetime.datetime.strptime(sys.argv[3], '%m-%d-%y')
today = datetime.datetime.today()
# Add 2 because strptime assumes beginning of day AND dropdown begins at 1
deltaDays = dateToPlay - today
daysAway = deltaDays.days + 2
if daysAway > 8:
    sys.exit('Days away exceeds 7.')

# Read time
teeTime = datetime.datetime.strptime(sys.argv[4], "%H:%M")

# Start browser maximized
options = webdriver.ChromeOptions()
options.add_argument("--start-maximized")
driver = webdriver.Chrome(options=options)
driver.get('https://foreupsoftware.com/index.php/booking/19347/1468#/teetimes')

# Login
inputElement = driver.find_element_by_name("username")
# Insert username
inputElement.send_keys(configParser.get('credentials', 'username'))
inputElement = driver.find_element_by_name("password")
# Insert Password
inputElement.send_keys(configParser.get('credentials', 'password'))
inputElement.send_keys(Keys.RETURN)
time.sleep(2)
# Have to refresh page to load buttons
driver.refresh()
buttons = driver.find_elements_by_xpath('//*[@id="content"]/div/button[1]')
for btn in buttons:
    btn.click()
time.sleep(2)
# Select Course
driver.find_element_by_xpath('//*[@id="schedule_select"]/option[%s]' % course).click()
# Set Date
dateElement = driver.find_element_by_xpath('//*[@id="date-field"]')
dateElement.send_keys(Keys.CONTROL + "a");
dateElement.send_keys(Keys.DELETE);
print(dateToPlay.strftime("%M-%d-%Y"))
dateElement.send_keys(dateToPlay.strftime("%m-%d-%Y"))
dateElement.send_keys(Keys.ENTER);

# Wait until 7:00
if waitFlag:
    today = datetime.datetime.today()
    startTime = datetime.datetime.combine(today, waitTime.time())
    print("Sleeping until: " + startTime.strftime("%H:%M:%S"))
    while startTime.time() > datetime.datetime.today().time(): # you can add here any additional variable to break loop if necessary
        sleep(1)

# Select Players
driver.find_element_by_xpath('//*[@id="nav"]/div/div[3]/div/div/a[%s]' % players).click()

# Get times
WebDriverWait(driver, 20, poll_frequency=.1).until(EC.visibility_of_element_located((By.CLASS_NAME, "loading")))
WebDriverWait(driver, 20, poll_frequency=.1).until(EC.invisibility_of_element_located((By.CLASS_NAME, "loading")))

#time.sleep(0.3)
booked = False
while booked == False:
    times = driver.find_elements_by_class_name('start')
    for i in range(len(times)):
        availableTime = datetime.datetime.strptime(times[i].text, "%I:%M%p")
        isLater = availableTime >= teeTime
        if isLater:
            x = i + 1
            try:
                driver.find_element_by_xpath('//*[@id="times"]/li[%s]' % x).click()
                driver.find_element_by_id("book_time")
            except:
                break
            else:
                booked = True
