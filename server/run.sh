#!/bin/bash

pkill server.py
./server.py > log.txt 2>&1 &
