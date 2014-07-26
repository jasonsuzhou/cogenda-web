<div class="box" >
{% markdown2 %}

<a name="172-5"></a> 
VisualTCAD 1.7.2-5
-------------------------------------
##### 2011.09.29

New feature and bug fixes.

#### VisualParticle (New Product)

 - GSeat: MonteCarlo Particle Simulator based on GEANT4, for simulation of single-event effects.
 - VisualParticle: Graphical Interface to GSeat.
 
#### Genius Device Simulator

 - New features:
   - Experimental support for half-implicit transient-mode solvers,
     offers 5x faster simulation speed.
   - Ray-tracing optics that supports lens and mirrors.
 - Improvements and bug fixes:
   - Solvers and Algorithms
     - Better cell truncation at boundary element, improved convergence.
     - Fine-tuned ASM linear pre-conditioners, improved convergence.
     - Improved curve-tracing algorithms for better detection of snap-back points.
     - Support Interconnect in circuit/device mixed-mode simulation.
     - Faster searching algorithm for tunneling partner node 
         at semiconductor/insulator boundaries.
     - More accurate integration algorithm for transient simulation with 
         optical- or particle-induced carrier generation.
   - Physical models
     - Free-carrier optical absorption is supported.
     - Fixed a parameter in Philips mobility model.
     - Fixed materials parameter of Ti and Tungsten.
   - General 
     - Extended syntax: list values are supported in options.
     - Updated data format for importing energy deposition profile from 
         GSeat particle simulation.
     - Calculates and outputs capacitances of all electrodes in AC simulation.
     - Import mesh file of the original Suprem4GS data format.

#### VisualTCAD

 - Defining interconnects in simulation control.
 - Scripting support in visualization module.
 - Warning and information messages displayed in log console window.
 - Fix a bug in constant current sources.

#### Gds2Mesh

 - Added parameters to control the density of doping profile rays.
 - Fixed several bugs related to regions with holes.
 - Fixed a bug in GDML mesh export.
 - Calculate doping concentration only in semiconductor regions.
 - Support Box object in GDSII mask file.
 - Stylized preview of mask graphs.

{% endmarkdown2 %}
</div>

<div class="box" >
{% markdown2 %}

<a name="172-3"></a> VisualTCAD 1.7.2-3
-------------------------------------
##### 2011.06.29

New feature and bug fixes.

#### Genius Device Simulator

 - Adaptive pseudo-time steps, allows pseudo-time analysis to converge in fewer steps.
 - Improves BDF2 time-discretization, prevents inaccurate time-derivative estimation
   when carrier concentration is rapidly decreasing.
 - Improves efficiency of importing radiation particle trajectory.
 - More robust implementation of ray-element intersection calculation in ray-tracing optics.
 - Fixes importing of boundary condition in CGNS.

#### VisualTCAD
 - Editing user-defined circuit symbols and components.
 - Define mesh-size-control boxes, in addition to control lines.

{% endmarkdown2 %}
</div>


<div class="box" >

{% markdown2 %}
<a name="172"></a> VisualTCAD 1.7.2
-------------------------------------
##### 2011.05.13

New features.

#### Genius Device Simulator

 - Proper truncation of triangle and tetrahedron with obtuse angles.
 - Small-signal AC analysis for devices with resistive metal regions.
 - Pseudo-time analysis mode for device simulation. Devices with floating regions,
   or other difficult-to-converge problems, have much improved convergence property
   with pseudo-time method. Iterative linear solvers can be used instead of direct
   solvers, drastically saving memory.
 - Re-order circuit variables in vector and Jacobian matrix, improves convergence.
 - Gmin-ramping and Source-ramping in device/circuit mixed simulation.
 - Updated build system on Linux, with updated and optimized numerical libraries.
   Requires RHEL5 and above, support for RHEL4.x stopped.
 - Fixed bugs related to distributed mesh.

#### VisualTCAD
 - More complete support for simulation control options, including
   Gmin-ramping/Source-ramping in device/circuit mixed simulation.
 - Create and edit custom circuit component libraries.
 - Edit mesh-size-constraint items in device drawings.
 - Improvements to the setting profile manager.

#### Gds2Mesh
 - More mask generation options for SRAM.
 - Fixed well contact doping in SRAM example.

{% endmarkdown2 %}
</div>


<div class="box" >

{% markdown2 %}
<a name="171-4"></a> VisualTCAD 1.7.1-4
-------------------------------------
##### 2011.03.19

Bug fixes.

#### Genius Device Simulator

 - Fix crash under Windows due to read violation.
 - Update 3D mesh refine example (PN_Diode/pn_refine.inp).

#### Gds2Mesh
 
 - Fix excessive message box when job finishes.

{% endmarkdown2 %}
</div>

<div class="box" >

{% markdown2 %}
<a name="171-3"></a> VisualTCAD 1.7.1-3
-------------------------------------
##### 2011.02.28

