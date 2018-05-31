
# OpenFlow Tables

This section describes the components of flow tables and group tables, along with the mechanics of matching and action handling.

1. Find highest-prority matching flow entry
1. Apply instructions
    1.  Modify packet & update match fields (apply actions instruction)
    1.  Update action set (clear actions and/or wirte actions isntructions)
    1.  Update metadata
1. Send match data and action set to next table

## Pipeline Processing

OpenFlow-compliant switches come in two types: OpenFlow-only, and OpenFlow-hybrid. 
OpenFlow-only switches support only OpenFlow operation, in those switches all packets are processed by the OpenFlow pipeline, and can not be processed otherwise.

OpenFlow-hybrid switches support both OpenFlow operation and normal Ethernet switching operation, i.e. traditional L2 Ethernet switching, VLAN isolation, L3 routing (IPv4 routing, IPv6 routing...), ACL and QoS processing.
Those switches should provide a classification mechanism outside of OpenFlow that routes traffic to either the OpenFlow pipeline or the normal pipeline. 
For example, a switch may use the VLAN tag or input port of the packet to decide whether to process the packet using one pipeline or the other, or it may direct all packets to the OpenFlow pipeline.
This classification mechanism is outside the scope of this specification. 
An OpenFlow-hybrid switch may also allow a packet to go from the OpenFlow pipeline to the normal pipeline through the NORMAL and FLOOD reserved ports (see 4.5).

The OpenFlow pipeline of every OpenFlow Logical Switch contains one or more flow tables, each flow table containing multiple flow entries. 
The OpenFlow pipeline processing defines how packets interact with those flow tables (see Figure 2).
An OpenFlow switch is required to have at least one flow table, and can optionally have more flow tables.
An OpenFlow switch with only a single flow table is valid, in this case pipeline processing is greatly simplified.


The flow tables of an OpenFlow switch are sequentially numbered, starting at 0.
Pipeline processing always starts at the first flow table: the packet is first matched against flow entries of flow table 0.
Other flow tables may be used depending on the outcome of the match in the first table.

When processed by a flow table, the packet is matched against the flow entries of the flow table to select a flow entry (see 5.3).
If a flow entry is found, the instruction set included in that flow entry is executed.
These instructions may explicitly direct the packet to another flow table (using the GotoTable Instruction, see 5.9), where the same process is repeated again.
A flow entry can only direct a packet to a flow table number which is greater than its own flow table number, in other words pipeline processing can only go forward and not backward.
Obviously, the flow entries of the last table of the pipeline can not include the Goto-Table instruction.
If the matching flow entry does not direct packets to another flow table, pipeline processing stops at this table, the packet is processed with its associated action set and usually forwarded (see 5.10).

If a packet does not match a flow entry in a flow table, this is a table miss.
The behavior on a table miss depends on the table configuration (see 5.4).
The instructions included in the table-miss flow entry in the flow table can
flexibly specify how to process unmatched packets, useful options include dropping
them, passing them to another table or sending them to the controllers over the 
control channel via packet-in messages (see 6.1.2).

There are few cases where a packet is not fully processed by a flow entry and
pipeline processing stops without processing the packet’s action set or directing 
it to another table. If no table-miss flow entry is present, the packet is dropped (see 5.4). 
If an invalid TTL is found, the packet may be sent to the controller (see 5.12).

The OpenFlow pipeline and various OpenFlow operations process packets of a specific 
type in conformance with the specifications defined for that packet type, unless
the present specification or the OpenFlow configuration specify otherwise.
For example, the Ethernet header definition used by OpenFlow must conform to 
IEEE specifications, and the TCP/IP header definition used by OpenFlow must 
conform to RFC specifications.
Additionally, packet reordering in an OpenFlow switch must conform to the requirements
of IEEE specifications, provided that the packets are processed by the same flow entries, 
group bucket and meter band.


### Pipeline Consistency

