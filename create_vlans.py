
from jnpr.junos import Device
from jnpr.junos.utils.config import Config
import ipaddress

PLE_SW_LIST={"PLE01":{'IP':'10.254.3.102','HOS_USER_PORTS':['ae0','ae1'],'NFS_HOS_PORTS':['ae38','ae39','ae42','ae43','ae46','ae47'],'NFS_DMZ_PORTS':['ae38','ae39','ae42','ae43','ae46','ae47'],'DMZ_USER_PORTS':['ae2','ae3']},"PLE51":{'IP':'10.254.3.103','HOS_USER_PORTS':['ae0','ae1'],'NFS_HOS_PORTS':['ae38','ae39','ae42','ae43','ae46','ae47'],'NFS_DMZ_PORTS':['ae38','ae39','ae42','ae43','ae46','ae47'],'DMZ_PORTS':['ae2','ae3']},"PLE02":{'IP':'10.254.3.104','HOS_USER_PORTS':['ae12','ae13','ae14','ae15','ae16','ae17','ae18','ae19','ae20','ae21','ae22','ae23','ae24','ae25','ae26','ae27','ae28','ae29'],'NFS_HOS_PORTS':['ae30','ae31','ae32','ae33','ae34','ae35','ae','ae37','ae38','ae39','ae40','ae41','ae42','ae43','ae44','ae45','ae46','ae47'],'NFS_DMZ_PORTS':[],'DMZ_USER_PORTS':[]},"PLE52":{'IP':'10.254.3.105','HOS_USER_PORTS':['ae12','ae13','ae14','ae15','ae16','ae17','ae18','ae19','ae20','ae21','ae22','ae23','ae24','ae25','ae26','ae27','ae28','ae29'],'NFS_HOS_PORTS':['ae30','ae31','ae32','ae33','ae34','ae35','ae36','ae37','ae38','ae39','ae40','ae41','ae42','ae43','ae44','ae45','ae46','ae47'],'NFS_DMZ_PORTS':[],'DMZ_USER_PORTS':[]},"PLE03":{'IP':'10.254.3.106','HOS_USER_PORTS':[],'NFS_HOS_PORTS':[],'NFS_DMZ_PORTS':['ae28','ae29'],'DMZ_USER_PORTS':['ae24','ae25']},"PLE53":{'IP':'10.254.3.107','HOS_USER_PORTS':[],'NFS_HOS_PORTS':[],'NFS_DMZ_PORTS':['ae28','ae29'],'DMZ_USER_PORTS':['ae24','ae25']}}


"""

set security zones security-zone MONITORING host-inbound-traffic system-services ping
set security zones security-zone MONITORING host-inbound-traffic system-services ntp
set security zones security-zone MONITORING interfaces reth0.1704
set interfaces reth0 unit 1704 description "*** MONITORING ***"
set interfaces reth0 unit 1704 vlan-id 1704
set interfaces reth0 unit 1704 family inet address 172.21.176.1/26
set routing-instances CORE interface reth0.1704

"""


def create_zone_ifw(vlan_id,subnet,zone_name, int_desc=None, verbose=False):
	config=[]
	set_conf=''
	int_ip=ipaddress.ip_network(subnet).network_address+'/'+subnet.prefixlen
	config.append("set security zones security-zone " + zone_name + " host-inbound-traffic system-services ping")
	config.append("set security zones security-zone " + zone_name + " host-inbound-traffic system-services ntp")
	for host_int in FW_LIST['IFW']['HOS_USER_PORTS']:
		config.append("set security zones security-zone " + zone_name + " host-inbound-traffic interfaces " + host_int + "." + vlan_id)
	config.append("set interfaces " + host_int + " unit " + vlan_id  + " vlan-id " + vlan_id)
	if int_desc: config.append("set interfaces " + host_int + " unit " + vlan_id  + " description " + int_desc)
	config.append("set interfaces " + host_int + " unit " + vlan_id  + " family inet address " + int_ip)
	config.append("set routing-instances CORE interface " + host_int + "." + vlan_id)
	if verbose: print(config)
	for conf_line in config:
		set_conf+=conf_line+'\n'
	return set_conf

def create_user_hos_vlan_config(vlan_id,vlan_name):
	config={}
	set_conf={}
	for SW in PLE_SW_LIST.keys():
		if PLE_SW_LIST[SW]['HOS_USER_PORTS']:
			config[SW]=[]
			for INTERFACE in PLE_SW_LIST[SW]['HOS_USER_PORTS']:
				config[SW].append("set interfaces " + INTERFACE + " unit 0 family ethernet-switching vlan members " + vlan_name)
	for SW in config.keys():
		config[SW].append("set protocols evpn extended-vni-list " + vlan_id +"0")
		config[SW].append("set vlans " + vlan_name + " vlan-id " + vlan_id)
		config[SW].append("set vlans " + vlan_name + " vxlan vni " + vlan_id +"0")
		config[SW].append("set vlans " + vlan_name + " vxlan ingress-node-replication")
	for SW in config.keys():
		set_conf[SW]=''
		for config_line in config[SW]:
			set_conf[SW]+=config_line+'\n'
	return set_conf
	
