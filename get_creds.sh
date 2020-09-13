#!/bin/bash
HOST=$1
wget -qO- $1'/system.ini?loginuse&loginpas' | strings
