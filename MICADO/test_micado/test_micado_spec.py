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

PLOTS = False

rc.__config__["!SIM.file.local_packages_path"] = "../../"


class TestInit:
    @pytest.mark.parametrize("modes", [["SCAO", "SPEC_3000x20"],
                                       ["SCAO", "SPEC_3000x50"],
                                       ["SCAO", "SPEC_15000x50"]])
    def test_micado_loads_optical_train(self, modes):
        cmds = sim.UserCommands(use_instrument="MICADO", set_modes=modes)
        micado = sim.OpticalTrain(cmds)
        opt_els = np.unique(micado.effects["element"])

        assert isinstance(micado, sim.OpticalTrain)
        assert len(opt_els) == 6
