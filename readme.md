# Client utility for PN512 NFC Tag Reader/Writer Emulator

## Usage

To read all pages on the tag and write them to a file

```shell
python readerClient.py --readerPath="addr" --file="pageData.txt" --cmd=writeToFile
```
To write all pages defined in the file to to the tag
```shell
python readerClient.py --readerPath="addr" --file="pageData.txt" --cmd=readFromFile
```

replace addr with one of the following

**Windows**

Where addr is the com port number on your windows based system. check serial ports node in device manager for example COM10

**raspberry pi**

addr will be the CDC serial device path /dev/ttyACMx where x will be a number likely 0

for example
```shell
git clone https://github.com/rhysbryant/readerEmulatorClient/
sudo python ./readerEmulatorClient/readerClient.py --readerPath=/dev/ttyACM0 --file=dump.txt --cmd readFromFile
```

## Using in your project

```python
from readerEmulatorClient import readerClient
from readerEmulatorClient import readerSerialConnection

c = readerSerialConnection.Connection()
c.connect(addr)
reader = ReaderEmulator(c)
reader.writePagesFromFile('pages.txt')
```

# License

LGPL

# What to Contribute?

sure pull requests are welcome. Please raise an issue first with a description of the problem or desired feature. so the pull request is not completely unexpected.