def create_dmz_hos_vlan_config(vlan_id,vlan_name):
	config={}
	set_conf={}
	for SW in PLE_SW_LIST.keys():
		if PLE_SW_LIST[SW]['HOS_DMZ_PORTS']:
			config[SW]=[]
			for INTERFACE in PLE_SW_LIST[SW]['HOS_DMZ_PORTS']:
				config[SW].append("set interfaces " + INTERFACE + " unit 0 family ethernet-switching vlan members " + vlan_name)
	for SW in config.keys():
		config[SW].append("set protocols evpn extended-vni-list " + vlan_id +"0")
		config[SW].append("set vlans " + vlan_name + " vlan-id " + vlan_id)
		config[SW].append("set vlans " + vlan_name + " vxlan vni " + vlan_id +"0")
		config[SW].append("set vlans " + vlan_name + " vxlan ingress-node-replication")
	for SW in config.keys():
		set_conf[SW]=''
		for config_line in config[SW]:
			set_conf[SW]+=config_line+'\n'
	return set_conf
	
def create_nfs_hos_vlan_config(vlan_id,vlan_name):
	config={}
	for SW in PLE_SW_LIST.keys():
		if PLE_SW_LIST[SW]['NFS_HOS_PORTS']:
			config[SW]=[]
			for INTERFACE in PLE_SW_LIST[SW]['NFS_HOS_PORTS']:
				config[SW].append("set interfaces " + INTERFACE + " unit 0 family ethernet-switching vlan members " + vlan_name)
	for SW in config.keys():
		config[SW].append("set protocols evpn extended-vni-list " + vlan_id +"0")
		config[SW].append("set vlans " + vlan_name + " vlan-id " + vlan_id)
		config[SW].append("set vlans " + vlan_name + " vxlan vni " + vlan_id +"0")
		config[SW].append("set vlans " + vlan_name + " vxlan ingress-node-replication")
	set_conf={}
	for SW in config.keys():
		set_conf[SW]=''
		for config_line in config[SW]:
			set_conf[SW]+=config_line+'\n'
	return set_conf
	
def create_nfs_dmz_vlan_config(vlan_id,vlan_name):
	config={}
	for SW in PLE_SW_LIST.keys():
		if PLE_SW_LIST[SW]['NFS_DMZ_PORTS']:
			config[SW]=[]
			for INTERFACE in PLE_SW_LIST[SW]['NFS_DMZ_PORTS']:
				config[SW].append("set interfaces " + INTERFACE + " unit 0 family ethernet-switching vlan members " + vlan_name)
	for SW in config.keys():
		config[SW].append("set protocols evpn extended-vni-list " + vlan_id +"0")
		config[SW].append("set vlans " + vlan_name + " vlan-id " + vlan_id)
		config[SW].append("set vlans " + vlan_name + " vxlan vni " + vlan_id +"0")
		config[SW].append("set vlans " + vlan_name + " vxlan ingress-node-replication")
	set_conf={}
	for SW in config.keys():
		set_conf[SW]=''
		for config_line in config[SW]:
			set_conf[SW]+=config_line+'\n'
	return set_conf
	
def apply_config_to_sw(config,sw_name,verbose=False):	
	if verbose: print("Trying to connect to " + sw_name + " on IP " + PLE_SW_LIST[sw_name]['IP'])
	dev = Device(host=PLE_SW_LIST[sw_name]['IP'],user="jspace").open()
	if verbose: print("Connection opened to " + sw_name + " on IP " + PLE_SW_LIST[sw_name]['IP'])	
	if verbose: print("Trying to apply the following configuration: ")
	if verbose: print(config)	
	if verbose: print("Trying to open config mode")
	co=Config(dev, mode='private')  
	if verbose: print("Trying to load the config")
	co.load(config, format='set')
	if verbose: co.pdiff()
	co.commit()

def apply_config(config,verbose=False):
	for SW in PLE_SW_LIST.keys():
		if SW in config.keys():
			if verbose: print("Applying config on SW " + SW)
			apply_config_to_sw(config[SW],SW,verbose)

		
def create_new_zone(vlan_id,subnet,verbose=False):
	FW_SET_CONF = create_zone_ifw()
	for SW in PLE_SW_LIST.keys()
		if SW in config.keys()

