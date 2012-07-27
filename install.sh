#!/bin/bash

echo "Copying executable to /usr/bin/    (requires root access) "

#TODO: support older versions, add a choice here

sudo cp funfind_2_7.py /usr/bin/funfind
if [ $? -eq 0 ];
then
    exit
fi

sudo chmod 755 /usr/bin/funfind

echo "Would you like to add some helpful function wrappers to your .bashrc? [Y/N]"
read -e ADDBASH

if [ $ADDBASH == "Y" -o $ADDBASH == "y" ]; 
then
    cat src/bashrc_functions.sh >> ~/.bashrc
    echo ""
    echo "NOTICE: You will have to reload your .bashrc for this to take effect" 
    echo ""
fi

echo    ""
echo    "==================================="
echo    "THANK YOU FOR INSTALLING FUN FINDER"
echo    "==================================="
echo    ""
