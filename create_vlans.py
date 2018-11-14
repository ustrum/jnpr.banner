
from jnpr.junos import Device
from jnpr.junos.utils.config import Config

VLAN_ID = '1251'
VLAN_NAME = 'CUS_HOS_TEST'



PLE_SW_LIST={"PLE01":{'IP':'10.254.3.110','HOS_USER_PORTS':['ae0','ae1'],'NFS_HOS_PORTS':['ae38','ae39','ae42','ae43','ae46','ae47'],'NFS_DMZ_PORTS':['ae38','ae39','ae42','ae43','ae46','ae47'],'DMZ_USER_PORTS':['ae2','ae3']},"PLE51":{'IP':'10.254.3.111','HOS_USER_PORTS':['ae0','ae1'],'NFS_HOS_PORTS':['ae38','ae39','ae42','ae43','ae46','ae47'],'NFS_DMZ_PORTS':['ae38','ae39','ae42','ae43','ae46','ae47'],'DMZ_PORTS':['ae2','ae3']},"PLE02":{'IP':'10.254.3.112','HOS_USER_PORTS':['ae12','ae13','ae14','ae15','ae16','ae17','ae18','ae19','ae20','ae21','ae22','ae23','ae24','ae25','ae26','ae27','ae28','ae29'],'NFS_HOS_PORTS':['ae30','ae31','ae32','ae33','ae34','ae35','ae','ae37','ae38','ae39','ae40','ae41','ae42','ae43','ae44','ae45','ae46','ae47'],'NFS_DMZ_PORTS':[],'DMZ_USER_PORTS':[]},"PLE52":{'IP':'10.254.3.113','HOS_USER_PORTS':['ae12','ae13','ae14','ae15','ae16','ae17','ae18','ae19','ae20','ae21','ae22','ae23','ae24','ae25','ae26','ae27','ae28','ae29'],'NFS_HOS_PORTS':['ae30','ae31','ae32','ae33','ae34','ae35','ae36','ae37','ae38','ae39','ae40','ae41','ae42','ae43','ae44','ae45','ae46','ae47'],'NFS_DMZ_PORTS':[],'DMZ_USER_PORTS':[]},"PLE03":{'IP':'10.254.3.114','HOS_USER_PORTS':[],'NFS_HOS_PORTS':[],'NFS_DMZ_PORTS':['ae28','ae29'],'DMZ_USER_PORTS':['ae24','ae25']},"PLE53":{'IP':'10.254.3.115','HOS_USER_PORTS':[],'NFS_HOS_PORTS':[],'NFS_DMZ_PORTS':['ae28','ae29'],'DMZ_USER_PORTS':['ae24','ae25']}}


def create_user_hos_vlan_config(vlan_id,vlan_name):
	config={}
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

def apply_config_to_sw(config,sw_name,verbose=False):
	dev = Device(host=PLE_SW_LIST[sw_name]['IP'],user="jspace").open()
	if verbose: print("Connection opened to " + sw_name + " on IP " + PLE_SW_LIST[sw_name]['IP'])	
	if verbose: print("Trying to apply the following configuration: ")
	if verbose: print(config)
	co=Config(dev, mode='private')  
	co.load(config, format='set')
	if verbose: cu.pdiff()
	co.commit()

def apply_config(config,verbose=False):
	for SW in PLE_SW_LIST.keys():
		apply_config_to_sw(config[SW],SW,verbose)
		
		
		

