#!/usr/bin/env python3
""" Skeleton Implementation of Project 2 for NEU CS3700 """

import argparse
import json
import select
import socket

##########################################################################################

# Message Fields
TYPE = "type"
SRCE = "src"
DEST = "dst"
MESG = "msg"
TABL = "table"

# Message Types
DATA = "data"
DUMP = "dump"
UPDT = "update"
RVKE = "revoke"
NRTE = "no route"

# Update Message Fields
NTWK = "network"
NMSK = "netmask"
ORIG = "origin"
LPRF = "localpref"
APTH = "ASPath"
SORG = "selfOrigin"

# internal route info
CUST = "cust"
PEER = "peer"
PROV = "prov"


##########################################################################################

class Router:
  """ Your Router """
  def __init__(self, networks):
    self.routes = {}
    self.updates = {}
    self.relations = {}
    self.sockets = {}
    for relationship in networks:
      network, relation = relationship.split("-")
      self.sockets[network] = socket.socket(socket.AF_UNIX, socket.SOCK_SEQPACKET)
      self.sockets[network].setblocking(0)
      self.sockets[network].connect(network)
      self.relations[network] = relation

  def lookup_routes(self, daddr):
    """ Lookup all valid routes for an address """
    # TODO
    outroutes = []
    return outroutes

  def get_shortest_as_path(self, routes):
    """ select the route with the shortest AS Path """
    # TODO
    outroutes = []
    return outroutes

  def get_highest_preference(self, routes):
    """ select the route with the shortest AS Path """
    # TODO
    outroutes = []
    return outroutes

  def get_self_origin(self, routes):
    """ select self originating routes """
    # TODO
    outroutes = []
    return outroutes

  def get_origin_routes(self, routes):
    """ select origin routes: EGP > IGP > UNK """
    # TODO
    outroutes = []
    return outroutes

  def filter_relationships(self, srcif, routes):
    """ Don't allow Peer->Peer, Peer->Prov, or Prov->Peer forwards """
    outroutes = []
    return outroutes

  def get_route(self, srcif, daddr):
    """ Select the best route for a given address """
    # TODO
    peer = None
    routes = self.lookup_routes(daddr)
    # Rules go here
    if routes:
      # 1. Highest Preference
      routes = self.get_highest_preference(routes)
      # 2. Self Origin
      routes = self.get_self_origin(routes)
      # 3. Shortest ASPath
      routes = self.get_shortest_as_path(routes)
      # 4. EGP > IGP > UNK
      routes = self.get_origin_routes(routes)
      # 5. Lowest IP Address
      # TODO
      # Final check: enforce peering relationships
      routes = self.filter_relationships(srcif, routes)
    return self.sockets[peer] if peer else None

  def forward(self, srcif, packet):
    """ Forward a data packet """
    # TODO
    return False

  def coalesce(self):
    """ coalesce any routes that are right next to each other """
    # TODO (this is the most difficult task, save until last)
    return False

  def update(self, srcif, packet):
    """ handle update packets """
    # TODO 
    nwork = packet[MESG][NTWK]
    nmask = packet[MESG][NMSK]
    peer = packet[SRCE]
    self.updates[nwork] = {NTWK: nwork, NMSK: nmask, PEER: peer}
    for network in self.sockets:
      if network != srcif:
        packet[DEST] = network
        packet[SRCE] = network[:-1] + '1'
        msg = json.dumps(self.sockets[network])
        print(msg)
        self.sockets[network].send(msg)
    return False

  def revoke(self, packet):
    """ handle revoke packets """
    # TODO
    return True

  def dump(self, packet):
    """ handles dump table requests """
    # TODO
    return True

  def handle_packet(self, srcif, packet):
    """ dispatches a packet """
    if packet[TYPE] == "update":
      self.update(srcif, packet)
    if packet[TYPE] == "revoke":
      self.revoke(packet)
    if packet[TYPE] == "data":
      self.forward(srcif, packet)
    if packet[TYPE] == "dump":
      self.dump(packet)
    # TODO
    return False

  def send_error(self, conn, msg):
    """ Send a no_route error message """
    # TODO
    return

  def run(self):
    """ main loop for the router """
    while True:
      socks = select.select(self.sockets.values(), [], [], 0.1)[0]
      for conn in socks:
        try:
          k = conn.recv(65535)
        except:
          # either died on a connection reset, or was SIGTERM's by parent
          return
        if k:
          for sock in self.sockets:
            if self.sockets[sock] == conn:
              srcif = sock
          msg = json.loads(k)
          print(msg)
          if not self.handle_packet(srcif, msg):
            self.send_error(conn, msg)
        else:
          return

if __name__ == "__main__":
  PARSER = argparse.ArgumentParser(description='route packets')
  PARSER.add_argument('networks', metavar='networks', type=str, nargs='+', help="networks")
  ARGS = PARSER.parse_args()
  Router(ARGS.networks).run()
