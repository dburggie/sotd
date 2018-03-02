
SRC = source
INC = include
BLD = build

CFLG = -std=c++11 -Wall -ggdb -Llib
CINC = -I${INC}
COPT = ${CFLG} ${CINC}
CC   = g++ ${COPT}

EDIR = /usr/local/bin
EXE = sotd
