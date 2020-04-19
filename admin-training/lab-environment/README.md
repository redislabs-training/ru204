# Lab Environment Overview

Much more than lab setup.

## Overview

Gives you an <overview> of what's in the environment and what it looks like when you use it.

Each student gets a VM with a bunch of stuff in it.

<overview link>

## Start VMs

Shows you how to <start VMs> as an employee or instructor.

## Use VMs

Shows you how to <use VMs>.

This is not the lab manual. The lab manual has many more steps. This is an overview for employees and instructors on how to use the VM.

## VM Stage 1 Config

Shows you how to <config a Stage 1 VM> with the Docker network and vanilla VNC.

VMs are created in stages for easy re-config.

## VM Stage 2 Config

Shows you how to <configure a Stage 2 VM> with <configured DNS>.

## VM Stage 3 Config

Shows you how to <configure a Stage 3 VM> with <configured VNC>.

## Why Stages

If you want to update a Stage 1 VM with new OS or Redis:
- Configure the new Stage 1 VM
- Start a Stage 2 VM and bring in the configured DNS Docker image from GCR.
- Start a Stage 3 VM and bring in the configured VNC Docker image from GCR.

