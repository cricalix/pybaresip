# Design of pybaresip

## High level

Rather than faff about with running `baresip` in a subprocess, and try to communicate through the **pty**, take advantage of the fact that `baresip` offers control via DBUS.

## What this library does not do

This library does not concern itself with actually running the `baresip` executable; you're responsible for setting it up and running it. However, some examples are included, and there is an example class that can run `baresip` as a subprocess in a thread. That example is provided as a suggestion, and is not supported.
