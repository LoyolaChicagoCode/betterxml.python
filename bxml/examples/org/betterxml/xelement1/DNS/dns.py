"""
XIR Toolkit
Copyright (c) 2003 by Nimkathana Corporation
Licensed under the LGPL (included with the source code)

        Source: $Id: dns.py,v 1.1 2006/07/16 22:22:07 gkt Exp $

    Revised by: $Author: gkt $

 Revision date: $Date: 2006/07/16 22:22:07 $

"""
import sys
import os
import os.path

sys.path.append('../../../../../src/')

from org.betterxml.xelement1.xparser import XElementParser
from org.betterxml.xelement1.xelement import XElement

SOA_TEMPLATE = """
;
; Zone file for %(domain)s
@       IN      SOA     %(ns_host)s %(contact)s.%(domain)s. (
; serial number
                        %(serial)s
; refresh
			%(refresh)s
; retry
			%(retry)s
; expire
			%(expire)s
; minimum TTL
                        %(minimum)s)
"""

NS_TEMPLATE = """
; Inet address of nameserver
	NS	%(name)s
"""

MX_TEMPLATE = """
; Mail exchanger record
	MX	%(priority)s %(name)s.%(domain)s.
"""

A_TEMPLATE = """
%(name)s	A	%(ip)s
"""

CNAME_TEMPLATE = """
%(alias)s	A 	%(name)s
"""

class Zones(XElement):
   def initialize(self):
      self.zones = {}

   def getZones(self):
      return self.zones

   def process(self):
      for zone in self.getChildren(ZoneConfiguration):
          zone_name = zone.getAttribute("domain")
          if not self.zones.has_key(zone_name):
             self.zones[zone_name] = zone
          else:
             raise "duplicate zone %s" % zone_name

      for zone in self.getChildren(ZoneConfiguration):
          zone.build(self) 

   def encode(self):
      for zone in self.getChildren(ZoneConfiguration):
          zone.encodeFile()

   def dump(self):
      for zone in self.getChildren(ZoneConfiguration):
          zone.dump()
     

class ZoneConfiguration(XElement):
   def initialize(self):
      self.hosts = {}
      self.ttl = None
      self.ns_hosts = []
      self.mx_hosts = []

   def setHost(self, host):
      host_name = host.getAttribute("name")
      if not self.hosts.has_key(host_name):
         self.hosts[host_name] = host
         

   def setTTL(self, ttl):
      if self.ttl == None:
         self.ttl = ttl

   def check_name_servers(self):
      self.ns_hosts = []
      for h in self.hosts.keys():
         host_ns = self.hosts[h].getAttribute("ns", "no")
         if host_ns == "yes":
            self.ns_hosts.append(self.hosts[h]);
      if not self.ns_hosts:
         raise "domain without nameserver"

   def check_mail_exchangers(self):
      self.mx_hosts = []
      for h in self.hosts.keys():
         host_mx = self.hosts[h].getAttribute("mail_exchange", "no")
         if host_mx == "yes":
            self.mx_hosts.append(self.hosts[h]);
      if not self.mx_hosts:
         print "warning: domain w/o mail exchanger"

   def build(self, zones):
      """
      Build zone table for a particular zone. This method must be recursive
      in the case of a depends_on attribute.
      """
      zones_visited = {}
      self.build_recursive(zones.getZones(), zones_visited, self)
      self.check_name_servers()
      self.check_mail_exchangers()

   def build_recursive(self, zone_table, zones_visited, zone_to_update):
      zone_domain = self.getAttribute("domain")
      if zones_visited.has_key(zone_domain):
         print "warning: cycle detected based on %s" % zone_domain
         return
      zones_visited[zone_domain] = zone_domain
      for ttl in self.getChildren(TTL):
         zone_to_update.setTTL(ttl)
      for host in self.getChildren(Host):
         zone_to_update.setHost(host)
      zone_based_on = self.getAttribute("based_on")
      if zone_table.has_key(zone_based_on):
         zone_table[zone_based_on].build_recursive(zone_table, zones_visited, zone_to_update)

   def dump(self):
      print "; Configuration for %s " % self.getAttribute("domain")
      print "; Generated by Core XML DNS Tool"
      my_attrs = self.getAttributes().asDict()
      my_attrs.update(self.ttl.getAttributes().asDict())
      my_attrs['ns_host'] = self.ns_hosts[0].getAttribute('name')
      my_attrs['serial'] = '<<add code for date>>'
      print SOA_TEMPLATE % my_attrs
      for h in self.mx_hosts:
          mx_domain_dict = my_attrs.copy()
          mx_dict = h.getAttributes().asDict()
          mx_domain_dict.update(mx_dict)
          mx_domain_dict['priority'] = '<<add priority (dynamic) here'
          print MX_TEMPLATE % mx_domain_dict
      for h in self.ns_hosts:
          print NS_TEMPLATE % h.getAttributes().asDict()
      for host_name in self.hosts.keys():
          print A_TEMPLATE % self.hosts[host_name].getAttributes().asDict()

   def encodeFile(self):
      pass
      
class Description(XElement): pass

class TTL(XElement): pass

class Alias(XElement): pass

class Host(XElement): pass

my_classes = { 
   'Zones' : Zones,
   'ZoneConfiguration' : ZoneConfiguration,
   'Description' : Description,
   'TTL' : TTL,
   'Alias' : Alias,
   'Host' : Host
}

xparser = XElementParser(my_classes)
doc = xparser.process(sys.argv[1])
doc.process()
doc.dump()
