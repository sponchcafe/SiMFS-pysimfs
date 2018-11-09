from pysimfs import Diffusion, Simulation
import json
import pytest
import os
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit 

def gauss(x, x0, A, sigma):
    return A*np.exp(-1/2*(x-x0)**2/sigma**2)

@pytest.fixture
def diffusion_sigma(parameter_json):
    D = parameter_json['diffusion_coefficient']
    inc = parameter_json['increment']
    return (2*D*inc)**0.5

@pytest.fixture
def parameter_json():
    return json.load(open('dif_default.json', 'r'))

@pytest.fixture
def parameters(parameter_json):
    return Diffusion(**parameter_json).params

@pytest.fixture
def n_coordinates(parameter_json):
    return int(parameter_json['experiment_time']/parameter_json['increment'])

@pytest.fixture
def diffusion_coordinates(parameter_json):
    coord_name = parameter_json['coordinate_output']
    with Simulation() as S:
        S.add(Diffusion(**parameter_json))
        S.run()
        coords = S.get_results()[coord_name]
    os.remove(coord_name)
    return coords

@pytest.fixture
def collisions(parameter_json):
    collision_name = parameter_json['collision_output']
    with Simulation() as S:
        S.add(Diffusion(**parameter_json))
        S.run()
        collisions = S.get_results()[collision_name]
    os.remove(collision_name)
    return collisions


def test_parameter_passing(parameter_json, parameters):
    for k in parameter_json.keys():
        assert parameters[k] == parameter_json[k]

def test_coordinate_n_points(parameter_json, diffusion_coordinates, n_coordinates):
    assert len(diffusion_coordinates) == n_coordinates

def test_time_range(parameter_json, diffusion_coordinates, n_coordinates):
    assert diffusion_coordinates[0]['t'] == 0.0
    assert diffusion_coordinates[-1]['t'] == parameter_json['increment']*(n_coordinates-1)

def test_increment(parameter_json, diffusion_coordinates):
    times = diffusion_coordinates[:]['t']
    assert np.allclose(times[1:]-times[:-1], parameter_json['increment'])

def test_xy_bounds(parameter_json, diffusion_coordinates):
    coords = diffusion_coordinates
    radii = (coords['x']**2+coords['y']**2)**0.5 
    assert np.all(radii <= parameter_json['radius'])

def test_z_bounds(parameter_json, diffusion_coordinates):
    coords = diffusion_coordinates
    assert np.all(coords['z'] <= parameter_json['half_height'])
    assert np.all(coords['z'] >= -parameter_json['half_height'])

def test_step_distribution(parameter_json, diffusion_coordinates, diffusion_sigma):

    c0 = diffusion_coordinates[:-1]
    c1 = diffusion_coordinates[1:]

    bins, step = np.linspace(-diffusion_sigma*10, diffusion_sigma*10, 101, retstep=True)
    fig, axes = plt.subplots(nrows=3, sharex=True)

    for c, ax in zip('xyz', axes):
        steps = c1[c]-c0[c]
        hist , _ = np.histogram(steps, bins)
        bins += step/2
        fit, res = curve_fit(gauss, bins[:-1], hist, p0=(0, 100, diffusion_sigma))

        label = f'c={fit[0]:.2e},\nsigma={fit[2]:.2e}'

        ax.plot(bins[:-1], hist)
        ax.plot(bins[:-1], gauss(bins[:-1], *fit), ls='--', color='k', label=label)
        ax.legend()
        ax.set_xlabel(f'Displacement in {c} in m')
        ax.set_ylabel('Count')
        ax.grid()
        
        assert fit[0] < diffusion_sigma*0.01
        assert fit[-1]-diffusion_sigma < diffusion_sigma*0.01

    plt.tight_layout()
    plt.savefig('test_step_distribution.png', format='png')

def test_collisions(parameter_json, diffusion_coordinates, collisions, diffusion_sigma):

    coords = diffusion_coordinates

    for c in collisions:
        index = np.argmax(c<coords['t'])-1
        coord = coords[index] 
        radius = (coord['x']**2+coord['y']**2)**0.5
        at_radius = radius - parameter_json['radius'] < diffusion_sigma
        at_top_or_bottom = coord['z'] - parameter_json['half_height'] < diffusion_sigma
        assert at_radius or at_top_or_bottom


