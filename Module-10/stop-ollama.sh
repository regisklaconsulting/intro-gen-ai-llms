#!/bin/bash

# Add this script to our PATH as follows:
# Put the file in $HOME/bin/ollama
# $ vi .bashrc: 
# export PATH=$PATH:$HOME/bin/ollama
# $ source .bashrc

echo
echo "[INFO] ===================="
echo "[INFO] stop-ollama.sh"
echo "[INFO] ===================="
echo 

sudo docker stop ollama ; docker rm ollama

code=${?}
if [ ${code} == 0 ]; then
  echo "[INFO] Ollama container is correctly stopped. Bye!"
else 
  echo "[ERROR] Something wrong happened. Error code = ${code}. Abort!"
fi

exit ${code}

