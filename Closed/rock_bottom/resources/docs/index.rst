.. _ddddr:

Rock Bottom
***********

:Author:
 J. Gonzalez <javierg@udel.edu>

.. toctree::
   :maxdepth: 1

   release_notes
   `Generated doxygen for this project <../../doxygen/rock_bottom/index.html>`_


Introduction
============

Don't hit rock bottom!!!

What you have here is a set of tools to work with IceTop.  It includes
modules to reconstruct events, but it might include other things. The
intention is to make it extremely modular, allowing one to replace and
combine the LDF, the shower front shape and various variance models in
a transparent manner. It happened because it was easier to start from
scratch rather than modify laputop, but it has also been a nice way to
learn icetray/gulliver stuff.

Most probably many of the things in here can be replaced by standard
classes from gulliver. This could be true, for example, the I3TopTrivialParametrization,
or the I3TopLeanFitter classes.

Guidelines:
===========

- Reconstruction is separate from pulse/dom/tank/event selection.
- Event selection is separate from pulse/dom/tank selection.
- Likelihood functions _make_no_decisions_.
- To the extent possible, the code should be SLC/HLC agnostic (both handled the same way).
- No 'global' corrections are applied inside the likelihood. For example,
  these can be done by another module or at least factored out (they are likely to change):
    a.- s_125 -> energy conversion
    b.- global pressure correction
- Flags indicating tank/DOM status should be _explictly_ stored in the event interface.
  In other words: we want to keep track of which tanks were used by the fitting module
- Some things are swapable.
  Common concepts that we could change often include:
    a.- LDF and its fluctuations (should they go together?, separate?).
    b.- Shower front shape (particle arrival time and its fluctuations).
    c.- Trigger/saturation probabilities.
    d.- Snow correction.
  The interface for these services is up for discussion.
- If possible, the likelihood functions should be separate but easily combined.

Comments:
=========

- I made an arbitrary separation between 'parameters' and 'constants'.
  Clearly, r_ref is a constant. All the others are not so clear.
  For example, with the NKG parametrization one could fit the value of
  the Moliere radius or the two exponents alpha and beta. Still, these
  are 'constant'. In principle, they should not vary once the atmospheric
  conditions and geometry of the shower is set.
- The LDF classes provide the mean value of the LDF as well as an estimate
  of its variance (actually standard deviation, should one provide both?).
  The LDF chi2 uses this but the likelihood doesn't.
- The LDF classes provide a method to set first-guess values for the parameters.
  Otherwise, I would have to know about the details of the parametrization
  inside the seed service. As it is, the seed service doesn't know anything
  about the implementation of the LDF. It does need to know about
  I3ParameterMap. I hope this is generic enough.
- Note that one does not control whether a parameter is fixed here.
  Maybe this is not very intuitive.

