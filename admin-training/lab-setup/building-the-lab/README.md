# Building the Lab

Color codings.

```diff
+ vanilla
! configured (pluggable)
- configured (unpluggable)
```

## Here's what you get

## Here's what you build

### Stage 1 VM

Starting point

```diff
+ Ubuntu 18.04
+ Redis 5.4 
+ vanilla VNC
```

Finishing point

```diff
+ Ubuntu 18.04
+ Redis 5.4 
+ vanilla VNC
- stage 1 changes
```

### Stage 2 VM

Starting point

```diff
+ Ubuntu 18.04
+ Redis 5.4 
+ vanilla VNC
+ vanilla DNS
- stage 1 changes
```

Finishing point

```diff
+ Ubuntu 18.04
+ Redis 5.4 
+ vanilla VNC
! configured DNS
- stage 1 changes
- stage 2 changes
```

### Stage 3 VM

Starting point

```diff
+ Ubuntu 18.04
+ Redis 5.4 
+ vanilla VNC
! configured DNS
- stage 1 changes
- stage 2 changes
```

Finishing point

```diff
+ Ubuntu 18.04
+ Redis 5.4 
! configured VNC
! configured DNS
- stage 1 changes
- stage 2 changes
- stage 3 changes
```

## Here's how you modify what you build
