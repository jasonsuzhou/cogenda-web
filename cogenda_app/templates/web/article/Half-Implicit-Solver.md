<div class="box" >

{% markdown2 %}
A Family of Fast TCAD Solvers
-----------

At this year's [SISPAD](http://www.sispad.org) (Denver, CO, 5-7 Sept.), 
Cogenda will present a paper on its new generation of TCAD device solver. 
This fast solver still solves the full TCAD equations (Schokley equations),
preserving the physical accuracy of TCAD.

With an improved "half-implicit" algorithm, the fast solver
provides 5 to 10 times acceleration when compared to
Cogenda's traditional solver, which had been the fastest in the industry.

<img src="/static/images/stories/hiddm/hiddm_speed.jpg" width="480"/> <br />
Fig-1. Comparison of simulation speed of the traditional and the fast solver,
on an 8-core workstation. Simulation speed of other TCAD tools, as reported 
in literature, are plotted as well. They are not simulated on the same hardware, though.

It is especially suitable for large-scale device/circuit simulation tasks,
which were previously outright impossible or prohibitively expensive with
traditional solvers.


### <a name="LargestTCAD"></a> World's Largest TCAD Simulation
At a glance:

  * D-Flipflop with 24 transistors;
  * 1.67 million mesh nodes, 10.7 milllion mesh elements;
  * computed on 4 nodes, dual Xeon X5670 CPUs, 48 cores in total, requires 190G RAM;
  * completed in 268 minutes (4.5 hours);

Enpowered by the fast TCAD solver, we can't resist the temptation to 
claim the largest TCAD simulation in the world.
A D-flipflop circuit consisting of 24 transistors is chosen for this test.

<img src="/static/images/stories/hiddm/dff_mask.jpg" width="360"/> <br />
Fig-2 Mask layout of the D-Flipflop circuit.

The 3D model is built with [Gds2Mesh]({{NICEDOG_BASE_URL}}/article/Gds2mesh)
using a 90nm process rule.
It contains 1,673,519 mesh nodes, and 10,659,866 tetrahedral mesh elements.

Due to the adaptive meshing, the majority of the mesh nodes are in the active region,
despite the much large substrate region.

<img src="/static/images/stories/hiddm/dff_3d.jpg" width="560"/> <br />
Fig-3 (left) 3D Model of the D-Flipflop circuit. 
(right) Zoom-in view of the active region of the circuit.

The single-event upset (SEU) of the circuit is simulated, with a 95 MeV Cl<sup>+</sup> ion
striking on the device. One can see from Fig-4 that the ion causes the data stored in the
flipflop to change.


<img src="/static/images/stories/hiddm/dff_flip_wave.jpg" width="360"/> <br />
Fig-4 Transient voltage waveform of the output node of the flipflop circuit.

### What's next

While developing a "silver-bullet" device simulator that is fast and efficient in 
all cases might not be possible,
specialized solvers, each designed for specific problem, are much more feasible.
The half-implicit solver, decribed above, is especially suitable for transient probems
for CMOS devices.
Specialized solvers for other problems are under development at Cogenda,
as part of our commitment to continuous innovations in TCAD technology.

{% endmarkdown2 %}
</div>

