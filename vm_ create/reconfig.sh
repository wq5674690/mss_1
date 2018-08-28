#!/bin/bash
# 克隆服务器时初始配置,软链到所有的clone目录
# bash $0 hostname ipAddress old_ipAddress

d=$(date "+%Y%m%d%H%M%S")
hostname=$1
ip=$2
gw=${ip%.*}".254"
net=$(echo $ip | awk -F. '{print $3}')

chage -d `date +%Y-%m-%d` admin

# change DNS config
if [ $net -lt 100 ];then
    nameserver="192.168.30.175"
else
    if [ "$net" == "123" ];then
        nameserver="192.168.123.51"
    else
        nameserver="192.168.172.51"
    fi
fi
echo -e "nameserver ${nameserver}\nsearch baofoo.cn" > /etc/resolv.conf

# disabled ipv6
echo -e "alias net-pf-10 off\noptions ipv6 disable=1" > /etc/modprobe.d/disable-ipv6.conf 

# change ip address
sed -i.$d -e "s/IPADDR=.*/IPADDR=$ip/" -e "s/GATEWAY=.*/GATEWAY=$gw/" /etc/sysconfig/network-scripts/ifcfg-eth0
sed -i -e "s/ONBOOT.*/ONBOOT=no/" /etc/sysconfig/network-scripts/ifcfg-eth0.$d
/etc/init.d/network restart

# change hostname
sed -i.$d -e "s/HOSTNAME=.*/HOSTNAME=$hostname/" /etc/sysconfig/network

# change hosts
sed -i.$d -e "/::1/d" /etc/hosts
echo "$ip $hostname" >> /etc/hosts

# rm udev file
rm -rf /etc/udev/rules.d/70-persistent-net.rules

# init salt
if [ -d /etc/salt/pki ];then
	rm -rf /etc/salt/pki/*
fi
#sed -i "s/master:.*/master: 192.168.33.50/g" /etc/salt/minion
sed -i "s/id:.*/id: $ip/g" /etc/salt/minion

# binging gw mac
/etc/init.d/network restart
/etc/init.d/falcon restart
sleep 5
ping -c 1 -W 2 ${gw} > /dev/null
mac=$(grep ${gw} /proc/net/arp | awk '{print $4}')
echo ${gw} ${mac} > /etc/ip-mac
echo 'arp -f /etc/ip-mac' >>  /etc/rc.d/rc.local
sed -i '/begin.sh/d' /etc/rc.d/rc.local

# 配置 yum
rm -rf /etc/yum.repos.d/*
v=$(rpm -qa | grep release | grep -E "[0-9]Server" -o | sed 's/Server//' | sort | uniq | head -n1)
wget http://192.168.25.200/file/baofoo-linux-$v.repo -O /etc/yum.repos.d/baofoo-linux-$v.repo
yum clean all

# 更新软件包
yum -y install openssh-server openssl filebeat

# 更新 Filebeat 配置
case $3 in
    pre_stage)
        topic="pre_stage"
        ;;
    cbpay)
        topic="cbpay"
        ;;
    custody)
        topic="custody"
        ;;
    zx)
        topic="credit-zx"
        ;;
    *)
       topic="trade_log"
        ;;
esac

if [ "$topic" == "credit-zx" ];then
    hosts='["192.168.90.16:19092", "192.168.90.17:19092", "192.168.90.18:19092", "192.168.90.19:19092" ]'
else
    hosts='["192.168.190.64:9092", "192.168.190.65:9092", "192.168.190.66:9092", "192.168.190.67:9092" ]'
fi

cat << EOF > /etc/filebeat/filebeat.yml 
################### Filebeat Configuration Example #########################
#
############################# Output ##########################################
# Configure what outputs to use when sending the data collected by the beat.
# Multiple outputs may be used.
#
output.kafka:
  enabled: true
  hosts: $hosts 
  topic: "$topic"

############################# Filebeat ######################################
filebeat.prospectors:
    # App logs
    - input_type: log
      paths:
        - /data/log/*.log
        - /log/*/*.log
        - /log/*/*/*.log

      multiline.pattern: '^\[{0,1}\d{4}-\d{2}-\d{2}\s\d{2}:\d{2}:\d{2}[.,:]0?\d{3}'
      multiline.negate: true
      multiline.match: after
      document_type: $topic

#logging.level: debug
EOF

chkconfig filebeat on
/etc/init.d/filebeat start

# clear banner
echo "" > /etc/issue
echo "" > /etc/issue.net

# 修改 su 权限
sed -i 's/.*pam_wheel.so use_uid/auth           required        pam_wheel\.so use_uid/g'  /etc/pam.d/su
echo "auth   sufficient    /lib64/security/pam_rootok.so">>/etc/pam.d/su
echo "auth   required     /lib64/security/pam_wheel.so group=admin">>/etc/pam.d/su

# 修改系统参数
echo "TMOUT=1800">>/etc/profile
echo "umask 027">>/etc/profile

# 修改 SSH
echo "Ciphers aes128-ctr,aes192-ctr,aes256-ctr,aes128-cbc,3des-cbc,blowfish-cbc,cast128-cbc,aes192-cbc,aes256-cbc,rijndael-cbc@lysator.liu.se">>/etc/ssh/sshd_config
echo "PermitRootLogin no">>/etc/ssh/sshd_config


#add user
groupadd systemadmin

for i in {1..8};do
    useradd -g systemadmin systemadmin$i
    mkdir /home/systemadmin$i/.ssh
    touch /home/systemadmin$i/.ssh/authorized_keys
    chmod 700 /home/systemadmin$i/.ssh
    chmod 600 /home/systemadmin$i/.ssh/authorized_keys
    chown -R systemadmin$i:systemadmin /home/systemadmin$i
done

echo "%systemadmin ALL = NOPASSWD: ALL" >> /etc/sudoers

echo "ssh-rsa *** ***@web-101-11" >> /home/systemadmin3/.ssh/authorized_keys


reboot
