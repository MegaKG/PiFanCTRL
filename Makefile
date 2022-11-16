SRC=src
BUILD=build
VERSION=1.0-0
CONFIG=config




deb:
	mkdir $(BUILD)
	mkdir $(BUILD)/FanCTRL-$(VERSION)
	mkdir $(BUILD)/FanCTRL-$(VERSION)/DEBIAN
	cp -v $(SRC)/control $(BUILD)/FanCTRL-$(VERSION)/DEBIAN/control
	mkdir -p $(BUILD)/FanCTRL-$(VERSION)/usr/sbin

	mkdir -p $(BUILD)/FanCTRL-$(VERSION)/etc/systemd/system/
	
	cp -v $(SRC)/FanCTRL.py $(BUILD)/FanCTRL-$(VERSION)/usr/sbin/
	cp -v $(SRC)/FanCTRL.service $(BUILD)/FanCTRL-$(VERSION)/etc/systemd/system/

	dpkg-deb --build $(BUILD)/FanCTRL-$(VERSION)
	cp -v $(BUILD)/FanCTRL-$(VERSION).deb ./

install:
	echo "Installing Fan Driver"
	cp -v $(CONFIG)/FanConfig.json /etc
	cp -v $(SRC)/FanCTRL.py /usr/sbin/
	cp -v $(SRC)/FanCTRL.service /etc/systemd/system/
	echo "Files Copied"

	systemctl enable FanCTRL.service
	systemctl start FanCTRL.service
	echo "Done"

clean:
	rm -rv $(BUILD)
	rm -rv FanCTRL-$(VERSION).deb

all:
	deb