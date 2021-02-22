
from selenium import webdriver
from time import sleep
import yaml

booking_details = {}

with open("booking.yaml", 'r') as stream:
    try:
        booking_details = yaml.safe_load(stream)
    except yaml.YAMLError as exc:
        print(exc)
        exit(0)

if 'firefox' in booking_details['browser']:
    driver = webdriver.Firefox(executable_path=booking_details['browser']['firefox'])
elif 'chrome' in booking_details['chrome']:
    driver = webdriver.Chrome(executable_path=booking_details['browser']['chrome'])
else:
    driver = {}
    print('browser option does not exist')
    exit(0)

driver.get("https://iiscgym.iisc.ac.in/gfr/")

driver.find_element_by_xpath("//*[@id='email']").send_keys(booking_details['login']['username'])
driver.find_element_by_xpath("//*[@id='pass']").send_keys(booking_details['login']['password'])
driver.find_element_by_xpath("//*[@id='login']").click()

for facility in booking_details['facility']:

    if facility == 'gymnasium':
        label = 1
    elif facility == 'badminton':
        label = 2
    elif facility == 'table tennis':
        label = 3
    else:
        label = 0
        print('facility {} does not exist', facility)
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

    # Slot is full
    while driver.find_element_by_xpath('//*[@id="msg_box"]').text == 'Time slot not selected !':

        sleep(1)
        driver.find_element_by_xpath('//*[@id="mdl_msg_box"]').click()
        sleep(1)

        if (time + counter > booking_details['number_of_slots'][facility] and time - counter < 1) or \
                counter > booking_details['lookup_range']:
            print('No slot available for {} in your booking range'.format(facility))
            exit(0)

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

    sleep(1)
    for i in range(1, 5):
        driver.find_element_by_xpath('/html/body/div[2]/div[1]/div/div/div[2]/ul/li[{}]/div/label'.format(i)).click()

    driver.find_element_by_xpath('//*[@id="btn_add"]').click()

    sleep(1)
    driver.find_element_by_xpath('//*[@id="mdl_msg_box"]').click()
    sleep(1)

driver.find_element_by_xpath('/html/body/div[1]/div[3]/div[2]/button').click()
sleep(1)
driver.find_element_by_xpath('//*[@id="logout"]').click()

driver.close()

