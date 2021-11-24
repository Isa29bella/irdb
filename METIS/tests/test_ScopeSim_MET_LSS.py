"""
0-mag photon fluxes from Vega Spectrum
--------------------------------------
J band (J=0mag)   --> 3505e6 ph/s/m2
H band (H=0mag)   --> 2416e6 ph/s/m2
Ks band (Ks=0mag) --> 1211e6 ph/s/m2
Lp band (Lp=0mag) -->  576e6 ph/s/m2
Mp band (Mp=0mag) -->  268e6 ph/s/m2


ScopeSim using SkyCalc defaults above atmosphere
------------------------------------------------
J  BG: 688 ph/s/m2/arcsec2
H  BG: 4e3 ph/s/m2/arcsec2
Ks BG: 1e3 ph/s/m2/arcsec2
Lp BG: 4e6 ph/s/m2/arcsec2


Theoretical METIS BG based on SkyCalc
-------------------------------------
Ks BG:  30e3 ph/s/pixel
Lp BG: 118e3 ph/s/pixel
Mp BG: 3.2e6 ph/s/pixel

"""


from pytest import approx
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import LogNorm

import scopesim as sim
from scopesim.source.source_templates import star, empty_sky, star_field
from scopesim.source.spectrum_templates import ab_spectrum
from scopesim import rc

rc.__currsys__['!SIM.file.local_packages_path'] = "../../"

PLOTS = False


class TestMetisLss:
    def test_works(self):
        src = star(mag=0, x=0, y=0) + \
              star(mag=2, x=-2, y=0) + \
              star(mag=4, x=2, y=0)
        # src = empty_sky()

        cmds = sim.UserCommands(use_instrument="METIS", set_modes=["lss_l"])
        cmds["!OBS.dit"] = 1
        metis = sim.OpticalTrain(cmds)
        metis["metis_psf_img"].include = False

        metis.observe(src)
        hdus = metis.readout()

        implane = metis.image_planes[0].data
        det_img = hdus[0][1].data
        assert 0 < np.sum(implane) < np.sum(det_img)

        if not PLOTS:
            plt.subplot(122)
            plt.imshow(hdus[0][1].data, origin="lower", norm=LogNorm(), vmin=1)
            plt.title("Detctor Plane (with noise)")
            plt.colorbar()

            plt.subplot(121)
            plt.imshow(metis.image_planes[0].data, origin="lower",
                       norm=LogNorm(), vmin=1)
            plt.title("Image Plane (noiseless)")
            plt.colorbar()
            plt.show()

    def test_integrated_spec_bg_equals_img_bg(self):
        src = empty_sky()

        cmds_img = sim.UserCommands(use_instrument="METIS", set_modes=["img_lm"])
        metis_img = sim.OpticalTrain(cmds_img)
        metis_img["metis_psf_img"].include = False
        metis_img.observe(src)
        img = metis_img.image_planes[0].data

        cmds_lss = sim.UserCommands(use_instrument="METIS", set_modes=["lss_l"])
        metis_lss = sim.OpticalTrain(cmds_lss)
        metis_lss["metis_psf_img"].include = False
        metis_lss.observe(src)
        lss = metis_lss.image_planes[0].data

        img_med = np.median(img)
        lss_med = np.median(np.sum(lss, axis=0))

        assert img_med, lss_med
