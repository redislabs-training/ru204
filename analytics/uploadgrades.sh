#!/bin/bash

if [ ! -f "./grade_loader.sh" ]; then
   echo "This script must be run from the the analytics directory containing grade_loader.sh!"
   exit 1
fi

if [[ -z "${GRADE_LOADER_TMP}" ]]; then
  echo "You must set the GRADE_LOADER_TMP environment variable!"
  exit 1
fi

if [[ -z "${GRADE_LOADER_DOWNLOAD}" ]]; then
  echo "You must set the GRADE_LOADER_DOWNLOAD environment variable!"
  exit 1
fi

if [[ -z "${GRADE_LOADER_PASSWORD}" ]]; then
  echo "You must set the GRADE_LOADER_PASSWORD environment variable!"
  exit 1
fi

rm -f ~/grades/*.csv
ls -tr ${GRADE_LOADER_DOWNLOAD}/*grade_report*.csv | tail -7 | xargs -I{} cp {} ${GRADE_LOADER_TMP}
sh ./grade_loader.sh ${GRADE_LOADER_PASSWORD} ${GRADE_LOADER_TMP}
