echo -e "\033[34m--------------- uwsgi process ---------------\033[0m"
ps -ef | grep uwsgi_mycgut.ini | grep -v grep
sleep 0.5
echo -e "\n--------------- going to close ---------------"
ps -ef | grep uwsgi_mycgut.ini | grep -v grep | awk '{print $2}' | xargs kill -9
sleep 0.5
echo -e "\n--------------- check if the kill action is correct ---------------"