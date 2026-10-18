echo "Starting script..."
while true; do python3 -u ~/twsium/twsium.sh 2>&1 | tee -a ~/.config/latest.log sleep 2; done
