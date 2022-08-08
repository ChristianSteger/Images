# Description: Plot atmospheric refraction according to Saemundsson (1986)
#
# Author: Christian Steger, August 2022

# Load modules
import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl

mpl.style.use("classic")
 
# Change latex fonts
mpl.rcParams["mathtext.fontset"] = "custom"
# custom mathtext font (set default to Bitstream Vera Sans)
mpl.rcParams["mathtext.default"] = "rm"
mpl.rcParams["mathtext.rm"] = "Bitstream Vera Sans"

# Output path for plot
path_plot = "/Users/csteger/Desktop/"

###############################################################################
# Functions
###############################################################################


def Saemundsson(h, T=10.0, P=101.0, h_min=-1.0, h_max=90.0):
    """"Refraction correction of solar elevation angle according to Saemundsson

    Input:
        h: true solar elevation angle [degree]
        T: temperature [Celsius]
        P: atmospheric pressure [kPa]
    Output: refraction correction [degree]

    Sources:
        - Saemundsson, P. (1986). "Astronomical Refraction". Sky and Telescope.
          72: 70
        - Meeus, J. (1998): Astronomical Algorithm - Second edition, p. 106
        - https://en.wikipedia.org/wiki/Atmospheric_refraction"""
    h = h.clip(min=h_min, max=h_max)  # restrict input angle range
    R = (1.02 / np.tan(np.deg2rad(h + 10.3 / (h + 5.11))))
    R += 0.0019279  # set R = 0.0 for h = 90.0 degree
    # (Book Astronomical Algorithm, p. 106)
    R *= (P / 101.0) * (283.0 / (273.0 + T))
    return R * (1.0 / 60.0)


###############################################################################
# Plot
###############################################################################

# Solar elevation angle
sol_elev = np.linspace(-2.5, 90.0, 926)  # solar elevation angle [degree]

# Atmospheric conditions
atmos_cond = ({"T": 10.0,  "P": 101.0, "col": "red"},
              {"T": -30.0, "P": 101.0, "col": "blue"},
              {"T": 10.0,  "P": 70.0,  "col": "coral"},
              {"T": -30.0, "P": 70.0,  "col": "cornflowerblue"})

# Test plot
fig = plt.figure(figsize=(10, 5))
for i in atmos_cond:
    plt.plot(sol_elev, Saemundsson(sol_elev, T=i["T"], P=i["P"], h_min=-20.0),
             color=i["col"], lw=1.8, ls=":")
    lab = "T = %.1f" % i["T"] + "$^{\circ}$ C, P = %.1f" % i["P"] + " kPa"
    plt.plot(sol_elev, Saemundsson(sol_elev, T=i["T"], P=i["P"]),
             color=i["col"], lw=1.8, ls="-", label=lab)
plt.vlines(x=0.0, ymin=-0.5, ymax=3.5, color="black", lw=1.2)
plt.hlines(y=0.0, xmin=-2.5, xmax=90.0, color="black", lw=1.2)
plt.fill_between(x=[-5.0, -1.0], y1=0.0, y2=3.5, color="gray", alpha=0.5)
plt.axis([-3.0, 45.0, -0.05, 0.88])
plt.xlabel("Solar elevation angle [$^{\circ}$]")
plt.ylabel("Refraction correction [$^{\circ}$]")
plt.legend(frameon=False, loc="upper right", fontsize=12)
plt.title("Atmospheric refraction according to Saemundsson (1986)",
          fontweight="bold", fontsize=12)
fig.savefig(path_plot + "Atmos_refrac.png", dpi=300, bbox_inches="tight")
plt.close(fig)


# Barometric formula
T_0 = 273.15 + 10.0  # [K]
p_0 = 101.0  # [kPa]
# Sources:
#  - Book Atmospheric Science - An Introductory Survey, p. 104
#  - https://en.wikipedia.org/wiki/Atmospheric_pressure
g = 9.81  # acceleration due to gravity at sea level [m s-2]
R_d = 287.0  # gas constant for dry air [J K􏰅-1 kg􏰅-1]
tau = 0.0065  # lapse rate of U.S. Standard Atmosphere [K m-1]

z = np.linspace(0.0, 31000.0, 1000)
p = p_0 * ((T_0 - tau * z) / T_0) ** (g / (R_d * tau))

plt.figure()
plt.plot(p, z / 1000.0)
plt.xlabel("Pressure [kPa]")
plt.ylabel("Altitude [km]")
