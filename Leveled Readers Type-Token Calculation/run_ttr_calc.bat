#!/bin/bash
# open fd=3 redirecting to 1 (stdout)
#exec 3>&1

echo exec 3>&1 1>>"TTR_Calc_Log_20180522.txt" 2>&1
# redirect stdout/stderr to a file but show stderr on terminal
#exec >file.log 2> >(tee >(cat >&3))
# function echo to show echo output on terminal

echo() {
   # call actual echo command and redirect output to fd=3
   command echo "$@" >&3
}
# script starts here
#exec 3>&1 1>>"TTR_Calc_Log_20180522.txt" 2>&1

cd "C:\Dropbox\Berkeley MIDS\MIDS+\Type-Token Analysis" | tee "TTR_Calc_Log_20180522.txt"
python "C:/Dropbox/TSlade Stata/Kenya Tusome/gitrepos/non-STATA/Leveled Readers Type-Token Calculation/Type-Token Calculator.py" | tee "TTR_Calc_Log_20180522.txt"
FOR %%A in ("C:/Dropbox/Berkeley MIDS/MIDS+/Type-Token Analysis/submissions/abantu" "C:/Dropbox/Berkeley MIDS/MIDS+/Type-Token Analysis/submissions/cambridge" "C:/Dropbox/Berkeley MIDS/MIDS+/Type-Token Analysis/submissions/evangel" "C:/Dropbox/Berkeley MIDS/MIDS+/Type-Token Analysis/submissions/focus" "C:/Dropbox/Berkeley MIDS/MIDS+/Type-Token Analysis/submissions/herald" "C:/Dropbox/Berkeley MIDS/MIDS+/Type-Token Analysis/submissions/klb" "C:/Dropbox/Berkeley MIDS/MIDS+/Type-Token Analysis/submissions/longhorn" "C:/Dropbox/Berkeley MIDS/MIDS+/Type-Token Analysis/submissions/moran" "C:/Dropbox/Berkeley MIDS/MIDS+/Type-Token Analysis/submissions/mountaintop" "C:/Dropbox/Berkeley MIDS/MIDS+/Type-Token Analysis/submissions/oneplanet" "C:/Dropbox/Berkeley MIDS/MIDS+/Type-Token Analysis/submissions/oxford" "C:/Dropbox/Berkeley MIDS/MIDS+/Type-Token Analysis/submissions/phoenix" "C:/Dropbox/Berkeley MIDS/MIDS+/Type-Token Analysis/submissions/queenex" "C:/Dropbox/Berkeley MIDS/MIDS+/Type-Token Analysis/submissions/scholastic" "C:/Dropbox/Berkeley MIDS/MIDS+/Type-Token Analysis/submissions/spear_sharp" "C:/Dropbox/Berkeley MIDS/MIDS+/Type-Token Analysis/submissions/storymoja" "C:/Dropbox/Berkeley MIDS/MIDS+/Type-Token Analysis/submissions/wordalive") DO [
ECHO a
ECHO p
ECHO %%A
ECHO .txt
ECHO c
ECHO c
]
ECHO f
ECHO a
ECHO a





