# Building the Lab

Color | Meaning
---|---
![](https://placehold.it/15/c5f015/000000) | vanilla
![](https://placehold.it/15/f03c15/000000) | configured
![](https://placehold.it/15/1589F0/000000) | blue

## Here's what you get

## Here's what you build

### Stage 1 VM


Starting point

```diff
- Ubuntu 18.04
- Redis 5.4 
- vanilla VNC
```

Finishing point

\ Ubuntu 18.04 /  \ Redis 5.4 /  \ vanilla VNC /  / ***Stage 1 changes*** \

### Stage 2 VM

Starting point

\ Ubuntu 18.04 /  \ Redis 5.4 /  \ vanilla VNC /  / Stage 1 changes \  \ ***vanilla DNS*** /

Finishing point

\ Ubuntu 18.04 /  \ Redis 5.4 /  \ vanilla VNC /  / Stage 1 changes \  / ***Stage 2 changes*** \  / ***configured DNS*** \

### Stage 3 VM

Starting point

\ Ubuntu 18.04 /  \ Redis 5.4 /  \ vanilla VNC /  / Stage 1 changes \  / Stage 2 changes \  / configured DNS \

Finishing point

\ Ubuntu 18.04 /  \ Redis 5.4 /  / Stage 1 changes \  / Stage 2 changes \  / configured DNS \  / ***configured VNC*** \ / ***Keys*** \ 

## Here's how you modify what you build
