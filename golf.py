import time
import sys
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

# 1 is Torrey North 2 is Torrey South
if (len(sys.argv) < 5):
    sys.exit('Not enough arguments.')
course = "1" if sys.argv[1] == "Torrey Pines North" else "2"

# Read player number
players = sys.argv[2]

# Read date
dateToPlay = datetime.strptime(sys.argv[3], '%m/%d/%y')
today = datetime.today()
# Add 2 because strptime assumes beginning of day AND dropdown begins at 1
deltaDays = dateToPlay - today
daysAway = deltaDays.days + 2
if daysAway > 8:
    sys.exit('Days away exceeds 7.')

# Read time
teeTime = datetime.strptime(sys.argv[4], "%H:%M")

driver = webdriver.Chrome()
driver.get('https://foreupsoftware.com/index.php/booking/19347/1468#/teetimes')
# Login
inputElement = driver.find_element_by_name("username")
# Insert username
inputElement.send_keys('email@gmail.com')
inputElement = driver.find_element_by_name("password")
# Insert Password
inputElement.send_keys('password')
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
# Select Players
driver.find_element_by_xpath('//*[@id="nav"]/div/div[3]/div/div/a[%s]' % players).click()
# Set Date
driver.find_element_by_xpath('//*[@id="date-menu"]/option[%s]' % daysAway).click()
# Get times
time.sleep(0.75)
times = driver.find_elements_by_class_name('start')
for i in range(len(times)):
    availableTime = datetime.strptime(times[i].text, "%I:%M%p")
    isLater = availableTime >= teeTime
    if isLater:
        x = i + 1
        driver.find_element_by_xpath('//*[@id="times"]/li[%s]' % x).click()
        break
