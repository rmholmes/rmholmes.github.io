---
title: "Tropical Instability Waves and Vertical Mixing"
permalink: /projects/TIW_Mixing
author_profile: true
---

{% include base_path %}

## Background

The small-scale turbulent mixing of heat is an important component of
the Sea Surface Temperature (SST) budget in the tropical Pacific, and
thus is crucial to a range of processes important for global climate,
such as the El-Nino Southern Oscillation. Modulations in the levels of
turbulent in the upper EUC of the tropical Pacific have been observed
on a range of time scales associated with intraseasonal Kelvin waves,
the Madden-Julian oscillation and TIWs. Understanding what drives
these modulations is crucial to our understanding of the SST budget.

The modulation of turbulence by TIWs has only recently been observed
(Lien et. al. (2008) GRL 35, L24607, Moum et. al. (2009) Nat. Geosci.,
2, 761–765, Inoue et. al. (2012) J. Geophys. Res., 117, C10009). These
observations showed a modulation in the rate of turbulent kinetic
energy dissipation with TIW phase, with the strongest turbulence
occurring during the transition from northward to southward TIW flow,
or leading into the TIW warm phase. Accompanying the modulation in
turbulence was a modulation in the reduced shear squared in the upper
EUC. The reduced shear squared is similar to the Richardson number in
that it indicates how unstable a flow is to Kelvin-Helmholtz shear
instability. For negative values of the reduced shear squared the
stratification is strong enough to suppress instability, while for
positive values the shear dominants and shear instability can grow.

## Are modulations in Zonal Shear, Meridional Shear or Stratification
   responsible?

Using a regional ocean model of the equatorial Pacific, we examined
the modulations of the reduced shear squared with TIW phase. Our model
contains strong variations in the reduced shear squared (see Fig. 1g)
in the upper EUC (between ~120m and ~40m), with accompanying strong
variations in the vertical diffusivity parameterized using the KPP
mixing scheme (not shown). These variations are dominantly due to
variations in the EUC zonal shear (Fig. 1d), with variations in
stratification playing a roll (Fig. 1c) and variations in TIW
meridional shear being relatively minor (Fig. 1e). Thus the results
from our model suggest that modulation of turbulence in the upper EUC
with TIW phase is associated with variations in the EUC shear.


Figure 1: Equatorial Depth-Longitude slice of (a) Temperature, (b)
Meridional Velocity, (c) Stratification, (d) zonal shear, (e)
meridional shear, (f) meridional diffluence and (g) reduced shear
squared from a ROMS model of the equatorial Pacific. The gray solid
line indicated the EUC core and the green line indicated the KPP mixed
layer depth.

## How do TIWs modify EUC shear?

To investigate how TIWs are able to modify the EUC shear, I performed
a Lagrangian budget of zonal shear du/dz. The zonal shear following a
Lagrangian particle obeys


I.e. the zonal shear can change due to horizontal vortex stretching
(term 1 on the RHS), vortex tilting of vertical vorticity (term 2),
the baroclinic torque (term 3) and frictional processes (term 4). I
examined this budget along a set of Lagrangian particles advected
online in the simulations that entered the patch of high reduced shear
squared near 140W in Fig. 1.  The results showed that the dominant
term causing an increase in the magnitude of the zonal shear was the
vortex stretching term. Further analysis showed that TIW meridional
velocities result in a modulation of meridional diffluence dv/dy that
then acts on the EUC shear through horizontal vortex stretching. The
physics of this mechanism are summarized in Fig. 2.

A schematic showing how variations in TIW driven meridional diffluence
dv/dy (red arrows) can drive variations in the magnitude of the EUC
shear (indicated by the black spirals) resulting in phases of enhanced
and reduced turbulence (indicated by the small blue spirals) along the
Equator.

## What is the total (rectified) effect of this modulation on the
turbulent heat flux?

To quantify the total rectifying effect of the TIW driven modulations
on the turbulent heat flux averaged over a TIW wave period, I
performed a number of simulations using a simple 1D mixing model of
the upper EUC driven by periodically varying TIW strain dv/dy. By
comparing simulations with and without the TIW forcing, I showed that
adding the TIW forcing resulted in an increase in the average
turbulent heat flux by up to 30%. The amount of increase was dependent
on the parameterization scheme used for shear driven interior mixing,
with potential implications for the role of TIWs in the SST budget of
ocean models using different parametrization schemes.

For more information, see my article in the Journal of Physical
Oceanography: The Modulation of Equatorial Turbulence by Tropical
Instability Waves in a Regional Ocean Model

