"""
Tests the SPEC mode, that it compiles and runs.

Ideally this will also contain a flux consistency test or two

Comments
--------
- 2022-03-18 (KL)

"""

# integration test using everything and the MICADO package
import pytest
from pytest import approx

import numpy as np

import scopesim as sim
from scopesim import rc
from scopesim.source import source_templates as st

from matplotlib import pyplot as plt
from matplotlib.colors import LogNorm

rc.__config__["!SIM.file.local_packages_path"] = "../../"
PLOTS = False


class TestInit:
    @pytest.mark.parametrize("modes", [["SCAO", "SPEC_3000x20"],
                                       ["SCAO", "SPEC_3000x50"],
                                       ["SCAO", "SPEC_15000x50"]])
    def test_loads_optical_train(self, modes):
        cmds = sim.UserCommands(use_instrument="MICADO", set_modes=modes)
        micado = sim.OpticalTrain(cmds)
        opt_els = np.unique(micado.effects["element"])

        assert isinstance(micado, sim.OpticalTrain)
        assert len(opt_els) == 6

    def test_runs_spec_hk_15000x50(self):
        src = st.empty_sky()

        cmds_img = sim.UserCommands(use_instrument="MICADO",
                                    set_modes=["SCAO", "IMG_4mas"])

        micado_img = sim.OpticalTrain(cmds_img)
        micado_img.observe(src)

        img_av_flux = np.median(micado_img.image_planes[0].data)

        cmds = sim.UserCommands(use_instrument="MICADO",
                                set_modes=["SCAO", "SPEC_15000x50"])
        cmds.cmds["!OBS.trace_file"] = "TRACE_MICADO.fits"    # Old, missing x=0
        cmds.cmds["!DET.dit"] = 3600
        cmds.cmds["!OBS.filter_name_fw1"] = "open"
        cmds.cmds["!OBS.filter_name_fw2"] = "Ks"

        micado = sim.OpticalTrain(cmds)
        FULL_DETECTOR = True
        micado["detector_window"].include = not FULL_DETECTOR
        micado["full_detector_array"].include = FULL_DETECTOR
        micado.observe(src)

        spec_int_flux = np.sum(micado.image_planes[0].data, axis=0)
        spec_av_flux = np.median(spec_int_flux[40:2600])

        slit_width = 50 / 4.      # [pixels]
        grating_efficiency = 0.6**2
        scale_factor = slit_width * grating_efficiency

        assert spec_av_flux / scale_factor == approx(img_av_flux, rel=0.1)

        # plt.subplot(121)
        # plt.imshow(micado.image_planes[0].data, norm=LogNorm(),
        #            origin="lower")
        #
        # plt.subplot(122)
        # plt.imshow(hdul[1].data, norm=LogNorm(), origin="lower")
        #
        # plt.show()
