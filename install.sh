#!/usr/bin/env bash
USER=BotLastPost
apt install  python3-venv -y
apt install python3-pip -y
python3 -m pip install --upgrade pip
useradd -m $USER
cd /home/$USER/ || exit
git clone https://github.com/asannasa/BotLastPost.git
cd /home/$USER/BotLastPost/ || exit
python3 -m venv venv
source "$PWD"/venv/bin/activate
"$PWD"/venv/bin/pip install -r requirements.txt
deactivate

clear
TOKEN=$(whiptail --title  "Настройка бота последнего сообщения" --inputbox  "Введите токен:" 10 60 3>&1 1>&2 2>&3)
exitstatus=$?
if [ $exitstatus = 0 ];  then
     echo "TOKEN=$TOKEN" > .env
else
     echo "Отмена"
fi

TIME=$(whiptail --title  "Настройка бота последнего сообщения" --inputbox  "Введите интервал сообщений (секунды):" 10 60 3>&1 1>&2 2>&3)
exitstatus=$?
if [ $exitstatus = 0 ];  then
     echo "TIME=$TIME" >> .env
else
     echo "Отмена"
fi

ADMIN=$(whiptail --title  "Настройка бота последнего сообщения" --inputbox  "Введите ИД админа или админов через запятую:" 10 60 3>&1 1>&2 2>&3)
exitstatus=$?
if [ $exitstatus = 0 ];  then
     echo "ADMIN=$ADMIN" >> .env
else
     echo "Отмена"
fi

cp BotLastPost.service /etc/systemd/system
chown -R $USER:$USER /home/$USER/$USER/
systemctl enable BotLastPost.service
systemctl start BotLastPost.service
