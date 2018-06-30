---
title: "Tropical Instability Waves and Kelvin Waves"
permalink: /projects/TIW_Kelvin
author_profile: true
---

{% include base_path %}


## The rapid decay of the TIW field in late 2014

During a research cruise to the equatorial Pacific in late 2014 on the
R/V Oceanus (see abyssal mixing section), we observed an unusual rapid
decay in the amplitude and propagation speed of a nearby TIW. Over a
period of only 16 days (half the dominant 30-day period of TIWs), the
extent of TIW-driven meridional excursions of the NEF reduced
dramatically (see Fig. 1a-c). This rapid decay turned out to coincide
with the arrival of a downwelling equatorial Kelvin Wave from the
western Pacific (see Fig. 1d).

<p align="center">
  <img src="/files/GOES_SST_plot.png" alt="GOES SST" style="width:40%;
  text-align:center"/>
  <img src="/files/EqSubSurfTempAnom.png" alt="Equatorial Subsurface Temperature" style="width:40%;
  text-align:center"/>
  <figcaption> Figure 1: GOES SST observations in the eastern equatorial Pacific on the
(a) 10th (b) 18th and (c) 26th of November 2014 showing a rapid
decrease in the amplitude of the TIW-driven meridional oscillations in
the north equatorial front. (d) Upper equatorial heat anomalies
between September and November 2014 showing a downwelling equatorial
Kelvin wave propagating into the eastern Pacific. The image in (d) was
provided by the NOAA/NWS Climate Prediction Center, College Park
Maryland from their Web site at http://www.cpc.ncep.noaa.gov/). The
GOES SST data (a-c) was obtained from the JPL Physical Oceanography
DAAC (NOAA/NESDIS, 2003)</figcaption>
</p>

## Intraseasonal first-baroclinic mode Kelvin waves

To investigate whether the Kelvin wave was responsible for the changes
in TIW amplitude, we decided to run a set of ROMS simulations forced
with intraseasonal Kelvin waves. These Kelvin wave experiments were
spun off of a statistically-steady spinup simulation forced with
constant atmospheric forcing taken from the strong trade-winds (and
thus strong TIWs) season. From this steady spinup run, we forced
60-day period upwelling and downwelling Kelvin wave pulses in the
western Pacific. These intraseasonal Kelvin waves propagate across to
the eastern Pacific driving changes in the thermocline depth, sea
surface height (SSH) and zonal currents (see Fig. 2 a, b). To cleanly
separate the TIW flow from the Kelvin wave flow, we performed an
ensemble of experiments allowing an ensemble average to remove the TIW
variability (see FIg. 2 c,d). We found that indeed downwelling Kelvin
waves do result in a significant decrease in the amplitude of the TIW
field, here measured using the TIW kinetic energy (TIWKE; see Fig.
2e). In contrast, an upwelling Kelvin wave drove a strong
intensification of the TIWKE, which peaked roughly 30-days after the
Kelvin wave peak (Fig. 2f).


<p align="center">
  <img src="/files/2016-09-07.png" alt="Hovmoellers" style="width:100%;
  text-align:center"/>
  <figcaption> Figure 2: Time–longitude plots of the 20C isotherm depth anomaly on the
equator for a single (a) downwelling and (b) upwelling intraseasonal
Kelvin wave and for the ensemble average (c) downwelling and (d)
upwelling Kelvin wave experiments. Time–longitude plot of the TIWKE
integrated over the top 244m for (e) downwelling and (f) upwelling
experiments. Also shown are 0.01-m contours of SSH anomalies, with
dark gray contours indicating positive values and light gray contours
indicating negative values. The forcing region and time period is
shown with the black box. The green line in (a)–(d) indicates a phase
speed of 2.64ms-1</figcaption>
</p>

## The TIWKE budget

To explain why the Kelvin waves drive changes in the TIWKE, we
examined the TIWKE, or EKE, budget described by the following
equation:

