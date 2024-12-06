#! /usr/bin/env python3

import toml, os, subprocess, signal

# Load and validate configuration
try:
    config = toml.load(os.environ["HOME"] + "/configuration.toml")
    dest_addr = config["destAddr"]
    tap_name = config["tap"]
    target_name = config["run"]["target"]
except:
    print("Configuration file error")
    exit(1)

# Create tap device
subprocess.run(["mkdir", "-p", "/dev/net"])
subprocess.run(["mknod", "/dev/net/tun", "c", "10", "200"])
subprocess.run(["chmod", "600", "/dev/net/tun"])

# Create iptables rules
if dest_addr == "127.0.0.1" or dest_addr == "localhost":
    # docker bridge network gateway
    dest_addr = "172.17.0.1"
subprocess.run(
    ["iptables", "-t", "nat", "-A", "PREROUTING", "-i", tap_name, "-p", "udp"]
    + ["-j", "DNAT", "--to-destination", dest_addr]
)
subprocess.run(
    ["iptables", "-t", "nat", "-A", "POSTROUTING", "-o", "eth0", "-p", "udp"]
    + ["-j", "MASQUERADE", "--to-ports", "40000-50000"]
)

# Build ns-3 command
ns3_run = [os.environ["NS3DIR"] + "/./ns3", "run"]
options = ["--cwd", os.environ["OUTPUT"]]
target = [target_name]
if "args" in config["run"] and config["run"]["args"]:
    target.append("--")
    for p, v in config["run"]["args"].items():
        if isinstance(v, bool):
            v = int(v)
        target.append("--" + p + "=" + str(v))

# Run ns-3 simulation
with subprocess.Popen(ns3_run + options + target) as proc:

    def handle(signum, _):
        proc.send_signal(signum)
        proc.wait()

    signal.signal(signal.SIGTERM, handle)
    proc.wait()
