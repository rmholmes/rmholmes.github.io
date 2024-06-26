---
title: "Abyssal Mixing at the Equator"
permalink: /projects/DeepEqMix
author_profile: true
---

{% include base_path %}

## Abyssal mixing near the equator: A microstructure turbulence study

In December 2014 I was invited to participate in a five-week research
cruise to the equatorial Pacific by Professor Jim Moum. Jim is a world
leader in making observations of small-scale turbulent mixing using a
number of cutting-edge microstructure turbulence instruments developed
by his group at Oregon State University. The research cruise aboard
the R/V Oceanus (Figure 1) was aimed at measuring turbulence both in
the upper ocean on the equator, but also at testing a new instrument
for making measurements of mixing in the abyssal ocean. The abyssal
measurements were made using a CTD Chi-pod instrument (see Fig. 2)
that measures temperature variability at very high frequency as the
instrument is lowered into the deep ocean.

<p align="center">
  <img src="/files/Oceanus.jpg" alt="R/V Oceanus" style="width:30%;
  text-align:center"/>
  <figcaption>Figure 1: The R/V Oceanus.</figcaption>
</p>

<p align="center">
  <img src="/files/CTDLAB.png" alt="CTD Chipod" style="width:35%;
  text-align:center"/>
  <figcaption>Figure 2: The Chi-pod instrument (blue circles) attached to a CTD cage
ready for deployment off the side of the R/V Oceanus. The sensors on
the top and bottom of the CTD package measure temperature at 100Hz, a
measurement that can be transformed into an estimate of the intensity
of small-scale turbulence.</figcaption>
</p>

## Strong abyssal mixing over smooth topography!

Mixing in the abyssal oceans is generally thought to occur mostly
above rough seafloor topography such as seamounts and the mid-ocean
ridges. Here, tidal and geostrophic currents flow over the topography
generating internal waves which break and mix the fluid.  This picture
has been developed over the last several decades through extensive
microstructure turbulence field campaigns. Much of this data was
recently compiled into a single data set by Waterhouse et. al. (2014),
who showed that indeed mixing measurements over rough topography and
mid-ocean ridges showed turbulent mixing intensities, quantified with
the turbulent kinetic energy dissipation epsilon, an order of
magnitude larger than those over smooth topography (compare red, green
and blue curves in Fig. 3).

Our cruise in December 2015 was to a region near the equator where the
seafloor was particularly flat and smooth compared with the global
average. Thus we were surprised to find very energetic mixing, with
energy dissipation rates just as strong as that found elsewhere over
mid-ocean ridges within the bottom 700m of the ocean (compare orange
line with blue line in Fig. 3 below 3200m). What was going on? Was
there something special about the equator?

<p align="center">
  <img src="/files/EpsProf.png" alt="Eps Profile" style="width:25%;
  text-align:center"/>
  <figcaption>Figure 3: Profiles of the dissipation rate of kinetic energy (epsilon) 
from our measurements (orange line with yellow confidence 
intervals) and from Waterhouse et. al. (2014) over smooth 
(red), rough (green) and mid-ocean ridge (blue) topography.</figcaption>
</p>

## Where does the energy come from?

If the energy that drives this mixing is not coming from the seafloor
through flow interactions with rough topography, then it must come
from the surface. One possibility is the downwards radiation of
low-frequency equatorial waves. These waves are commonly found in the
surface equatorial oceans and are generated by wind forcing and
instabilities (such as tropical instability waves). While we did not
have any temporal measurements to investigate the existance of waves
in the deep ocean (each profile of the CTD Chipod represents just one
point in time), we did have a long-time series of velocity
measurements in the upper 800m made by the shipboard ADCP instrument
(Fig. 4). These measurements did indeed show evidence of a
low-frequency wave (upward propagating phases highlighted with black
lines in Fig. 4). In fact, the properties of the measured wave were
consistent with the dispersion relation for a downward propagating
equatorial Yanai wave with downward energy flux ~2mWm-2. This downward
propagating wave had sufficient energy flux to drive the abyssal
mixing estimated from the Chipod instrument to average ~1mWm-2.


