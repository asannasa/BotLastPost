#!/usr/bin/env bash
systemctl stop BotLastPost.service
systemctl disable BotLastPost.service
deluser --remove-all-files BotLastPost
rm /etc/systemd/system/BotLastPost.service
