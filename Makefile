
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
HDR = ${ID}/sotd.h

# object files to build
OBJ = ${BD}/Entry.o
OBJ += ${BD}/Work.o
OBJ += ${BD}/Data.o
OBJ += ${BD}/util.o
OBJ += ${BD}/main.o

INSTALL_MACRO_NAME=DATA_PATH
INSTALL_MACRO_FALLBACK=DATA_FALLBACK

# compiler and options
CDEF = -D${INSTALL_MACRO_NAME}=\"${DID}/${DAT}\"
CDEF += -D${INSTALL_MACRO_FALLBACK}=\"./${DD}/${DAT}\"
CFLG = -std=c++11 -Wall
CINC = -I${ID}
COPT = ${CFLG} ${CINC} ${CDEF}
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
	${EXE} > /etc/motd

disable:
	systemctl disable ${TMR}
	systemctl stop ${TMR}

uninstall:
	rm --preserve-root -rf ${DID}
	rm -f ${BID}/${EXE}
	rm -f ${UID}/${SRV}
	rm -f ${UID}/${TMR}

clean:
	rm -f ${OBJ}
	rm -f ${EXE}


# RECIPES

${BD}:
	mkdir -p $@

${EXE}: ${BD} ${OBJ} ${HDR}
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

