.. vim: spell spelllang=en

=====================================================================
 Python-based Simulation of the Helper Node in Wireless Mesh Network
=====================================================================

Description
===========

The broadcast nature of the wireless channel allows neighboring nodes to
overhear transmissions of the main route.
Considering that wireless channels suffer from significant packet losses, this
overhearing opens interesting possibilities for exploiting neighboring nodes to
forward a packet opportunistically in order to enhance overall performance.

.. image: helper.gif

On the other hand the sender and helper cannot send at the same time.
If the helper cannot provide new information to the receiver it is just
stealing the sending time of the sender.

The task is to build a basic simulation of this scenario using Kodo Python.
This simulation can then be used to compare different sending policies of the
helper node.

Prerequisites
=============

 * Python programming
 * Kodo-Python https://github.com/steinwurf/kodo-python
 * Plotting

Supervisor
==========
 * Dipl.-Inf. Frank Wilhelm <frank.wilhelm@tu-dresden.de>

