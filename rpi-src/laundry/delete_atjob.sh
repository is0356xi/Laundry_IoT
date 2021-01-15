#!/bin/sh

at -l | while read a b;do atrm $a;done