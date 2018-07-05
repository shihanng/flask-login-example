#!/bin/bash
set -x
set -e

yum -y update
yum -y install https://centos7.iuscommunity.org/ius-release.rpm
yum -y install python36u python36u-pip python36u-devel nginx policycoreutils-python

cp /vagrant/simple_login.service /etc/systemd/system/simple_login.service
cp /vagrant/nginx.conf /etc/nginx/nginx.conf
cp /vagrant/simple_login /etc/sysconfig/simple_login

chmod 710 /simple_login
cd /simple_login && pip3.6 install .
usermod -a -G vagrant nginx

semanage permissive -a httpd_t

systemctl start simple_login && systemctl enable simple_login
systemctl start nginx && systemctl enable nginx
