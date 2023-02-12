#! /usr/bin/env python3

import toml
import os

configpath = os.environ['HOME'] + "/configuration.toml"
assert os.path.exists(configpath), "Missing configuration.toml file in /home/elora"
configs = toml.load(configpath)

ns3 = os.environ['NS3DIR'] + "/./ns3"
assert 'target' in configs, "Simulation target not specified in configuration.toml"
target = configs['target']
options = "--cwd " + os.environ['OUTPUT']

command = ns3 + " run " + target + " " + options + " --"

if 'args' in configs:
    for p, v in configs['args'].items():
        arg = " --" + p + "="
        if isinstance(v, bool):
            arg += str(int(v))
        elif isinstance(v, str):
            arg += "\"" + v + "\""
        else:
            arg += str(v)
        command += arg

os.system(command)
