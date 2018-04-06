import numpy as np
import pytest
import mbuild as mb
import parmed as pmd
from porebuilder.tests.base_test import BaseTest

class TestPoreBuilder(BaseTest):
    """
    Unit Tests for Pore class functionality.
    """

    def test_save(self, gph_pore_nosolv, gph_pore_solv):
        gph_pore_nosolv.save(filename='gph_pore_nosolv.gro')
        gph_pore_solv.save(filename='gph_pore.gro')

    def test_porewidth(self, gph_pore_solv):
        bot = np.min(gph_pore_solv.bot_xyz[:,1])
        top = np.max(gph_pore_solv.top_xyz[:,1]) # change naming
        pore_width = bot - top
        np.testing.assert_almost_equal(pore_width, 1, 4)

    def test_sheet_dims(self, gph_pore_solv):
        x_length = np.max(gph_pore_solv.bot_xyz[:,0]) 
        - np.min(gph_pore_solv.bot_xyz[:,0])
        assert x_length == pytest.approx(3, 0.5)
        y_length = np.max(gph_pore_solv.bot_xyz[:,2])
        - np.min(gph_pore_solv.bot_xyz[:,2])
        assert y_length == pytest.approx(3, 0.5)
    
    def test_n_particles(self, gph_pore_solv, gph_pore_nosolv):
        if gph_pore_solv:
            assert gph_pore_solv.n_particles == 5016
        elif gph_pore_nosolv:
            assert gph_pore_nosolv.n_particles == 2016
    
    def test_particles_in_box(self, gph_pore_solv):
        box = mb.Box(gph_pore_solv.box)
        totalPM = pmd.Structure()
        for child in gph_pore_solv.children:
            if child.name in 'Compound':
                totalPM += child.to_parmed(residues='Compound', box=box)
            elif child.name in gph_pore_solv.fluid_name:
                totalPM += child.to_parmed(residues='SOL', box=box)
        gphPM = totalPM['Compound',:]
        SOLPM = totalPM['SOL', :]
        systemPM = gphPM + SOLPM
        systemPM.box = np.empty(6)
        systemPM.box[:3] = box.maxs * 10 
        systemPM.box[3:7] = 90
        for position in gph_pore_solv.xyz:
            for x in range(3):
                assert position[x] < systemPM.box[x]
                assert position[x] >= 0.0 # May have to change this test

    # TODO: Get correct x-dimension of graphene sheet
    """def test_x_bulk_length(self, gph_pore_solv):
        gph_length = np.max(gph_pore_solv.bot_xyz[0])
        np.min(gph_pore_solv.bot_xyz[0])
        assert (gph_pore_solv.periodicity[0] - gph_length)/2 == # need value"""
