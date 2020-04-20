# Lab Environment

This site explains more than just lab setup.

## Overview

This shows what's [in the environment] and what it looks like when you use it.

Each student gets a VM with a bunch of stuff in it.

## Start VMs

This shows how to [start VMs] as an employee or instructor.

## Use VMs

This shows how to [use VMs]. It's not the lab manual. The lab manual has many more steps.

## Config VMs

VMs are created in stages for easy re-config.

#### Stage 1

This shows how to [config a Stage 1 VM] with Docker networking and vanilla VNC.

#### Stage 2

This shows how to [configure a Stage 2 VM] with [configured DNS].

#### Stage 3

This shows how to [configure a Stage 3 VM] with [configured VNC].

## How Stages Help

If you want to update a Stage 1 VM with new OS or Redis:
- Configure the new Stage 1 VM
- Start a Stage 2 VM and bring in the configured DNS Docker image.
- Start a Stage 3 VM and bring in the configured VNC Docker image.

