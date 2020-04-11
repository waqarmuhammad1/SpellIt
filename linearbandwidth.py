#!/usr/bin/python

"""
Test bandwidth (using iperf) on linear networks of varying size,
using both kernel and user datapaths.

We construct a network of N hosts and N-1 switches, connected as follows:

h1 <-> s1 <-> s2 .. sN-1
       |       |    |
       h2      h3   hN

WARNING: by default, the reference controller only supports 16
switches, so this test WILL NOT WORK unless you have recompiled
your controller to support 100 switches (or more.)

In addition to testing the bandwidth across varying numbers
of switches, this example demonstrates:

- creating a custom topology, LinearTestTopo
- using the ping() and iperf() tests from Mininet()
- testing both the kernel and user switches

"""


from mininet.net import Mininet
from mininet.node import UserSwitch, OVSKernelSwitch, Controller
from mininet.topo import Topo
from mininet.log import lg, info
from mininet.util import irange, quietRun
from mininet.link import TCLink
from mininet.log import setLogLevel

from functools import partial

import sys
import csv
import random
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import pprint
flush = sys.stdout.flush
plt.close('all')
class LinearTestTopo( Topo ):
    "Topology for a string of N hosts and N-1 switches."

    def build( self, N, **params ):
        # Create switches and hosts
        hosts = [ self.addHost( 'h%s' % h )
                  for h in irange( 1, N ) ]
        switches = [ self.addSwitch( 's%s' % s )
                     for s in irange( 1, N - 1 ) ]

        # Wire up switches
        last = None
        for switch in switches:
            if last:
                self.addLink( last, switch )
            last = switch

        # Wire up hosts
        self.addLink( hosts[ 0 ], switches[ 0 ] )
        for host, switch in zip( hosts[ 1: ], switches ):
            self.addLink( host, switch )

def ping_function(lengths):
    pings=[]
    topo = LinearTestTopo(lengths)
    net = Mininet( topo=topo )
    net.start()
    for n in range(0,lengths):
        pings.append([])
        for m in range(0,lengths):
            if n==m:
                pings[n].append(None)
                continue

            pings[n].append(net.pingFull( [ net.hosts[ n ], net.hosts[ m ] ] )[0][2][3])
        #pings.append(net.pingFull( [ net.hosts[ 0 ], net.hosts[ n ] ] )[0][2][3])
        #print(len(net.hosts),n)
    with open("fullresolution.csv", "wb") as f:
        writer = csv.writer(f)
        writer.writerows(pings)
    net.stop()

def random_ping_function(lengths):
    topo = LinearTestTopo(lengths)
    net = Mininet( topo=topo )
    net.start()

    node_pool = range(lengths)
    random.shuffle(node_pool)
    while node_pool:
        pings=[]
        poppy = [node_pool.pop(),node_pool.pop()]
        poppy.sort()
        #print(poppy)
        sub_list = []
        for n in range(poppy[0],poppy[1]+1):
            sub_list.append(n)
        for i,n in enumerate(sub_list):
            pings.append([])
            for j,m in enumerate(sub_list):
                if n==m:
                    pings[i].append(0.0)
                    continue

                pings[i].append(net.pingFull( [ net.hosts[ n ], net.hosts[ m ] ] )[0][2][3])
        df = pd.DataFrame(pings, index=sub_list, columns=sub_list)

        low_res_list = []
        new_i=0
        for index, row in df.iterrows():

            for item in row:
                low_res_list.append([index,item])
            ++new_i
        pp = pprint.PrettyPrinter(depth=6)
        low_rez_df = pd.DataFrame(low_res_list, columns=("origin","destination"))
        #pp.pprint(low_res_list)
        low_rez_df.plot(kind='hexbin',x='origin',y='destination',gridsize=50,cmap='inferno')
        plt.show()
    net.stop()

def linearBandwidthTest( lengths ):

    "Check bandwidth at various lengths along a switch chain."

    results = {}
    switchCount = max( lengths )
    hostCount = switchCount + 1

    switches = { 'reference user': UserSwitch,
                 'Open vSwitch kernel': OVSKernelSwitch }

    # UserSwitch is horribly slow with recent kernels.
    # We can reinstate it once its performance is fixed
    del switches[ 'reference user' ]

    topo = LinearTestTopo( hostCount )

    # Select TCP Reno
    output = quietRun( 'sysctl -w net.ipv4.tcp_congestion_control=reno' )
    assert 'reno' in output

    for datapath in switches.keys():
        info( "*** testing", datapath, "datapath\n" )
        Switch = switches[ datapath ]
        results[ datapath ] = []
        link = partial( TCLink, delay='2ms', bw=10 )
        net = Mininet( topo=topo, switch=Switch,
                       controller=Controller, waitConnected=True,
                       link=link )
        net.start()
        info( "*** testing basic connectivity\n" )
        for n in lengths:
            net.ping( [ net.hosts[ 0 ], net.hosts[ n ] ] )
        info( "*** testing bandwidth\n" )
        for n in lengths:
            src, dst = net.hosts[ 0 ], net.hosts[ n ]
            # Try to prime the pump to reduce PACKET_INs during test
            # since the reference controller is reactive
            src.cmd( 'telnet', dst.IP(), '5001' )
            info( "testing", src.name, "<->", dst.name, '\n' )
            # serverbw = received; _clientbw = buffered
            serverbw, _clientbw = net.iperf( [ src, dst ], seconds=10 )
            info( serverbw, '\n' )
            flush()
            results[ datapath ] += [ ( n, serverbw ) ]
        net.stop()

    for datapath in switches.keys():
        info( "\n*** Linear network results for", datapath, "datapath:\n" )
        result = results[ datapath ]
        info( "SwitchCount\tiperf Results\n" )
        for switchCount, serverbw in result:
            info( switchCount, '\t\t' )
            info( serverbw, '\n' )
        info( '\n')
    info( '\n' )
setLogLevel('error')
topos = { 'mytopo': ( lambda: LinearTestTopo(5) ) }
random_ping_function(10)
