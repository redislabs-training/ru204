# Lab Environment

This site explains:
- What's in lab VMs
- How to start VMs
- How to use VMs
- How to configure VMs.

Each user/student gets a VM that they can use to run two Redis Labs clusters with DNS database resolution.

VMs are created in 3 stages for easy re-config.

A Stage 1 VM includes Ubuntu, RES, a Docker network, and VNC.
A Stage 2 VM adds configured DNS.
A Stage 3 VM adds configured VNC.

If you want to update a Stage 1 VM with new OS or Redis:
- Configure a new Stage 1 VM
- Start a Stage 2 VM and bring in the configured DNS Docker image.
- Start a Stage 3 VM and bring in the configured VNC Docker image.
