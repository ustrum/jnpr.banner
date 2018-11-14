
from jnpr.junos import Device
from jnpr.junos.utils.config import Config


OOB_SW_LIST = { "ODI":'10.254.3.110',"OAC01":'10.254.3.111',"OAC02":'10.254.3.112',"OAC03":'10.254.3.113',"OAC04":'10.254.3.114',"OAC05":'10.254.3.115',"OAC06":'10.254.3.116',"OAC07":'10.254.3.117',"OAC08":'10.254.3.118'}

conf='set system login message "Remember to use your NGAHRUSER account to log in.\n\n"'


conf='set system login message "\\n\\       ****************************************************\\n       *                                                  *\\n       *            Unauthorized access to this           *\\n       *                                                  *\\n       *               Device is prohibited !             *\\n       *                                                  *\\n       ****************************************************\\n\\n\\nRemember to use your NGAHRUSER account to log in.\\n\\n"'

for SW_IP in OOB_SW_LIST.values():
	dev = Device(host=SW_IP,user="jspace").open()
	with Config(dev, mode='private') as cu:  
		cu.load(conf, format='set')
		cu.pdiff()
		cu.commit()
	