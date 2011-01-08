#!/bin/sh

for program in add/Add max/Max rect/Rect pong/Pong; do
    echo ${program}
    ./Assembler.py ${program}.asm > ${program}.hack.out
    diff ${program}.hack ${program}.hack.out
done
