#!/bin/bash
serviceName="parser.service"
cat <<EOF > /etc/systemd/system/$serviceName
[Unit]
Description=kinescope parser

[Service]
ExecStart=/home/dotsenkois/main.py

[Install]
WantedBy=multi-user.target

EOF

systemctl deamon-reload && systemctl enable $serviceName && systemctl start $serviceName && systemctl status $serviceName