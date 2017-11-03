# TCP-Simulation-model
A simple TCP flow model with packets sent to a queue

A TCP flow that demonstrates slow start and congestion control when flow packets that are
enqueued into a finite buffer are dropped due to the low service rate of the outgoing port.
It means that packets are not removed from the queue as fast as the flow generates and
enqueues packets. See how congestion control is invoked and the evolution of the congestion window.

Shows the evolution of congestion window against time in rtt
<rtt, cwnd>
and also prints out the packets dropped, buffer occupied, and ssthresh parameters.
Run as: python tcp-model.py
