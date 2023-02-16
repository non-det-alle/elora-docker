#! /usr/bin/env python3

import toml
import os
import subprocess as sp
import signal

# Load configurations
configpath = os.environ['HOME'] + '/configuration.toml'
configs = toml.load(configpath)

# Define iptables rules
dest = configs['destAddr']
tap = configs['tap']
sp.run(['iptables', '-t', 'nat', '-A', 'PREROUTING', '-i', tap,
       '-p', 'udp', '-j', 'DNAT', '--to-destination', dest])
sp.run(['iptables', '-t', 'nat', '-A', 'POSTROUTING', '-o', 'eth0',
       '-p', 'udp', '-j', 'MASQUERADE', '--to-ports', '40000-50000'])

# Run ns-3 simulation
run = configs['run']
ns3 = os.environ['NS3DIR'] + '/./ns3'
target = run['target']
options = ['--cwd', os.environ['OUTPUT']]
args = ['--']
if 'args' in run:
    for p, v in run['args'].items():
        args.append('--' + p + '=' + str(int(v) if isinstance(v, bool) else v))
sp.run([ns3, 'run', target] + options + args)
