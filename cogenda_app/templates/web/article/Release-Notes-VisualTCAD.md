<div class="box" >
{% markdown2 %}

<a name="174-14"></a> VisualTCAD 1.7.4-14
-------------------------------------
##### 2013.3.19

This is a bug-fix release. 

#### Genius Device Simulator
   - Lag-LU preconditioner is now stable.
   - Fix slowness mixed-mode simulation due to insufficient memory allocation.
   - Fix a bug in synchronizing the volume of mesh elements across processors.
   - Several fixes to protect mathematical functions from overflow/underflow.
   - Better support importing Medici TIF file.
   - Operation-point solution is saved to '*.op.dat' to avoid overwriting other solution files.

#### VisualTCAD GUI
   - Support importing TIF file produced by Suprem4/TSuprem4 in 2D Device drawing, for re-meshing.
   - Fix mesh generator crash due to floating-point number rounding error.
   - Avoid crashing when reading malformed TIF3D mesh file.
   - Support reading user-defined profile in TIF3D file.

#### Gds2mesh
   - Allow user to define custom field variables, and specify their units.
   - Each physical volume in exported GDML now has a distinct name.
   - The material of the "World" physical volume in exported GDML is changed to Vacuum.
   - Remove degenerate polygons in GDSII layout.

</div>

<div class="box" >
<a name="174-10"></a> VisualTCAD 1.7.4-10
-------------------------------------
##### 2012.11.27

This is a bug-fix release. 

#### Genius Device Simulator
   - Display units of physical quantities in vtk output files.
   - Allow user to set the convergence criteria of operation-point solution.
   - Fix occasional crash due to uninitialized variable in external circuit solver.
   - Fix boundary detection when seconductor region is in contact with many insulator regions.

#### VisualTCAD GUI
   - Improve font display on some Linux systems.
   - Improve compatibility with TMA TIF mesh format.
   - Display units of physical quantities in vtk output files.
   - Added support for dose-rate radiation effect analysis.
   - Fix a bug that causes button not being functional on some Linux platform.
   - Fix a bug that leads to crash when a vtk/cgns file contains unrecognized material.

{% endmarkdown2 %}
</div>

<div class="box" >
{% markdown2 %}

<a name="174-8"></a> VisualTCAD 1.7.4-8
-------------------------------------
##### 2012.10.08

This is a bug-fix release. 

#### Genius Device Simulator
   - Experimental option to use Lag-LU preconditioner, improves the speed of DDM solver by up to 2x.
   - Improves convergence when a mesh edge has negative FVM cross-section area.
   - Fix the incomplete implementation of the resistive-metal/insulator interface in small-signal AC simulation.
   - Fix an error in mole fraction setting in parallel simulation.
   - Fix numerical trunction error in ray-tracing optics, when light source is far from the device.

#### GSeat Particle Simulator
   - Enabled elastic hadron processes for alpha particle and general ions.
   - Fix crashing error when HDF5 output filename is not supplied by user.

#### VisualTCAD GUI
   - Fix linear mole fraction profile seetting in GUI.
   - Misc. fixes in AC simulation setup in GUI.
   - Fix waveform display in voltage/current source setings.

{% endmarkdown2 %}
</div>

<div class="box" >
{% markdown2 %}

<a name="174-5"></a> VisualTCAD 1.7.4-5
-------------------------------------
##### 2012.08.02

This is a bug-fix release. 

#### Supported Platforms
   - Experimental support for Debian 7 (Wheezy/sid) x86_64 Linux platform. 
     It is built and tested on Ubuntu 12.04LTS.

#### Genius Device Simulator
   - Fix synchronization of the boundary-proximity flag of mesh nodes, which affects surface mobility calculation.
   - Improves mesh element truncation scheme, reduces fluctuation when mesh elements near interfaces have poor quality.
   - Fix mesh element truncation rule mismatch. The same rule must be used in semiconductor and metal regions.
   - Improves convergence when EQF is used as parallel E-field in mobility calculation.
   - Fix importing TIF mesh file produced by the MEDICI program.

#### VisualTCAD GUI
   - Support syntax-highlighting in scripting window in VisualFab.
   - Fix specification of mole fraction of two compound semiconductor materials.
   - Miscellaneous fixes.

