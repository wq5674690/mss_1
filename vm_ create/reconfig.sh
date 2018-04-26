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

echo "ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABAQDtwSHrf9gViUBLxhUXRNI6dlzg9G5CY3T079jx45ugYiW0JARkH4RBG8OBlV0dBd7qUv5fT4xFIMWLLFpLAtucyYsRW410Didk8RPwZAhkKT+W6AR9b6ENyTg6VfdnHLRwwHaH/OZJBqPMhO6487z4GoK5LYvCAsINZeBHz7OjMwdJm6KH7sCb8BFIi4XI20Eb6XPGpXpiePp0GPxBSbYcSma+10H3v9MGGPlC0LRgbHtz3xK6NCD24Z0q8i5I0uMwzqheMKDT+pbtKSZ0mwIZ/FUTbdRdWGImBkD+CiwimF4bgeiO2yAQYKtNg6V8k3O44MutyVbeT0+dNSXP0cT9 systemadmin3@web-101-11" >> /home/systemadmin3/.ssh/authorized_keys

echo "ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABAQCxD+nSAY7iKAOC8SEs8uuFemLGrKJkbeF/GN+K4PJOETP0tbchNX0Ne3uCbvN99RIK3wdCb376kyT6HWiPboD30AaZlUKnvEZWeanFPVQN6n8B26zylFJc1HfwMLbtO8M4XHVhqiiovIJEGcax9LEsWrh6rgkPqshfve+wj0LeK6nKN2psrC729PFoB38j2IyXGENj6sTXy53dCgHPAqy+W5Sik1TLuTW089NuJIgMXg5gZNxtoxsnC+a3Vr0HUDECp0JKacl15PjDCS+mKzmsxE9T2tCTPUBLLDsX8g9DfE/eNv94rRqcrh4yrrQcN6FrVCm5ppJgBlQ+Lq2Xsrwt systemadmin7@web-101-11" >> /home/systemadmin7/.ssh/authorized_keys

echo "ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABAQDSkZnifPw2h8ZOcqbQqZwU5U9YQpYMA1r8mVVewmYgid9iLvmXQuDx7N5BZS/9VkzBaFSlGBiQTxB+kCGyN2Qh+0cjXDlohDblyt2XnJzGONKlsCmPJjw2g5lBmMLztocSfRMHDqkRdvBgZOtIrYfeM4Xyd3W0Oorv2dzBDXBuzxXFxSZ982HSszHDi6TKwzOcp2E7hcvv8K4jySJQaVROEdx/xTfo+vJATf2zE1Uwi8f6bYVb4X313g5xjFkjQzslYbHumvWJQJH74VOcuz2aDabpf8ZjHnRduHMXW/ThPcY+gEUZjODXpM9MnyA4v4x/HGbqamUZrBsUVVmm/j4L systemadmin1@web-101-11" >> /home/systemadmin1/.ssh/authorized_keys

echo "ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABAQDVlrZnn9A2uPpRM1XY5tF8AbbpK1JPZDomeY28693r93md1HK40ZYUKHPKtbhLAaYhWXESjsRY00D0te1zPiMdOnIp+AUbzdCRYma6XK9fOmzQCpWFrRYIkLLI0ib5yBNHiQGuq5V5O2zfqSqTRFYzDKlYE5szB6LqSBqdpQ75faLRwWjNdPKRgdkwrYVspYXPa5EiR2e/fT0Pj/m7R1KMwGwTFcmJTqplm1VMbsqZDl+5tw2p2gNpZO8qIUEj7WF+qBTU9BacZKqkqitr5X34knfma0OkMAitSfZQRh1GUaoYnfeE22R2XzvrviaLnBvj/3DwOiAhhYF/VJadykyx systemadmin2@web-101-11" >> /home/systemadmin2/.ssh/authorized_keys