<p align="center">
  <img src="/files/TIWKEbudget.png" alt="TIWKE Budget Equation" style="width:65%;
  text-align:center"/>
</p>  
<p align="center">
  <img src="/files/TIWKEeq.png" alt="TIWKE" style="width:30%;
  text-align:center"/>
</p>  

where K is the TIWKE and the terms on the right-hand-side represent
mean advection of TIWKE, pressure (or wave) fluxes of TIWKE, eddy
advection of TIWKE, conversion of potential energy to TIWKE, fritional
dissipation of TIWKE and shear production of TIWKE respectively. The
over-line represents an ensemble average while the prime is a
deviation from this average, representing the TIW flow. In the steady
spinup run, the TIWKE budget is dominated by a balance between the
production of TIWKE through conversion from PE (the w'b' term) and
lateral shear production acting on the meridional shear of zonal
velocity (LSP; the u'v' dU/dy term), dissipation of TIWKE through
friction (the u'Fh' term) and the radiation of waves (the u'P'
pressure flux term).

The Kelvin waves disrupt this balance by altering the background flow
(U and V) and the TIW Reynold's stress terms (u'v', w'b' etc.). In
particular, a downwelling Kelvin wave reduces the meridional shear,
dU/dy, in the region where the TIWs are strong, thereby reducing the
LSP. This kicks off a negative feedback where the TIWKE reduces,
driving a reduction in the Reynold's stress u'v' and thus a further
reduction in LSP. This negative feedback continues until the TIWKE
sink terms of dissipation and wave radiation adjust to compensate the
changes in LSP. For more details please see my Journal of Physical
Oceanography article Holmes and Thomas (2016) Modulation of Tropical
Instability Wave Intensity by Equatorial Kelvin Waves.

## The upper-ocean heat budget

Intraseasonal Kelvin waves are known to be critical ingredients for
initiating sustained perturbations in the coupled tropical
atmosphere-ocean as part of the El Nino - Southern Oscillation
(ENSO). In particular, downwelling Kelvin waves initiated by westerly
wind bursts in the western Pacific are known to drive warm SST
anomalies in the eastern Pacific through vertical and zonal
advection. In our simulations we do indeed see these SST anomalies
(Fig. 3 a, b). However, a single downwelling (upwelling) Kelvin wave
pulse should drive a net warming (cooling) due to the net displacement
of the zonal gradient in SST to the east (west). In our simulations we
find that this net SST change is damped by the changes in the TIW
meridional heat fluxes (due to the change in TIWKE), which counter the
Kelvin wave induced SST anomalies (compare dotted and dashed lines in
Fig. 3 a, b). This results has implications for the role of TIWs in
the initiation of ENSO events.


<p align="center">
  <img src="/files/HeatBudget.png" alt="Hovmoellers" style="width:50%;
  text-align:center"/>
  <figcaption> Fig 3: Time series of terms in the upper-ocean heat budget (expressed
in terms of an average temperature). Average temperature in (a)
downwelling and (b) upwelling experiments (solid lines). (c)
Convergence of mean heat fluxes and (d) convergence of meridional eddy
heat fluxes for both downwelling (blue) and upwelling (red)
experiments. Also shown in (a) and (b) are the time-integrated mean
convergence (dashed) and meridional eddy convergence (dotted)
terms. The large initial changes in heat content are driven by the
mean heat convergence through Kelvin wave zonal and vertical
advection. Kelvin wave zonal advection drives a net change in heat
content [cf. dashed lines in (a) and (b) before and after the Kelvin
wave passes] that is compensated for by changes in the meridional eddy
convergence [dotted lines in (a) and (b) after the Kelvin wave passes]</figcaption>
</p>

For more information, see my article published in the Journal of
Physical Oceanography: [Modulation of Tropical Instability Wave
Intensity by Equatorial Kelvin
Waves](http://dx.doi.org/10.1175/JPO-D-16-0064.1).


