#! /usr/bin/env python3

from toml import load
from os import environ
from subprocess import run, Popen
from signal import SIGTERM, signal

# Load and validate configuration
try:
    config = load(environ["HOME"] + "/configuration.toml")
    dest_addr = config["destAddr"]
    tap_name = config["tap"]
    target_name = config["run"]["target"]
except:
    print("Configuration file error")
    exit(1)

# Create tap device
run(["mkdir", "-p", "/dev/net"])
run(["mknod", "/dev/net/tun", "c", "10", "200"])
run(["chmod", "600", "/dev/net/tun"])

# Create iptables rules
run(
    ["iptables", "-t", "nat", "-A", "PREROUTING", "-i", tap_name, "-p", "udp"]
    + ["-j", "DNAT", "--to-destination", dest_addr]
)
run(
    ["iptables", "-t", "nat", "-A", "POSTROUTING", "-o", "eth0", "-p", "udp"]
    + ["-j", "MASQUERADE", "--to-ports", "40000-50000"]
)

# Build ns-3 command
ns3_run = [environ["NS3DIR"] + "/./ns3", "run"]
options = ["--cwd", environ["OUTPUT"]]
target = [target_name]
if "args" in config["run"] and config["run"]["args"]:
    target.append("--")
    for p, v in config["run"]["args"].items():
        if isinstance(v, bool):
            v = int(v)
        target.append("--" + p + "=" + str(v))

# Run ns-3 simulation
try:
    p = Popen(ns3_run + options + target)
    # Propagate SIGTERM from docker stop
    signal(SIGTERM, lambda: p.send_signal(SIGTERM))
    p.wait()
except KeyboardInterrupt:
    exit(0)
