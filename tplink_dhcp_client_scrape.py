import requests
from pprint import pprint


class TPLINK_DHCP_LIST(object):
	url = 'HTTP://192.168.1.1/cgi'
	user = ''
	passwd = ''
	dhcp_post_data = "[LAN_HOST_ENTRY#0,0,0,0,0,0#0,0,0,0,0,0]0,4\r\nleaseTimeRemaining\r\nMACAddress\r\nhostName\r\nIPAddress\r\n"
	req_params = {"5":""}

	def __init__(self, auth=('admin','admin') ):
		self.user,self.passwd = auth

	def req_client_list(self):
		sesh = requests.Session()
		r2 = sesh.post(self.url, data=self.dhcp_post_data, auth=(self.user, self.passwd), params=self.req_params)
		sesh.close()
		return r2.text

	def scrape_resp(self,doc):
		encoded_str = doc.encode("ascii",'ignore')
		ents = []
		index = -1;
		for line in encoded_str.splitlines(True):
			if line.startswith('['):
				index +=1
				ents.append({})
			else:
				ent = line.replace('\n','').split('=')
				ent = dict ([(ent[0],ent[1])])
				ents[index].update(ent)
		return ents

	def req_and_parse(self):
		resp_data = self.req_client_list()
		self.resp = self.scrape_resp(resp_data)
		return self.resp
		

if __name__ == "__main__":
	pprint (TPLINK_DHCP_LIST().req_and_parse())