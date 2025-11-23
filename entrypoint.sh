#!/bin/sh

#above is a shebang -> tells the system "Run the script using sh interpreter"

if [$# -lt 2]; then #if fewer than 2 arguments are provided then do the following: 
    echo "Usage: entrypoint.sh <input-file> <output-file>" #informs user how to run the script (debugging)
    exit 1

fi 

python /app/metadata_parser.py "$1" "$2" #the 1 and 2 represent the arguments the first one is input and the other is output

#References: 
#https://www.datacamp.com/tutorial/docker-entrypoint
