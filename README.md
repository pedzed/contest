# ConTest
_**Continuous testing** made easy._


## Pre-requisites
- Python 3 (installation with `pyenv` recommended)
    - pip3 dependency installation module


## Installation
```bash
# Set up
mkdir -p "$HOME/contest-install"
cd "$HOME/contest-install"

# pigpio (Pi GPIO)
# Follow instructions at http://abyz.me.uk/rpi/pigpio/download.html or:
wget abyz.me.uk/rpi/pigpio/pigpio.zip
unzip pigpio.zip
cd PIGPIO
make
sudo make install

# AutomationHAT (optional)
curl -sS https://get.pimoroni.com/automationhat | bash

# PIP dependencies
pip install -r requirements.txt

# J-Link Flashing
curl 'https://www.segger.com/downloads/jlink/JLink_Linux_arm.tgz' --data 'accept_license_agreement=accepted' --compressed -o jlink.tgz
tar -xvzf jlink.tgz && mv JLink_* jlink
sudo mv jlink /opt/jlink
sudo ln -s /opt/jlink/JLinkExe /usr/local/bin

# Tear down
rm -rf "$HOME/contest-install"
```


## Usage
### Drivers
#### TTN Data Storage
To get results from The Things Network (TTN), the Data Storage integration could be used. In order to get data, check out the `ttn_data_storage` driver.


## Development & Testing
### Provided Examples
In order to run the examples from the `/examples` directory, run this command first:
```bash
pip3 install -e .
```

Then the examples can be run:
```bash
python3 -m pytest examples/officehawk/officehawk.py
python3 -m pytest examples/flashing/jlink.py
```

### Unit Testing
In order to unit test the library, install the dependencies on the ConTest device and run:
```bash
python3 setup.py test
# Or:
python3 -m pytest
```


## Further Reading
### Flashing (J-Link)
To program the J-Link Commander, chapter 3.2 of Segger's J-Link datasheet may come of use: https://www.segger.com/downloads/jlink/UM08001