<p align="center">
  <img src="/files/SADCP_Simple.png" alt="SADCP Profile" style="width:60%;
  text-align:center"/>
  <figcaption>Figure 4: Measurements of meridional (North-South) velocity in the upper 800m
made using the shipboard ADCP instrument on the R/V Oceanus. The upward
propagating phases highlighted in black are consistent with a downward
propagating equatorial Yanai wave with energy flux ~2mWm-2.</figcaption>
</p>


## Non-traditional wave trapping

The downward propagating equatorial Yanai wave may have sufficient
energy to drive the mixing, but the remaining question is why would it
break and drive mixing in the bottom 700m? Wave breaking typically
occurs at critical layers created by a background mean flow, or where
the vertical wavelength of the wave becomes small in regions of high
stratification. However, we did not observe any mean flows, and the
stratification generally reduces towards the seafloor. One
possibility, normally neglected in most oceanograhic studies, is the
influence of the horizontal component of Earth's rotation (the so
called non-traditional effects). The dispersion relation for a
classical internal waves is,

<p align="center">
<img
src="https://latex.codecogs.com/svg.latex?\Large&space;\text{Traditional:
}\quad\omega^2=f^2+N^2\alpha^2" />
</p>

where <img
src="https://latex.codecogs.com/svg.latex?\Large&space;\omega" /> is
the wave frequency, f is the Coriolis parameter, <img
src="https://latex.codecogs.com/svg.latex?\Large&space;N^2" /> is the
stratification and <img
src="https://latex.codecogs.com/svg.latex?\Large&space;\alpha" /> is
the slope of wave characteristics. Since all terms in this equation
are positive, this implies that a wave can only exist equatorward of
where its frequency omega is equal to f (since f reduces towards the
equator). This results in the wave being trapped within its so-called
'inertial latitudes' (thick lines in Fig. 5a). However, when the
non-traditional terms are included, the dispersion relation acquires
an extra term.

<p align="center">
<img
src="https://latex.codecogs.com/svg.latex?\Large&space;\text{Non-traditional:
}\quad\omega^2=f^2+\color{red}{2f\tilde{f}\alpha}\color{black}+N^2\alpha^2" />
</p>

The additional term, dependent on the horizontal component of Earth's
rotation <img
src="https://latex.codecogs.com/svg.latex?\Large&space;\tilde{f}" />,
can be negative and allows wave to exist poleward of their inertial
latitude in regions where the stratification is small, i.e. near the
seafloor. Practically, this creates trapping regions near the seafloor
where wave energy can enter but cannot leave, and thus builds up and
breaks driving mixing (compare inverse Richardson number between
traditional and non-traditional cases in Fig. 5). Thus these
non-traditional effects may be responsible for the trapping of the
energy of the downward propagating equatorial Yanai wave, resulting in
the bottom-intensified mixing over smooth topography that we observed
with the Chipod.

<p align="center">
  <img src="/files/Movie.gif" alt="Non-traditional Wave Trapping" style="width:80%;
  text-align:center"/>
  <figcaption>Figure 5: Time-periodic solutions to
the wave equation for traditional (1st and 3rd panel) and
non-traditional (2nd and fourth panel) for a low-frequency wave
generated near the surface. The left two panels show meridional
velocity and the right two panels show inverse Richardson number. The
inverse Richardson number obtains high values in the trapping regions
near the seafloor in the non-traditional solution, suggesting enhanced
mixing there.</figcaption>
</p>

For more information please see my article published in Geophysical
Research Letters ([Evidence for Seafloor-Intensified Mixing by
Surface-Generated Equatorial
Waves](http://dx.doi.org/10.1002/2015GL066472)) or feel free to
contact me. This article was also the subject of several media
releases that are also worth a look:

[Stanford University News: Intense ocean turbulence discovered near
sea floor in equatorial Pacific, Stanford scientists
say](https://earth.stanford.edu/news/intense-deep-ocean-turbulence-equatorial-pacific-could-help-drive-global-circulation)

[Environmental Monitor: Study Of Deep Turbulence Reveals Ocean
Currents
Insights](http://www.fondriest.com/news/study-deep-turbulence-reveals-ocean-currents-insights.htm)

