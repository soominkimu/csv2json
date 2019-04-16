#!/bin/zsh

CBLACK='\e[30m'
RED='\e[0;31m'
GREEN='\e[0;32m'
BLUE='\e[0;34m'
YELLOW='\e[0;33m'
CREDBG='\e[41m'
CGREENBG='\e[42m'
CYELLOWBG='\e[43m'
CWHITEBG='\e[47m'
NC='\e[0m'
DATE=`date +"Date : %a %m/%d/%Y"`
TIME=`date +"Time : %H.%M.%S"`
print "${YELLOW}${DATE} ${GREEN}${TIME}${NC}"

PGMS=(
  "weather_jma.py"
  "merge_json.py"
)

run_python() {
  print "${BLUE}===============================================================${NC}"
  print "${GREEN}python ${YELLOW}${PGM}${NC}"
  python ${PGM}
}

for p in "${PGMS[@]}"; do
  PGM=$p
  run_python
done
