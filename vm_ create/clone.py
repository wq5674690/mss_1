# -*- coding: UTF-8 -*-
import time
import ssl
import os
import re
import sys
import atexit
from collections import Iterable
import requests

from pyVim import connect
from pyVmomi import vim, vmodl

PROJECT_ROOT = os.path.realpath(os.path.join(os.path.dirname(__file__)))
sys.path.insert(0, PROJECT_ROOT)


import setting


def WaitTask(task, vm_name, actionName='job', hideResult=False):
    while task.info.state == vim.TaskInfo.State.running:
        print('服务器 %s 任务进行中... [%s]' % (vm_name, task.info.state))
        time.sleep(2)

    if task.info.state == vim.TaskInfo.State.success:
        return '已完成'
    else:
        return task.info.error


class VmwareApi:
    def __init__(self, **kwargs):
        self.host = kwargs.get('host')
        self.user = kwargs.get('user')
        self.password = kwargs.get('password')
        self.port = kwargs.get('port', 443)
        self.content = self.login()
        if not self.content:
            return

    def login(self):
        try:
            context = ssl.SSLContext(ssl.PROTOCOL_TLSv1)
            context.verify_mode = ssl.CERT_NONE
            service_instance = connect.SmartConnect(host=self.host,
                                                    user=self.user,
                                                    pwd=self.password,
                                                    port=self.port,
                                                    sslContext=context
            )

            atexit.register(connect.Disconnect, service_instance)

            content = service_instance.RetrieveContent()
            return content
        except vmodl.MethodFault as error:
            print("Caught vmodl fault : " + error.msg)
            return

    def get_obj(self, vimtype, name):
        obj = None
        container = self.content.viewManager.CreateContainerView(self.content.rootFolder, vimtype, True)
        for view in container.view:
            if view.name == name:
                obj = view
                break
        return obj

    def get_vm(self, name):
        return self.get_obj([vim.VirtualMachine], name)

    def get_network(self, name, is_VDS=False):
        if is_VDS:
            return self.get_obj([vim.dvs.DistributedVirtualPortgroup],name)
        else:
            return self.get_obj([vim.Network], name)

    def clone(self, temp_name, cloned_name):
        try:
            template_vm = self.get_vm(temp_name)
            relocateSpec = vim.vm.RelocateSpec()
            cloneSpec = vim.vm.CloneSpec(powerOn=True, template=False, location=relocateSpec)
            task = template_vm.Clone(name=cloned_name, folder=template_vm.parent, spec=cloneSpec)
            result = WaitTask(task, cloned_name)
            return result
        except Exception as e:
            print(e)
            return str(e)
			
    def upload_file(self, vm_name, vm_user, vm_pwd, source_file, des_file):
        vm = self.get_vm(vm_name)
        creds = vim.vm.guest.NamePasswordAuthentication(username=vm_user, password=vm_pwd)
        
        with open(source_file, 'rb') as f:
            args = f.read()
        
        try:
            file_attribute = vim.vm.guest.FileManager.FileAttributes()
            url = self.content.guestOperationsManager.fileManager.InitiateFileTransferToGuest(
                vm, creds, des_file, file_attribute,len(args), True)
            resp = requests.put(url, data=args, verify=False)  # resp.status_code == 200
            return resp.status_code
        except Exception as err:
            return err.msg
            
    def process(self, vm_name, vm_user, vm_pwd, executable_program, arguments):
        vm = self.get_vm(vm_name)
        creds = vim.vm.guest.NamePasswordAuthentication(username=vm_user, password=vm_pwd)
        
        try:
            pm = self.content.guestOperationsManager.processManager

            ps = vim.vm.guest.ProcessManager.ProgramSpec(
                programPath=executable_program,
                arguments=arguments,
            )
            res = pm.StartProgramInGuest(vm, creds, ps)

            if res > 0:
                return True

        except IOError as err:
            print(err)

    def change_network(self, vm_name, vlan_name, is_VDS=True):
        vm = self.get_vm(vm_name)
        vlan = self.get_network(vlan_name, is_VDS)
        virtual_nic_device = None

        if not (vm and vlan):
            return

        for dev in vm.config.hardware.device:
            if isinstance(dev, vim.vm.device.VirtualEthernetCard):
                virtual_nic_device = dev

        if not virtual_nic_device:
            return

        virtual_nic_spec = vim.vm.device.VirtualDeviceSpec()
        virtual_nic_spec.operation = vim.vm.device.VirtualDeviceSpec.Operation.edit
        virtual_nic_spec.device = virtual_nic_device
        virtual_nic_spec.device.wakeOnLanEnabled = virtual_nic_device.wakeOnLanEnabled

        if not is_VDS:
            virtual_nic_spec.device.backing = vim.vm.device.VirtualEthernetCard.NetworkBackingInfo()
            virtual_nic_spec.device.backing.network = vlan
            virtual_nic_spec.device.backing.deviceName = vlan_name
        else:
            dvs_port_connection = vim.dvs.PortConnection()
            dvs_port_connection.portgroupKey = vlan.key
            dvs_port_connection.switchUuid = vlan.config.distributedVirtualSwitch.uuid
            
            virtual_nic_spec.device.backing = vim.vm.device.VirtualEthernetCard.DistributedVirtualPortBackingInfo()
            virtual_nic_spec.device.backing.port = dvs_port_connection

        virtual_nic_spec.device.connectable =  vim.vm.device.VirtualDevice.ConnectInfo()
        virtual_nic_spec.device.connectable.startConnected = True
        virtual_nic_spec.device.connectable.allowGuestControl = True
        virtual_nic_spec.device.connectable.connected = True

        device_changes = [virtual_nic_spec]
        config_spec = vim.vm.ConfigSpec(deviceChange=device_changes)
        task = vm.ReconfigVM_Task(config_spec)
        result = WaitTask(task, vm_name)
        return result


