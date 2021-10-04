#!/bin/bash
cd $(dirname $0)
echo "Starting MCEdit..."
f=
if [ -f "GDMC/mcedit.py" ]
then
    f="mcedit.py"
elif [ -f "GDMC/mcedit.pyc" ]
then
    f="GDMC/mcedit.pyc"
elif [ -f "GDCM/mcedit" ]
then
    f="mcedit"
else
    echo "MCEdit program not found."
    echo "Check your installation and retry."
    exit 1
fi
cd GDMC/
python2 $f "${@}"
read -n 1 -p "Press any key to close."
echo ""
