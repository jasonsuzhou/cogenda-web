<div class="box" >

{% markdown2 %}

Applications
------------

Our simulators incorporate a wide range of physical models and materials, giving rise to numerous applications. On the other hand, the capability of handling large device/circuit structures and the unprecedented performance offered in Genius create new applications. We list a few examples of among the applications of Genius.

#### Single Event Upset in SRAM
##### [Brochure](/downloads/pubs/SRAM_SEU.pdf) | [Application Notes](#)

For serious TCAD study of SEU effects, a complete workflow is mandatory to handle the large amount of computation and data analysis work. 

A complete workflow is developed to study the effect of particle radiation in SRAM or other logic circuit cells.
With the precedented performance and the highly integrative work-flow, it is now possible to validate the SEU hardness of a circuit within days.
<img src="/static/images/seu_sram/flowchart_small.jpg" alt="" width="480" />

#### 3D SRAM Cell
A 3D SRAM structure is generated from the GDSII mask layouts, and its writing sequence simulated in Genius.
The model contains over 96,000 mesh nodes, and the entire write sequence is simulated in about 4 hours.

<object classid="clsid:d27cdb6e-ae6d-11cf-96b8-444553540000" codebase="http://download.macromedia.com/pub/shockwave/cabs/flash/swflash.cab#version=6,0,40,0" width="500" height="364"><param name="width" value="500" /><param name="height" value="364" /><param name="src" value="/static/media/genius/sram_write.swf" /><embed type="application/x-shockwave-flash" width="500" height="364" src="/static/media/genius/sram_write.swf"></embed></object> 


#### ESD Protection Devices
Electrostatic discharge is a common cause of IC failure. ESD protection circuits are usually placed near the I/O pads to guard the internal devices from ESD related damages. Since ESD is a high current event, ESD protection circuits should be able to sink high level of currents without being permanently damaged. Additionally, in CMOS IC, devices in the ESD protection should be compatible with the normal CMOS fabrication technology. The gate grounded NMOS (ggNMOS) transistor satisfies both requirements, and is a popular ESD protection device.

[Click here to download an application note on ESD Protection Devices.](../downloads/docs/an_esd.pdf)

#### 3D CMOS Inverter
With the continuous scaling of CMOS technology, the interaction between manufacturing processes and the device characteristics has increasingly become relevant to circuit designers, especially in the design of logic cell library. TCAD engineers are now called upon to simulate small logic circuit cells, preferably in 3-dimensional models.
There are a few alternative ways to simulate small logic circuit cells with TCAD tools. One "traditional" approach is circuit/device mixed simulation, in which one simulates each transistor in TCAD individually and use SPICE to connect the numerical devices. GENIUS is capable of this type of mixed-mode simulation.
However, since device simulations are decoupled, the device simulation has to be repeated a few times until the circuit simulator finds the right node voltages for the entire circuit. As a result, mixed-mode simulations are significantly slower. GENIUS offers an alternative method, in which the circuit cell is simulated as a whole in one TCAD model. We will go through the simulation steps, using a simple CMOS inverter as example in the following sections

[Click here to download an application note on 3D MOS Inverters.](../downloads/docs/an_inv.pdf)

#### Trapping Carriers
The carrier capture and emission at bound states within the bandgap of semiconductors is one of the important fundamental processes in semiconductor devices, and have enormous implications to the device performance. For example, Au dopants were intentionally introduced to BJT devices to reduce the carrier lifetime and improve high frequency performance. The surface states at the oxide/silicon interface has always been a critical issue for the performance and reliability of MOSFET devices. In this chapter, we will demonstrate the simulation of charge trapping related processes in PN diode and MOSFET devices, using the Genius device simulator.

[Click here to download an application note on Trapping Carriers.](/downloads/docs/an_trap.pdf)

{% endmarkdown2 %}
</div>

