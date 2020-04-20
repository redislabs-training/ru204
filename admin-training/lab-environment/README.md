# Lab Environment

Each user gets a VM that runs ***two*** RES clusters with DNS resolution.

This site explains:
1. What's [in a VM](Overview)
2. How to [start VMs](start-vms)
3. How to [use VMs]
4. How to [config VMs](config-vms).

VMs are configured in 3 stages for easy re-config.

User VMs are started from a Stage 3 VM image or instance template.

A Stage 1 VM includes Ubuntu, RES, Docker network, VNC.
A Stage 2 VM adds configured DNS.
A Stage 3 VM adds configured VNC.

If you want to update a Stage 1 VM with new OS or Redis:
- Configure a new Stage 1 VM
- Start a Stage 2 VM and add the DNS Docker image.
- Start a Stage 3 VM and add the VNC Docker image.
