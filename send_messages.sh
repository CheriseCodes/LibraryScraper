#!/bin/bash
WORK_DIR=${HOME}/Desktop/Code/Projects/LibraryScraper
source ${WORK_DIR}/env/bin/activate
${WORK_DIR}/env/bin/python ${WORK_DIR}/src/libscrape/main.py
deactivate