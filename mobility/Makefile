SDK ?= /home/mouse/SW/android-sdk-linux_x86

all: eVote-debug.apk

eVote-debug.apk: .zxing-unpacked
	cd $(CURDIR)/zxing/core; \
	    ant -lib $(SDK)/tools/lib \
	        -Dandroid-home=$(SDK) -Dno-optimize=true; \
	for d in android androidtest; do \
	    cd $(CURDIR)/zxing/$$d; \
	    ant debug -lib $(SDK)/tools/lib \
	        -Dandroid-home=$(SDK) -Dno-optimize=true; \
	done
	cp -f zxing/androidtest/bin/$@ $@

.zxing-unpacked: ZXing-1.7.zip
	unzip ZXing-1.7.zip
	rsync -aq androidtest/ zxing/androidtest/
	touch .zxing-unpacked

ZXing-1.7.zip:
	wget -c -O $@ http://zxing.googlecode.com/files/ZXing-1.7.zip

clean:
	rm -rf zxing .zxing-unpacked

.PHONY: clean