Bug fixes. 

#### Genius Device Simulator

 - Option to adjust voltage reference used in potential damping.
 - Improve parsing of large numbers in input files.

#### Gds2Mesh
 
 - Allow multiple and intersecting fill-objects.

#### VisualTCAD
 
 - Improve formatting of large numbers.

{% endmarkdown2 %}
</div>

<div class="box" >

{% markdown2 %}
<a name="171-2"></a> VisualTCAD 1.7.1-2
-------------------------------------
##### 2011.02.28

Bug fixes with some new features.

#### Genius Device Simulator

 - Distributed mesh storage, significant memory usage reduction in parallel simulation.
 - Added GaN and AlGaN material models.
 - Added HEMT example.
 - Fix current direction calculation at heterojunction.

#### Gds2Mesh
 
 - Fix typo in GUI that breaks polygon item in simple masks. 

{% endmarkdown2 %}
</div>


<div class="box" >

{% markdown2 %}
<a name="171-1"></a> VisualTCAD 1.7.1-1
-------------------------------------
##### 2011.02.14

Bug fixes with some new features.

#### Genius Device Simulator

 - Waveform modulated (in time) by an envelope for light and irradiation sources.
 - Adjust linear solver parameters for better stability
 - Effective surface E-field for mobility calculation is turned-on by default.
 - Exporting mesh and solution in DF-ISE format.
 - Fix Jacobian matrix for some displacement current components.
 - Fix error in importing 2D elements in DF-ISE file.

#### Gds2Mesh
 
 - A simple GUI.
 - Updated Python interface and documentation.

#### VisualTCAD GUI

 - minor fixes

{% endmarkdown2 %}
</div>


<div class="box" >
{% markdown2 %}

<a name="171"></a> VisualTCAD 1.7.1
-------------------------------------
##### 2011.01.06

New Features and enhancements.

#### Genius Device Simulator

 - Added support for Windows 64bit platform.
 - Added support for incomplete-ionization of dopant impurities.
 - More efficient data structure to store solution data.
 - Overhaul of the storage of user-defined solution variables.
 - Load material optical parameters from data file.
 - Improve support for quadrilateral mesh element with high aspect ratio.
 - Fix bug in calculation of carrier quasi-Fermi-level when Bandgap narrowing is present.

#### Gds2Mesh

 - Fix bug in doping profiles calculation.

#### VisualTCAD GUI

 - Improves the editing of configuration profiles.
 - Improves the mesh quality near region boundary.
 
{% endmarkdown2 %}
</div>

<div class="box" >
{% markdown2 %}

<a name="170-2"></a> VisualTCAD 1.7.0-2
-------------------------------------
##### 2010.11.25