{% endmarkdown2 %}
</div>


<div class="box" >

{% markdown2 %}
<a name="174-3"></a> VisualTCAD 1.7.4-3
-------------------------------------
##### 2012.07.10

This is a bug-fix release.

#### Genius Device Simulator
   - Fix default direct linear solver in serial mode.
   - Fix unit of dopant concentration in RegionSet command.

#### VisualTCAD GUI
   - Fix a bug in principal optical axes setting for 2D structure.
   - Fix a bug in netlist topology calculation in schematic editor.
   - Minor fixes in Windows installer, improve support for Flexlm.

{% endmarkdown2 %}
</div>


<div class="box" >
{% markdown2 %}

<a name="174-2"></a> VisualTCAD 1.7.4-2
-------------------------------------
##### 2012.06.24

This is a bug-fix release, with some user manual updates.

#### Genius Device Simulator
   - General
     - Fix large memory consumption during importing the carrier generation profile
       data due to high energy particle (introduced in 1.7.4-1).
     - Fix time step control at negative pulse edge (introducted in 1.7.4-1).
     - If the Metis mesh partitioner failed, fall back to a simple partitioner.
   - Material Models
     - Fix CIGS bandgap data
     - Fix an instability in the mobility model of AlGaAs

#### Gds2mesh Modeller
  - Fix a bug in handling long-narrow 3D objects.

{% endmarkdown2 %}
</div>


<div class="box" >
{% markdown2 %}

<a name="174-1"></a> VisualTCAD 1.7.4-1
-------------------------------------
##### 2012.06.03

New features. FlexLM floating license manager is used on all platforms.

#### Genius Device Simulator
  - Solver and Models
    - Optical anti-reflection coating at surfaces of the device.
    - Complete implementation of gate direct tunneling current.
    - Support R-C transmission line as the external circuit at electrodes.
    - Significant reduction in memory footprint.
  - General improvements
    - Specify region name with regular expressions (in PMI and MODEL commands).
    - The equation residuals are now displayed in meaningful physical units. 
    - More flexible specification of linear solver and preconditioners in Half-implicit solver.
    - General convergence improvements.
    - Dedicated optimized version on RHEL6 system.
  - Bug fixes
    - Discontinuity in Hypertang mobility model.
    - Rare bug in ray-tracing.
    - Misc. bugs that affects convergence in rare cases.

#### GSeat Particle Simulator
  - Upgrade to Geant4.9.5
  - Fixed a geometry calculation bug in Geant4, which affects particle tracking in structures with complex geometry.
  - Improved speed of particle tracking in complex geometry.
  - Support more space-efficient HDF5 data format.

#### VisualTCAD/VisualFab/VisualParticle GUI
  - Support AC small-signal simulation in GUI.
    - Capacitance-Voltage sweep analysis.
    - Capacitance-Frequency sweep analysis.
  - Much improved speed in loading large device structure for visualization.
  - Improved display of device regions in visualization module.
  - Support updated GSeat(HDF5) and TIF3D v1.2 data formats.
  - Revamp wafer-state inspector and simulation manager modules and other major improvements in VisualFab.
  - Misc. bug fixes.

#### Gds2mesh Modeller
  - Much improved speed in generating 3D geometry objects.
  - Use unique material reference in GDML output format.
  - Support for TIF3D v1.2 data format.

{% endmarkdown2 %}
</div>



<div class="box" >
{% markdown2 %}

<a name="173-2"></a> VisualTCAD 1.7.3-2
-------------------------------------
##### 2012.03.12

Improvements and bug fixes.

#### VisualTCAD/VisualFab/VisualParticle GUI
  - New window manager
    - Group related windows together.
    - Show/hide/close individual or group of windows.
  - Improved XY-plot module
    - Display legends on the graph.
    - Option to refresh plots when underlying data changes.
  - Bug fixes
    - When editing plot axis scale, axis properties may get applied on wrong axis.
    - Improved handling of extremely small 2D polygons.

#### Gds2mesh Modeller

  - Improved GDML export. Build the geometry with minimal number of faces.
  - Support custom doping profile and mesh-size control in python process rules.
  - Bug fixes
    - Fixed a buffer overflow that causes segfault.
    - Improved handling of extremely small 2D polygons.
    - Fixed polygon offsetting algorithm.

