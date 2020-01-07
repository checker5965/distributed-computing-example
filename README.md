# distributed-computing-example
The following socket program showcases networking communication in managing distributed systems.

The Server side program will be running simultaneously at three different PCs.

Let L = (x1, x2, . . . , x10) be a list of 10 integers.

Each server will be holding a copy of this list, say Li = (x1, x2, . . . , x10), where
i = 1, 2, 3.

Each server will be listening, and accepting requests from different clients, who
want to shuffle any two entries in the L that is presented to them by the
accepting server.

The task at hand is that eventually, each server should hold the same copy of L
even after executing the requests that they have received from different clients.

In principle, this is possible if the servers are able to order these requests using
the time stamp that they are carrying.

The following socket program implements the above functionality, along with functionality to prioritize requests by a certain IP over others.