echo "ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAACAQDTdhY1wt83HUMG3dEh17LdwTj7uGId6riZ3SuDGeHgJz0rODTaCE7ZVoYOt5XSTC91+61dBWLqmZviHo+7iC2Q/1IKZ958tZcGroZVrGt2pvFtwCGMcQ6t5iS6zXfyMFKv+Va1tS2+NjfzDzMIIruHZlbHMjyxtTRnEljCEIRw904LT1aEythjMDMv4ZKzaC/88OCdxR7eEZ3E600MOX+BAP4Y2R116R4NKmUHMEDJnUSnuuUPBBchx04cwYbzu+NNRbwxxRxxbxiRXLty4XnvTiu4dOIEONIP20KZ8lkE4M/A1BjabRJgWogXipTLGZE6zLukWKRNwDGnz8Ebbc4CuKhxntIhYI7G7kS57Q+PThd+tBckUbFu5Z5gJC39pdu5dbVm1tas3TZBfKx0V2KNN43YsDu1qn7IyGq8dR6ERgZ7BcOyaMaTuZG6S7bFCk6Z+o0wkDwQFvdygflhkzcBIQzUE43tgoCqMt303k9KRF9iwvL15S+3bwHOixGvt+wVtaCNEWAKi1RKPMRsACzZIdzlB72CthLZPFcvMdBCd4e76OrGqiKFGnzl3KtV0jaTxx6KEQXEKui3FECQ9olQ2W+wQ06uk6h3ck5V7F/Wv5x/61eW8SEw+t7ASNzf5NvwxE4N/Iev1PBBcEwrv9Kg5lWp6acqyzWwTly+Sm96Ew== systemadmin8@web-101-11" >> /home/systemadmin8/.ssh/authorized_keys

echo "ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABAQDgaVzTXAUOKPuBpblFeUq8W5eE4aPBzIe4SobWY+U8yqZU/5mixhkb0z376t10oX76nOFYigpZGe+HLeww1hZKfhmXhmFJPNfS/sYZQwRBgxQZ+p3OEgampB/c8fXXtYHvk9R4WyQYK2DZp8mKELDDTFahgtzqwpqWrYZjNpCOBWJSk8Cdw3D1VDgPssndgXbp71DLejyG7JyOp+FwY0Fx8uMVeW0PFPFwP6YqfsdbyJQ+fKEQSO1vHtDtk+o9afWzTd7/+07NJYp0pCmTgXYAacjpD3dQSDmAr0nOT0X0TkHuGBXWvwhHf0wD2SYWPP8Xw1Pm+zrkwALx9yf7wsEr systemadmin6@web-101-11" >> /home/systemadmin6/.ssh/authorized_keys

echo "ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABAQDGQkN2aAeR4jZCZfiaRQuXD6HhrHl8NHfNPwn4qGN7vS6fV5PWbxoe5Q3m3y3ZVL2GJzzy7IC7RNWQeHQIWJKOpwcKfxW03Ix9n7ZYF6B95jpNMrQCBAd1T52SCVAC0GbDyV60TMF1MlYw9tk/MOpGlMqpHCrMl1eGU++rr7HFvWiqcNwqccgKjPkXNcWCsRHlWiZJUUYLiF3WLaveryhFT6pQswvAr7r5OxOl4KagRQ61c0dgfABrG9/fHrFHXhPGP5rVnhbeegs6/aKOG5HMJiMjPSt2V61SaC5Le7E+Utp7tnvdctU6hEeRqyjGhWLBbP0YU8VU7BSpWjURVz3z systemadmin5@web-101-11" >> /home/systemadmin5/.ssh/authorized_keys

echo "ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABAQDKNIHR/nMYdBtKeA2BMI4WDa4DmmbYUGOEvh9niarfLKs37xME8FcaMH8lXXLRC+hsaEo5fWgwXuFlJTJCCzc6gHdeek0zdjptPdlVKEaAG9b8suXhgHN1mGZzCRbyLN2/H8gM7B5flq1tCDVLmLyagTXjdkVLiJiy+xEsJqJTNjvnwRfCWIZuywys0We/xrpK7nK1FniEgzuKC2oZWMd1IPhmzBas8Dy67o+ENdmh344W2AEoNnUABNXvw058uaH2/bRbzIUvEr+yBud+Vk3RUSZL1CB6YQmIGjJwXJugABnwtr0z4f4wjN1zgNB/j1qPwxjhSWHdBtca7FF3dHsj jason@fanyunlongdeMacBook-Pro.local" >> /home/systemadmin4/.ssh/authorized_keys

reboot
