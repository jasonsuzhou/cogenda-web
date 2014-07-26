<div class="box" >
{% markdown2 %}

Technical Support Center
------------------------

Any questions? [Send us an email](mailto:support@cogenda.com).

Technical support is provided via electronic mail solely. When contacting the support team, please provide us with the following information:

 * Detailed description of the problem
 * Version of the software you are using
 * Your operating system version (9x, NT, 2000, XP)

You can send your message to our support team with your bug reports or your ideas regarding software improvements (functionality, new features, etc.). All errors found will be corrected as soon as possible and we'll work hard to improve our software according your ideas and suggestions.

Before contacting the support team, please take a moment to browse through our Frequently Asked Questions page below - you may find the answer you're looking for is nearer than you think!

For your convenience, we try to provide as much support information as we can on our website. If you can't find the information you need on our site, please contact us by email. We'll always try to give you fast, courteous and competent answers.

{% endmarkdown2 %}
</div>


<div class="box" >
{% markdown2 %}

Frequently Asked Questions
------------------------
<p />
 
###### How did you made your simulator so fast?
There is no black magic. The Genius device simulator is designed to take advantage of parallel computers. Parallel computation have been widely used in scientific computation for almost 50 years. Traditionally it has been regarded as expensive technology. However, as fast microprocessors become commodities, cluster computers are now very affordable. For slightly over USD 10,000, one can have a 32-core cluster operating at stunning speed.

However, using a parallel computer does not automatically provides speed enhancement. The simulator program must be written in specific ways to take advantage of the parallel computation power. Writing parallel code is tricky, and it is even trickier to convert old serial code to parallel ones. As a result, we at Cogenda chose to start a fresh TCAD simulator, with parallelism designed into its core.

In our tests, our new design scales up very well as one adds in more processors. With 32 processor cores, we consistently get nearly 10 times speed up in simulations on large problems.

###### How is your parallel simulator different from the "multi-thread" simulators in the market?
Parallel computers come in a few different flavor. One popular type is the shared-memory computers, which usually come in the form of multi-core processors and multiple processors on the same main board.In this computing model, program runs in a few processors (cores) in parallel, but shares the same memory space. Most "multi-threaded" or "multi-core enabled" TCAD simulators fall in this shared-memory category. The shared memory model provides enhanced performance and has low processor-to-processor communication delay. However, in today's multi-core processors, memory bandwidth is the major bottle-neck to the performance of parallel computation. As a result, shared memory computation does not scale-up very well in practice.

Another parallel computation model is the distributed model, where programs work cooperatively in (logically) separate memory spaces. It is possible to span the system on a few separate computers in a cluster, so that the programs are not limited by the memory bandwidth in a single computer. Genius is based on this distributed computing model. Our test system consists of 4 computers, each having two quad-core processors. The 4 computers are wired-up with a high-speed infini-band interconnnection. We have observed very good scaling behavior, and see no problem extending the performance gain with larger clusters.

###### Is Genius compatible with X or Y device simulator?
Genius is a complete new design and new implementation. It is not related to any commercial device simulator. The syntax of Genius input file is therefore not compactible with them. However, it is relatively straightforward to convert the input deck of the Pisces device simulator, and commercial software based on Pisce, to the syntax of Genius input file. Genius can import device structures saved in Technology Interchange Format (TIF), adding to its interoperability with other popular commercial simulators.

Under what terms is Genius licensed?
Genius is available under a commercial license agreement, and is distributed in binary form. There is also an open-source edition of Genius released under GPL. You may download the source code in the open-source section.

{% endmarkdown2 %}
</div>