def create_server_list(description_vm_begin, ip_range):

    only_ip_regx = '(?:25[0-5]\.|2[0-4]\d\.|[01]?\d\d?\.){3}(?:25[0-5]|2[0-4]\d|[01]?\d\d?)$'
    ip_range_regx = '(?:25[0-5]\.|2[0-4]\d\.|[01]?\d\d?\.){3}(?:25[0-5]|2[0-4]\d|[01]?\d\d?)-(?:25[0-5]|2[0-4]\d|[01]?\d\d?)$'
    
    only_ip_regx_com = re.compile(only_ip_regx)
    ip_range_regx_com = re.compile(ip_range_regx) 

    vm_list = []

    if only_ip_regx_com.match(ip_range):
        name = description_vm_begin + "-"+ "-".join(ip_range.split(".")[2:])
        vm_list.append({
            "ip": ip_range,
            "vm_name": name,
            "hostname": name,
            "vlan": ip_range.split(".")[2]
        })
    elif ip_range_regx_com.match(ip_range):
        ip_begin = ".".join(ip_range.split(".")[:3])
        ip_net = ip_range.split(".")[2]
        begin, end = [int(x) for x in ip_range.split(".")[-1].split("-")]
        if begin <= end:
            for n in range(begin, end+1):
                name = "%s-%s-%d" % (description_vm_begin, ip_net, n)
                vm_list.append({
                    "ip": "%s.%d" % (ip_begin, n),
                    "vm_name": name,
                    "hostname": name,
                    "vlan": ip_range.split(".")[2]
                })
    else:
        return False

    return vm_list

        
def main():
    help = """
        执行方法： python %s template_name ip_range topic
            template_name: 模版主机名称, 如为 config, 则是仅重新配置已开机的虚拟机,不克隆
            ip_range: 可以为单独的 IP 地址,也可以为 IP 范围: 192.168.1.1-10
            topic: 默认将日志写入的 topic 
                  资管:      topic=custody        index=custody
                  支付:      topic=trade_log      index=applog
                  跨境:      topic=cbpay          index=cbpay
                  准生产:    topic=pre_stage      index=pre_stage
                  征信:      topic=credit-zx      index=credit-zx
    """ % sys.argv[0]

    try:
        template_vm = sys.argv[1]
        ip_range = sys.argv[2]
        topic = sys.argv[3]
    except Exception as e:
        print(help)
        return

    vm_list = create_server_list(setting.destination_vm_begin, ip_range)

    if not vm_list:
        print(help)
        return

    vc = VmwareApi(host=setting.vc_host, user=setting.vc_user, password=setting.vc_password)

    for vm_info in vm_list:
        print("服务器 %s 开始克隆..." % vm_info["vm_name"])
        if template_vm == "config":
            task1 = "已完成"
        else:
            task1 = vc.clone(template_vm, vm_info["vm_name"])
        vm_info["task_status"] = task1
        if task1 == "已完成":
            print("服务器 %s 已经创建完成，请等待服务器开机..." % vm_info["vm_name"])

    time.sleep(30)

    for vm_info in vm_list:    
        if vm_info["task_status"] == "已完成":

            vlan_name = setting.vlan_begin + vm_info["vlan"]
            vm_name = vm_info.get("vm_name")

            print("服务器 %s 开始配置网络..." % vm_name)
            change_network_status = vc.change_network(vm_name, vlan_name)
            if change_network_status == "已完成":
                print("服务器 %s 的网络已经规划至 %s" % (vm_name, vlan_name))
            else:
                print("服务器 %s 网络配置出错，请检查脚本: %s" % (vm_name, change_network_status))

            print("服务器 %s 已经开机，开始上传文件并执行..." % vm_name)
            upload_file_code = vc.upload_file(vm_name, setting.vm_user, setting.vm_pwd, setting.source_file, setting.des_file)
            if upload_file_code == 200:
                arguments = "/tmp/reconfig.sh %s %s %s" % (vm_info["hostname"], vm_info["ip"], topic)
                process_status = vc.process(vm_info["hostname"], setting.vm_user, setting.vm_pwd, setting.executable_program, arguments)
                if process_status:
                    print("服务器 %s 开始重启，请稍等一分钟后使用新的 IP 地址 [%s] 尝试登录" % (vm_name, vm_info["ip"]))
                else:
                    print("服务器 %s 脚本执行出错，请检查脚本: %s" % (vm_name, process_status))
            else:
                print("服务器 %s 文件上传失败: %s" % (vm_name, upload_file_code))
        else:
            print(vm_info.get("vm_name"), vm_info["task_status"])
            

if __name__ == "__main__":
    main()
