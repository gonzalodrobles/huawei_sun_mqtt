# Huawei SUN Jeedom Integration
1- Create a VM to run this code
2- Clone this repo on the VM
3- launch "pip install -r requirements.txt"
4- Rename conf_template.json to conf.json and update it (for DongleFE port=502 and slave=1, for huawei-sun Wifi port=6607 and slave=0)
5- setup a cronjob that runs huawei_sun.py

# Refs
https://skyboo.net/2022/02/huawei-sun2000-why-using-a-usb-dongle-for-monitoring-is-not-a-good-idea
https://pypi.org/project/huawei-solar/