#### Genius Device Simulator
  - Solvers and Models
    - Support simulation in cylindrical coordinates.
    - Support custom definition of the track radius of (high-energy) particles.
    - Support distributed contact resistance.
  - General improvements
    - More efficient mesh importer for TIF data format.
    - More efficient assembly of equations at internal interfaces.
  - Bug fixes
    - Output of current at metal boundaries in half-implicit simulation.
    - Optical boundary condition settings added to .cgns files.
    - Fixed linear solver setting in AC simulation.
    - Proper warning message when 
      - Optical modulation envelop is incorrect.
      - Region with no material assignment.
      - Error in reading optical spectrum data.

#### GSeat Particle Simulator

  - Use G4ScreenedNuclearRecoil model by default
  - Adjust the limit to the track step length, for better resolution of the final stage of ion track.
 
{% endmarkdown2 %}
</div>

<div class="box" >

{% markdown2 %}
<a name="173"></a> VisualTCAD 1.7.3
-------------------------------------
##### 2012.01.01

New feature and bug fixes.

#### VisualTCAD/VisualFab/VisualParticle GUI

  - VisualFab is mature enough to enter the standard release.
  - Ray-tracing simulation supported in GUI
    - Setting up principal axis, light source and lenses in GUI.
    - Setting up modulation, polarization, power spectrum in GUI.
    - Self-consistent device/optics simulation supported in GUI.
  - Improved XY-plot module
    - More flexible ways to adding multiple curves to plot.
    - Axis settings saved to .plt files.
    - Extract and export data from plots.
  - Slicing function for visualizing internal variables of 3D structures.
  - General improvements
    - Use more than one processors when loading large mesh files.
    - Editing subwindow and document properties.
    - More debug/information message in log console.
    - Support Genius built with the hydra MPI process manager.
    - Expose more numerical solver options for device and circuit simulations.
  - Bug fixes
    - On Windows, loading large mesh (taking >15 seconds) used to fail.
    - In VisualParticle, setting seed number of random number generator in GUI not working.
    - In Device2D Editor, changing ruler items causes mesh to be destroyed.
    - Some default settings are not effective when VisualTCAD is used for the first time.
 
#### Genius Device Simulator

  - Stable half-implicit transient-mode solvers.
    - Proprietary correction algorithm, significantly reducing simulation error.
    - Half-implicit DDM1 and DDM2 solver are fully supported.
    - Optimized time-step control.

  - Physics and Models
    - Removed bogus surface mobility degradation at very high E-field in Lucent mobility model.
    - New material models: ZnO, CdS and CIGS.

  - General improvements:
    - Improved parallel efficiency in importing and constructing large mesh structures.
    - Expose performance profiling option to end users.
    - Preliminary support AIX operating system.
    - Upgrade to MPICH2 1.4 and MVAPICH2 1.7, switch to Hydra process manager.
    - Output gate current when applicable.
    - More warning messages when mesh quality is poor.
    - More flexible syntax for input file, list values are supported.
    - More flexible doping profile placement commands in input file.

  - Bug fixes:
    - Various import failures of mesh in DF-ISE format.
    - Buffer of some material parameters not updated after PMI commands.

#### GSeat Particle Simulator

  - Recover bias factor of cross-section (for neutron/proton) after reaction occurs.
  - Switch to a better random number generation and seeding.
  - Filtering by material regions in output file. 
  - More particle and material information stored in output files.

#### Gds2mesh Modeller

  - More efficient export of model in GDML format, producing smaller-size output file.
  - Support custom-defined doping profile defined in Python script.
  - Support path objects in GDSII files.
  - GUI allows user to select top-level structures in GDSII files.
  - Improved efficiency in constructing 3D objects.
  - Fix a bug in handling 3D objects with complex shape and positions.
  - Fix a bug in doping profile calculation.


{% endmarkdown2 %}
</div>


<div class="box" >
{% markdown2 %}

Older Releases
-------------------------------------
[Year 2011 and older](./Release-Notes-2011)

{% endmarkdown2 %}
</div>
