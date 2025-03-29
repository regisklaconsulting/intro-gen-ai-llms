#!/bin/bash

# Add this script to our PATH as follows:
# Put the file in $HOME/bin/ollama
# $ vi .bashrc: 
# export PATH=$PATH:$HOME/bin/ollama
# $ source .bashrc

echo
echo "[INFO] ===================="
echo "[INFO] start-ollama.sh"
echo "[INFO] ===================="
echo 

if [ "$(docker ps -a|grep ollama)" != "" ]; then 
  echo "[WARN] Ollama is running or not correctly stopped. Stoping it..."
  sudo docker stop ollama ; docker rm ollama
  echo "[INFO] Done."
fi

sudo docker run -d \
  -v /home/ml/ollama:/root/.ollama \
  -v /home/ml/pretrained-models/llms:/root/llms \
  -v /home/ml/pretrained-models/llms/ollama-modelfiles:/root/ollama-modelfiles \
  -p 11434:11434 --name ollama ollama/ollama

code=${?}
if [ ${code} == 0 ]; then
  echo "[INFO] Ollama container is correctly started in background. Bye!"
else 
  echo "[ERROR] Something wrong happened. Error code = ${code}. Abort!"
fi

exit ${code}

