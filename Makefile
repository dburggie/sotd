
SOURCE_DIR = source
INCLUDE_DIR = include
DATA_DIR = data
BUILD_DIR = build

UNIT_DIR = /etc/systemd/service
BIN_INSTALL_DIR = /usr/bin
DAT_INSTALL_DIR = /usr/share/sotd

EXE = sotd
DAT = sotd.dat
TMR = sotd.timer
SRV = sotd.service

CFLG = -std=c++11 -Wall -ggdb -Llib
CINC = -I${INC}
COPT = ${CFLG} ${CINC}
CC   = g++ ${COPT}

all: ${BUILD_DIR}/${EXE}

install: ${BUILD_DIR}/${EXE}
	mkdir -p ${DAT_INSTALL_DIR}
	cp ${DATA_DIR}/${DAT} ${DATA_INSTALL_DIR}/
	cp ${BUILD_DIR}/${EXE} ${BIN_INSTALL_DIR}/
	cp ${SOURCE_DIR}/${SRV} ${UNIT_DIR}/
	cp ${SOURCE_DIR}/${TMR} ${UNIT_DIR}/
	systemctl enable ${TMR}
	systemctl start ${TMR}
	${EXE}

disable:
	systemctl disable ${TMR}

uninstall:
	rm --preserve-root -rf ${DATA_INSTALL_DIR}
	rm -f ${BIN_INSTALL_DIR}/${EXE}
	rm -f ${UNIT_DIR}/${SRV}
	rm -f ${UNIT_DIR}/${TMR}
	

