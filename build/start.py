#! /usr/bin/env python3

import toml
import os
import subprocess

# Load configurations
configpath = os.environ['HOME'] + '/configuration.toml'
configs = toml.load(configpath)

# Define iptables rules
dest = configs['destAddr']
if dest == "127.0.0.1" or dest == "localhost":
    dest = "172.17.0.1"
tap = configs['tap']
subprocess.run(['iptables', '-t', 'nat', '-A', 'PREROUTING', '-i', tap,
                '-p', 'udp', '-j', 'DNAT', '--to-destination', dest])
subprocess.run(['iptables', '-t', 'nat', '-A', 'POSTROUTING', '-o', 'eth0',
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
subprocess.run([ns3, 'run', target] + options + args,
               stdin=subprocess.PIPE)
