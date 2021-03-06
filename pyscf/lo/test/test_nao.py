#!/usr/bin/env python

import unittest
from functools import reduce
import numpy
from pyscf import gto
from pyscf import scf
from pyscf.lo import nao

mol = gto.Mole()
mol.verbose = 0
mol.output = None
mol.atom = '''
     O    0.   0.       0
     1    0.   -0.757   0.587
     1    0.   0.757    0.587'''

mol.basis = 'cc-pvdz'
mol.build()
mf = scf.RHF(mol)
mf.conv_tol = 1e-14
mf.scf()

mol1 = mol.copy()
mol1.cart = True
mf1 = scf.RHF(mol1).set(conv_tol=1e-14).run()

class KnowValues(unittest.TestCase):
    def test_pre_nao(self):
        c = nao.prenao(mol, mf.make_rdm1())
        self.assertAlmostEqual(numpy.linalg.norm(c), 5.7742626195362039, 9)
        self.assertAlmostEqual(abs(c).sum(), 33.214804163888289, 6)

        c = nao.prenao(mol1, mf1.make_rdm1())
        self.assertAlmostEqual(numpy.linalg.norm(c), 5.5434134741828105, 9)
        self.assertAlmostEqual(abs(c).sum(), 31.999905597187052, 6)

    def test_nao(self):
        c = nao.nao(mol, mf)
        s = mf.get_ovlp()
        self.assertTrue(numpy.allclose(reduce(numpy.dot, (c.T, s, c)),
                                       numpy.eye(s.shape[0])))
        self.assertAlmostEqual(numpy.linalg.norm(c), 8.982385484322208, 9)
        self.assertAlmostEqual(abs(c).sum(), 90.443872916389637, 6)

        c = nao.nao(mol1, mf1)
        s = mf1.get_ovlp()
        self.assertTrue(numpy.allclose(reduce(numpy.dot, (c.T, s, c)),
                                       numpy.eye(s.shape[0])))
        self.assertAlmostEqual(numpy.linalg.norm(c), 9.4629575662640129, 9)
        self.assertAlmostEqual(abs(c).sum(), 100.24554485355642, 6)


if __name__ == "__main__":
    print("Test orth")
    unittest.main()