Enhancements and Bug-fixes to the [1.7.0-1](#170-1) release.

#### Genius Device Simulator

 - Added support for lattice heating and energy-balance solvers in resistive metal regions.
 - Turn off experimental triangle truncation algorithm, which proves to causes instability.
 - Fix ray-tracing crash when the intensity of one polarization vanishes at interface.
 - Speed optimization at boundaries.
 - Overhaul of the storage of solution variables.

#### Gds2Mesh

 - Fix bug in placing doping profiles using a mask with holes.

#### VisualTCAD GUI

 - Allow users to edit and switch configuration profiles.
 - Improves to import of doping profile in Device2D.
 - Synchronize selection between column view and the main spreadsheet.
 
{% endmarkdown2 %}
</div>

<div class="box" >

{% markdown2 %}
<a name="163-1"></a> VisualTCAD 1.6.3-1
-------------------------------------
##### 2010.11.25

Maintenance release for the [1.6.x](#163) branch.

#### Genius Device Simulator

 - Fix ray-tracing crash when the intensity of one polarization vanishes at interface

#### VisualTCAD GUI
 - Incorporate new GUI features of [1.7.0-2](#170-2).

{% endmarkdown2 %}
</div>


<div class="box" >

{% markdown2 %}
<a name="163"></a> VisualTCAD 1.6.3
-------------------------------------
##### 2010.10.31

Maintenance release for the [1.6.x](#162-2) branch.

#### Genius Device Simulator

 - Fix boundary width when importing mesh file.
 - Improve stability of Sharfetter-Gummel discretization.

#### VisualTCAD GUI
 - Incorporate new GUI features of [1.7.0-1](#170-1) and [1.7.0](#170).

{% endmarkdown2 %}
</div>


<div class="box" >

{% markdown2 %}

<a name="170-1"></a> VisualTCAD 1.7.0-1 
-------------------------------------
##### 2010.10.31

Bug-fixes to the [1.7.0](#170) release.

#### Genius Device Simulator

 - Fix boundary width when importing mesh file.
 - Improve stability of Sharfetter-Gummel discretization.
 - Fix nearest boundary node searching.
 - Option to limit the maximum voltage ramp rate in transient simulation.
 - Save boundary label in CGNS even if it has no mesh node (yet).

#### VisualTCAD GUI

 - Fix python scripting in Win32.
 - Fix memory leaks in XY plot.

#### Gds2Mesh
 - Improve efficiency in calculating doping profiles.

{% endmarkdown2 %}
</div>

<div class="box" >
{% markdown2 %}

<a name="170"></a> VisualTCAD 1.7.0 
-------------------------------------
##### 2010.10.18

The 1.7.0 release contains many new features in the Genius simulator
and the VisualTCAD GUI.
A new product GDS2Mesh is released, and included in this version.

#### Genius Device Simulator

 - Support realistic metal regions that is resistive. 
   Resistive metal regions is allowed to be in contact with each
   other, circuit cells are constructed this way.
 - Major speed-up in simulating large structures. Loading a 100K node
   structure is almost 10 times faster, the matrix assembly step is
   almost 2x faster. The overall speed up for SRAM simulation is ~1.5x.
 - Experimental support for gate current (tunneling and hot carrier).
 - Support TIF3D mesh data format.

#### VisualTCAD GUI

New features in VisualTCAD includes:

 - Python scripting for automating common tasks in the following
modules: 
   - 2D device drawing, 
   - spreadsheet, 
   - XY plot. 
 - Saving/loading XY plots to disk.
 - Predefined palette for curve style/color in XY plots.
 - In 2D device drawing, import 1D/2D doping profile from file.
 - Support TIF3D mesh data format.
 - Visulization module:
   - Probe multiple variables in device.
   - Select/deselect multiple regions to filter
 

#### GDS2Mesh (New Product)
 Construct 3D TCAD model directly from GDSII mask layout.
 (included in the Linux package, but licensed separately).

{% endmarkdown2 %}
</div>

<div class="box" >
{% markdown2 %}

<a name="162-2"></a> VisualTCAD 1.6.2-2
-------------------------------------
##### 2010.08.30
 
Bug fixes:

 - Device 2D: correctly handle doping profile with zero height.

{% endmarkdown2 %}
</div>


<div class="box" >
{% markdown2 %}

<a name="162-1"></a> VisualTCAD 1.6.2-1
-------------------------------------
##### 2010.08.11

Bug fixes:

 - Mixed simulation: support numerical device with 32 pin (up from 7).
 - Improve pseudo color plot in visualization module.

{% endmarkdown2 %}
</div>

<div class="box" >
{% markdown2 %}

<a name="162"></a> VisualTCAD 1.6.2
-------------------------------------
##### 2010.08.02

#### VisualTCAD GUI
 - 2D Device Drawing :
   - Added "Ruler" tool, for measuring sizes of objects
   - Support setting background doping concentration and mole fraction of material ares.
   - Support placing mole fraction profile in device structure
   - Support "Opaque" rendering mode, which is faster over remote display.
   - Improves material selector
   - Improves mesh quality
 - Device Simulation:
   - Allow boundaries and contacts to have different width in the Z-direction.
   - Fix bugs related to impact ionization and band-to-band tunneling model parameters.
 - X-Y Plot:
   - Correctly handle negative values in log-scale plots
 - Visualization:
   - Support setting values of contour line

#### Genius Device Simulator

 - Performance optimizations
 - Bug fixes in heterojunction current, band-to-band tunneling models
 - Support AlN material


{% endmarkdown2 %}
</div>

<div class="box" >

{% markdown2 %}
<a name="161"></a> VisualTCAD 1.6.1
-------------------------------------
##### 2010.05.24


#### Genius Device Simulator

 - Fixes an error in calculating current at heterojunction
 - Improves convergence of AC small signal simulation
 - Fixes random crashes after simulation is completed
 - Add support for electron bean injection
 - Fixes minor problems in exporting CGNS and VTK
 - Report syntax error to log file, in addition to console
 - Fixes optical parameters of some III-V and II-VI materials
 - Fixes stdout/stderr buffer problem when using pythonw on windows.

#### VisualTCAD GUI

 - Support dongle license keys
 - Provides GUI in simplified Chinese language
 - Fixes memory leak when requesting log
 - Fixes excessive CPU usage when running long simulations
 - Improves user-interaction in the object list in device drawing tools
 - Check for duplicate region/profile names in device drawing
 - Improves the ramp-up sequence of device simulation
 - Fixes error in calculating simulation progress
 - Fixes crash when using VTK window under X-over-TCP platform


{% endmarkdown2 %}
</div>

<div class="box" >
{% markdown2 %}

<a name="160"></a> VisualTCAD 1.6.0
-------------------------------------
##### 2010.04.04

Public release with numerous bug fixes.

{% endmarkdown2 %}
</div>

<div class="box" >
{% markdown2 %}

<a name="160b"></a> VisualTCAD 1.6.0-beta
-------------------------------------
##### 2010.02.10

Test version released to distributors and selected customers.

{% endmarkdown2 %}
</div>