The OpenFlow pipeline is an abstraction that is mapped to the actual hardware of the switch.
In some cases, the OpenFlow switch is virtualised on the hardware, for example to support 
multiple OpenFlow switch instances or in the case of an hybrid switch. 
Even if the OpenFlow switch is not virtualised, the hardware typically will not 
correspond to the OpenFlow pipeline, for example OpenFlow assume packets to be 
Ethernet, so non-Ethernet packets would have to be mapped to Ethernet, in another 
example some switch may carry the VLAN information in some internal metadata while 
for the OpenFlow pipeline it is logically part of the packet. 
Some OpenFlow switch may define logical ports implementing complex encapsulations 
that extensively modify the packet headers. The consequence is that a packet on a 
link or in hardware may be mapped differently in the OpenFlow pipeline.

However, the OpenFlow pipeline expect that the mapping to the hardware is consistent, 
and that the OpenFlow pipeline behave consistently. In particular, this is what is expected :

* Tables consistency: the packet must match in the same way in all the OpenFlow flow 
tables, and the only difference in matching must be due to the flow table content and 
explicit OpenFlow processing done by those flow tables. In particular, headers can
not be transparently removed, added or changed between tables, unless explicitly 
specified by OpenFlow processing.

* Flow entry consistency: the way the actions of a flow entry apply to a packet 
must be consistent with the flow entry match. In particular, if a match field in
the flow entry match a specific packet header field, the corresponding set-field 
action in the flow entry must modify the same header field, unless explicit 
OpenFlow processing has modified the packet.

* Group consistency: the application of group must be consistent with flow tables.
In particular, actions parts of a group bucket must apply to the packet the same
way as if they were in a flow table, the only difference must be due to explicit
OpenFlow processing.

* Packet-in consistency: the packet embedded in the packet-in messages must be
consistent with the OpenFlow flow tables. In particular, if the packet-in was
generated directly by a flow entry, the packet received by the controller must
match the flow entry that sent it to the controller.

* Packet-out consistency: the packet generated as the result of a packet-out 
request must be consistent with the OpenFlow flow tables and the packet-in process. 
In particular, if a packet received via a packet-in is is sent directly without 
modifications out a port via a packet-out, the packet on that port must be 
identical as if the packet had been sent to that port instead of encapsulated
in a packet-in. Similarly, if a packet-out is directed at flow tables, the 
flow entries must match the encapsulated packet as expected by the OpenFlow 
matching process.

* Port consistency: the ingress and egress processing of an OpenFlow port must 
be consistent with each other. In particular, if an OpenFlow packet is output 
on a port and generates a physical packet on a switch physical link, then if 
the reception by the switch of the same physical packet on the same link 
generates an OpenFlow packet on the same port, the OpenFlow packet must be 
identical.

## Flow Table

A flow table consists of flow entries.

Table 1: Main components of a flow entry in a flow table.

Each flow table entry (see Table 1) contains:

* match fields: to match against packets. These consist of the ingress port and 
packet headers, and optionally other pipeline fields such as metadata specified 
by a previous table.
* priority: matching precedence of the flow entry.
* counters: updated when packets are matched.
* instructions: to modify the action set or pipeline processing.
* timeouts: maximum amount of time or idle time before flow is expired by the switch.
* cookie: opaque data value chosen by the controller. May be used by the controller 
to filter flow entries affected by flow statistics, flow modification and flow deletion 
requests. Not used when processing packets.
* flags: flags alter the way flow entries are managed, for example the flag OFPFF_SEND_FLOW_REM 
triggers flow removed messages for that flow entry.

A flow table entry is identified by its match fields and priority: the match fields 
and priority taken together identify a unique flow entry in a specific flow table. 
The flow entry that wildcards all fields (all fields omitted) and has priority equal 
to 0 is called the table-miss flow entry (see 5.4).

A flow entry instruction may contain actions to be performed on the packet at some 
point of the pipeline (see 5.12). The set-field action may specify some header fields 
to rewrite. Each flow table may not support every match field, every instruction, every 
action or every set-field defined by this specification, and different flow tables of 
the switch may not support the same subset. The table features request enable the controller 
to discover what each table supports (see 7.3.5.5).


