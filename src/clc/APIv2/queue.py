"""
Queue related functions.  

These queue related functions generally align one-for-one with published API calls categorized in the queue category

API v2 - https://t3n.zendesk.com/forums/21772620-Queue

Server object variables:


"""

# TODO - implement wait until

import json
import clc


class Queue(object):
	pass



class Requests(object):

	def __init__(self,requests_lst,alias=None):
		"""Create Requests object.

		Treats one or more requests as an atomic unit.
		e.g. if performing a simulated group operation then succeed
		or fail as a group

		"""

		if alias:  self.alias = alias
		else:  self.alias = clc.v2.Account.GetAlias()

		self.requests = []
		for r in requests_lst:
			if 'server' in r:  
				context_key = "server"
				context_val = r['server']

			if not r['isQueued']:  raise(clc.CLCException("%s '%s' not added to queue: %s" % (context_val,context_key,r['errorMessage'])))

			self.requests.append(Request(id,alias=self.alias,request_obj={'context_key': context_key, 'context_val': context_val}))



class Request(object):

	def __init__(self,id,alias=None,request_obj=None):
		"""Create Queue object.

		https://t3n.zendesk.com/entries/32859214-Get-Server

		#If parameters are populated then create object location.  
		#Else if only id is supplied issue a Get Policy call

		>>> clc.v2.Server("CA3BTDICNTRLM01")
		<clc.APIv2.server.Server object at 0x10c28fe50>
		>>> print _
		CA3BTDICNTRLM01

		"""

		self.id = id

		if alias:  self.alias = alias
		else:  self.alias = clc.v2.Account.GetAlias()

		if server_obj:  self.data = server_obj
		else:  self.data = clc.v2.API.Call('GET','servers/%s/%s' % (self.alias,self.id),{})
		#import pprint
		#pprint.pprint(self.data)


	def __getattr__(self,var):
		if var in self.data:  return(self.data[var])
		elif var in self.data['details']:  return(self.data[var])
		else:  raise(AttributeError("'%s' instance has no attribute '%s'" % (self.__class__.__name__,var)))


	def Account(self):
		"""Return account object for account containing this server.

		>>> clc.v2.Server("CA3BTDICNTRLM01").Account()
		<clc.APIv2.account.Account instance at 0x108789878>
		>>> print _
		BTDI
		
		"""

		return(clc.v2.Account(alias=self.alias))


	def Group(self):
		"""Return group object for group containing this server.

		>>> clc.v2.Server("CA3BTDICNTRLM01").Group()
		<clc.APIv2.group.Group object at 0x10b07b7d0>
		>>> print _
		Ansible Managed Servers

		"""

		return(clc.v2.Group(id=self.groupId,alias=self.alias))

	
	def _Operation(self,operation):
		data = clc.v2.API.Call('POST','operations/%s/servers/%s' % (self.alias,operation),{'serverIds': self.id})
		import pprint
		pprint.pprint(data)


	def Pause(self):  return(self._Operation('pause'))
	def ShutDown(self):  return(self._Operation('shutDown'))
	def Reboot(self):  return(self._Operation('reboot'))
	def Reset(self):  return(self._Operation('reset'))
	def PowerOn(self):  return(self._Operation('powerOn'))
	def PowerOff(self):  return(self._Operation('powerOff'))


	def Snapshot(self,expiration_days=7):
		"""Take a Hypervisor level snapshot retained for between 1 and 10 days (7 is default).

		"""

		data = clc.v2.API.Call('POST','operations/%s/servers/createSnapshot' % (self.alias),
		                       {'serverIds': self.id, 'snapshotExpirationDays': expiration_days},debug=True)
		import pprint
		pprint.pprint(data)


#	def Create(self,name,description=None):  
#		"""Creates a new group
#
#		*TODO* 
#
#		"""
#
#		if not description:  description = name
#
#		#clc.v2.API.Call('POST','groups/%s' % (self.alias),{'name': name, 'description': description, 'parentGroupId': self.id},debug=True)
#		raise(Exception("Not implemented"))
#
#
#	def Update(self):
#		"""Update group
#
#		*TODO* API not yet documented
#
#		"""
#		raise(Exception("Not implemented"))
#
#
#	def Delete(self):
#		"""Delete server.
#		
#		"""
#		#status = {u'href': u'/v2/operations/btdi/status/wa1-126437', u'id': u'wa1-126437', u'rel': u'status'}
#		status = clc.v2.API.Call('DELETE','groups/%s/%s' % (self.alias,self.id),{})


	def __str__(self):
		return(self.data['name'])

