# iisc-gymkhana-booking

### Steps to follow to add this automation booking to your system

* Install selenium and pyyaml python library (pip install selenium, pip install pyyaml)
* For firefox, make sure you have geckodriver. If not follow [this link](https://askubuntu.com/questions/870530/how-to-install-geckodriver-in-ubuntu). 
* Add the path to geckodriver in the booking.yaml
* Update booking.yaml with your username and password and the other details required as per your booking slot.
* Add the cronjob mentioned in the crontab.txt in your system crontab using "crontab -e"
* You can update the time to some other time as per your requirement. See crontab syntax for doing so.
