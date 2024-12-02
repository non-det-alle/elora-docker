#! /usr/bin/env python3

import toml, os, subprocess, signal

# Load configuration
config = toml.load(os.environ["HOME"] + "/configuration.toml")

# Create iptables rules
dest = config["destAddr"]
if dest == "127.0.0.1" or dest == "localhost":
    # docker bridge network gateway
    dest = "172.17.0.1"
tap = config["tap"]
subprocess.run(
    ["iptables", "-t", "nat", "-A", "PREROUTING", "-i", tap, "-p", "udp"]
    + ["-j", "DNAT", "--to-destination", dest]
)
subprocess.run(
    ["iptables", "-t", "nat", "-A", "POSTROUTING", "-o", "eth0", "-p", "udp"]
    + ["-j", "MASQUERADE", "--to-ports", "40000-50000"]
)

# Run ns-3 simulation
ns3_run = [os.environ["NS3DIR"] + "/./ns3", "run"]
options = ["--cwd", os.environ["OUTPUT"]]
target = [config["run"]["target"]]
if "args" in config["run"] and config["run"]["args"]:
    target.append("--")
    for p, v in config["run"]["args"].items():
        if isinstance(v, bool):
            v = int(v)
        target.append("--" + p + "=" + str(v))
with subprocess.Popen(ns3_run + options + target) as proc:

    def handle(signum, _):
        proc.send_signal(signum)
        proc.wait()

    signal.signal(signal.SIGTERM, handle)
    proc.wait()
