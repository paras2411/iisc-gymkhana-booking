
from selenium import webdriver
from selenium.webdriver import FirefoxOptions
from time import sleep
import yaml
import datetime

now = datetime.datetime.now().time()

if now >= datetime.time(hour=17, minute=0, second=0) or now < datetime.time(hour=5, minute=30, second=0):
    print('Booking is closed for today')
    exit(0)

booking_details = {}

with open("booking.yaml", 'r') as stream:
    try:
        booking_details = yaml.safe_load(stream)
    except yaml.YAMLError as exc:
        print(exc)
        exit(0)

if 'firefox' in booking_details['browser']:

    if booking_details['headless']:
        opts = FirefoxOptions()
        opts.add_argument("--headless")
        driver = webdriver.Firefox(options=opts)
    else:
        driver = webdriver.Firefox(executable_path=booking_details['browser']['firefox'])

elif 'chrome' in booking_details['browser']:

    driver = webdriver.Chrome(executable_path=booking_details['browser']['chrome'])

else:

    driver = {}
    print('{} browser option does not exist'.format(booking_details['browser']))
    exit(0)

driver.get("https://iiscgym.iisc.ac.in/gfr/")

driver.find_element_by_xpath("//*[@id='email']").send_keys(booking_details['login']['username'])
driver.find_element_by_xpath("//*[@id='pass']").send_keys(booking_details['login']['password'])
driver.find_element_by_xpath("//*[@id='login']").click()

acknowledged = False

for facility in booking_details['facility']:

    if facility == 'gymnasium':
        label = 1
    elif facility == 'badminton':
        label = 2
    elif facility == 'table tennis':
        label = 3
    else:
        label = 0
        print('Facility {} does not exist', facility)
        exit(0)

    driver.find_element_by_xpath('/html/body/div[2]/div[4]/div/div/div[2]/div/label[{}]'.format(label)).click()
    sleep(2)

    if 'booked' not in driver.find_element_by_xpath('//*[@id="msg_box"]').text:
        driver.find_element_by_xpath('/html/body/div[2]/div[4]/div/div/div[1]/div/div/label').click()
        sleep(2)

    if 'booked' in driver.find_element_by_xpath('//*[@id="msg_box"]').text:
        print('Slot already booked for {}'.format(facility))
        driver.find_element_by_xpath('//*[@id="mdl_msg_box"]').click()
        sleep(2)
        continue

    if booking_details['facility'][facility] == 13:
        print('13-14 slot does not exist')
        continue

    time = booking_details['facility'][facility] - 5
    if time > 7:
        time -= 1
    if time < 1 or time > booking_details['number_of_slots'][facility]:
        print('{} not a valid time for {}'.format(booking_details['facility'][facility], facility))
        exit(0)

    driver.find_element_by_xpath('/html/body/div[2]/div[4]/div/div/div[3]/div[{}]/div[1]'.format(time)).click()
    driver.find_element_by_xpath('//*[@id="btn_chk"]').click()
    counter = 1

    skip_booking = False
    # Slot is full
    while driver.find_element_by_xpath('//*[@id="msg_box"]').text == 'Time slot not selected !':

        sleep(1)
        driver.find_element_by_xpath('//*[@id="mdl_msg_box"]').click()
        sleep(1)

        if (time + counter > booking_details['number_of_slots'][facility] and time - counter < 1) or \
                counter > booking_details['lookup_range']:
            print('No slot available for {} in your booking range'.format(facility))
            skip_booking = True
            break

        if 'before' in booking_details['lookup'] and time - counter > 0:
            driver.find_element_by_xpath('/html/body/div[2]/div[4]/div/div/div[3]/div[{}]/div[1]'.
                                         format(time - counter)).click()
            driver.find_element_by_xpath('//*[@id="btn_chk"]').click()

        if driver.find_element_by_xpath('//*[@id="msg_box"]').text != 'Time slot not selected !':
            break

        sleep(1)
        driver.find_element_by_xpath('//*[@id="mdl_msg_box"]').click()
        sleep(1)

        if 'after' in booking_details['lookup'] and time + counter < 15:
            driver.find_element_by_xpath('/html/body/div[2]/div[4]/div/div/div[3]/div[{}]/div[1]'.
                                         format(time + counter)).click()
            driver.find_element_by_xpath('//*[@id="btn_chk"]').click()

        counter += 1

    if skip_booking:
        continue

    sleep(1)
    if not acknowledged:
        for i in range(1, 5):
            driver.find_element_by_xpath('/html/body/div[2]/div[1]/div/div/div[2]/ul/li[{}]/div/label'.format(i)).click()
        acknowledged = True

    driver.find_element_by_xpath('//*[@id="btn_add"]').click()

    sleep(1)
    driver.find_element_by_xpath('//*[@id="mdl_msg_box"]').click()
    sleep(1)

driver.find_element_by_xpath('/html/body/div[1]/div[3]/div[2]/button').click()
sleep(1)
driver.find_element_by_xpath('//*[@id="logout"]').click()

driver.close()

