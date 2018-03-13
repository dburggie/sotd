
INSTALL_MACRO_NAME=DATA_PATH

# source directories
SD = source
ID = source
DD = data
BD = build

# install directories
UID = /etc/systemd/system
BID = /usr/bin
DID = /usr/share/sotd

# files to install
EXE = sotd
DAT = sotd.dat
TMR = sotd.timer
SRV = sotd.service

# header file
HDR = ${INC}/sotd.h

# object files to build
OBJ = ${BD}/Entry.o
OBJ += ${BD}/Work.o
OBJ += ${BD}/Data.o
OBJ += ${BD}/util.o
OBJ += ${BD}/main.o

# compiler and options
CDEF = -D${INSTALL_MACRO_NAME}="${DID}/${DAT}"
CFLG = -std=c++11 -Wall
CINC = -I${INC}
COPT = ${CFLG} ${CINC}
CC   = g++ ${COPT}



all: ${EXE}

install: ${EXE}
	mkdir -p ${DID}
	cp ${DD}/${DAT} ${DID}/
	cp ${EXE} ${BID}/
	cp ${SD}/${SRV} ${UID}/${SRV}
	cp ${SD}/${TMR} ${UID}/${TMR}
	systemctl enable ${TMR}
	systemctl start ${TMR}
	${EXE}

disable:
	systemctl disable ${TMR}
	systemctl stop ${TMR}

uninstall:
	rm -f ${DID}/${DAT}
	rm -f ${BID}/${EXE}
	rm -f ${UID}/${SRV}
	rm -f ${UID}/${TMR}
	rmdir ${DID}



# RECIPES

${BD}:
	mkdir -p $@

${BD}/${EXE}: ${BD} ${OBJ} ${HDR}
	${CC} -o $@ ${OBJ}


${BD}/Entry.o: ${SD}/Entry.cpp ${HDR}
	${CC} -o $@ -c $<

${BD}/Work.o: ${SD}/Work.cpp ${HDR}
	${CC} -o $@ -c $<

${BD}/Data.o: ${SD}/Data.cpp ${HDR}
	${CC} -o $@ -c $<

${BD}/util.o: ${SD}/util.cpp ${HDR}
	${CC} -o $@ -c $<

${BD}/main.o: ${SD}/main.cpp ${HDR}
	${CC} -o $@ -c $<

