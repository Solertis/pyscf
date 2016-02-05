#!/usr/bin/env python

import unittest
import numpy
from pyscf import gto
from pyscf import dft
from pyscf.dft import gen_grid
from pyscf.dft import radi

h2o = gto.Mole()
h2o.verbose = 0
h2o.output = None#"out_h2o"
h2o.atom.extend([
    ["O" , (0. , 0.     , 0.)],
    [1   , (0. , -0.757 , 0.587)],
    [1   , (0. , 0.757  , 0.587)] ])

h2o.basis = {"H": '6-31g',
             "O": '6-31g',}
h2o.build()

class KnowValues(unittest.TestCase):
    def test_gen_grid(self):
        grid = gen_grid.Grids(h2o)
        grid.prune_scheme = None
        grid.radi_method = radi.gauss_chebyshev
        grid.becke_scheme = gen_grid.original_becke
        grid.atomic_radii = radi.becke_atomic_radii_adjust(h2o, \
                numpy.round(radi.BRAGG_RADII, 2))
        grid.atom_grid = {"H": (10, 50), "O": (10, 50),}
        coord, weight = grid.setup_grids()
        self.assertAlmostEqual(numpy.linalg.norm(coord), 185.91245945279027, 9)
        self.assertAlmostEqual(numpy.linalg.norm(weight), 1720.1317185648893, 9)

        grid.becke_scheme = gen_grid.stratmann
        coord, weight = grid.setup_grids()
        self.assertAlmostEqual(numpy.linalg.norm(weight), 1730.3692983091271, 9)

    def test_radi(self):
        grid = gen_grid.Grids(h2o)
        grid.prune_scheme = None
        grid.atomic_radii = radi.becke_atomic_radii_adjust(h2o, \
                numpy.round(radi.COVALENT_RADII, 2))
        grid.radi_method = radi.mura_knowles
        grid.atom_grid = {"H": (10, 50), "O": (10, 50),}
        coord, weight = grid.setup_grids()
        self.assertAlmostEqual(numpy.linalg.norm(weight), 1804.5437331817291, 9)

        grid.radi_method = radi.delley
        coord, weight = grid.setup_grids()
        self.assertAlmostEqual(numpy.linalg.norm(weight), 1686.3482864673697, 9)

    def test_prune(self):
        grid = gen_grid.Grids(h2o)
        grid.prune_scheme = gen_grid.sg1_prune
        grid.atom_grid = {"H": (10, 50), "O": (10, 50),}
        coord, weight = grid.setup_grids()
        self.assertAlmostEqual(numpy.linalg.norm(coord), 202.17732600266302, 9)
        self.assertAlmostEqual(numpy.linalg.norm(weight), 442.54536463517167, 9)

        grid.prune_scheme = gen_grid.nwchem_prune
        coord, weight = grid.setup_grids()
        self.assertAlmostEqual(numpy.linalg.norm(coord), 151.01253616288849, 9)
        self.assertAlmostEqual(numpy.linalg.norm(weight), 586.59843503169827, 9)


if __name__ == "__main__":
    print("Test Grids")
    unittest.main()
