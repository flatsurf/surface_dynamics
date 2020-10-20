r"""
Installation script for the flatsurf module

It depends on distutils
"""

try:
    import sage.all
except ImportError:
    raise ValueError("this package currently installs only inside SageMath (http://www.sagemath.org)\n"
                     "If you are using Ubuntu with Sage installed from the official apt repository, run\n"
                     "first in a console \"$ source /usr/share/sagemath/bin/sage-env\"\n")

from distutils.core import setup
from distutils.extension import Extension
from Cython.Build import cythonize
import sys, os
from distutils.version import LooseVersion

with open("surface_dynamics/version.py") as f:
    version = f.read().strip()
    prefix = "version='"
    suffix = "'"
    assert version.startswith(prefix) and version.endswith(suffix)
    version = version[len(prefix):len(version)-len(suffix)]
with open("README.rst") as f:
    long_description = f.read()

try:
    import ppl
except ImportError:
    sys.stderr.write('Warning: pplpy not installed. Will not compile iet_family\n')
    WITH_PPL = False
else:
    WITH_PPL = True

extensions_data = {
    'origamis': {
        'name': 'surface_dynamics.flat_surfaces.origamis.origami_dense',
        'dir': os.path.join('flat_surfaces', 'origamis'),
        'sources': ['origami_dense.pyx', 'normal_form.c', 'lyapunov_exponents.c'],
        'headers': ['origami_dense.pxd', 'lyapunov_exponents.h', 'normal_form.h']
        },

    'lyapunov_exponents': {
        'name': 'surface_dynamics.interval_exchanges.lyapunov_exponents',
        'dir': 'interval_exchanges',
        'sources': ['lyapunov_exponents.pyx', 'generalized_permutation.c' , 'lin_alg.c', 'quad_cover.c', 'random.c', 'permutation.c'],
        'headers': ['lyapunov_exponents.h']
        },

    # this will not compile on sage < 8.0 (troubles with cysignals)
    'integer_iet': {
        'name': 'surface_dynamics.interval_exchanges.integer_iet',
        'dir': 'interval_exchanges',
        'sources': ['integer_iet.pyx', 'int_iet.c', 'int_vector.c'],
        'headers': ['integer_iet.pxd', 'int_iet.h'],
        },

    # build iet_family only if pplpy is available
    'iet_family': {
        'name': 'surface_dynamics.interval_exchanges.iet_family',
        'dir': 'interval_exchanges',
        'sources': ['iet_family.pyx'],
        'headers': [],
        'condition': WITH_PPL
        }
}

extensions = []
source_files = []

for name, data in extensions_data.items():
    if data.get('condition', True):
        print('Adding extension {}:\n  sources = {}\n  headers = {}'.format(data['name'], data['sources'], data['headers']))

        full_dir = os.path.join('surface_dynamics', data['dir'])
        sources = [os.path.join(full_dir, src) for src in data['sources']]
        headers = [os.path.join(full_dir, data['dir'], head) for head in data['headers']]
        extensions.append(Extension(data['name'], sources = sources))

        sources = [os.path.join(data['dir'], src) for src in data['sources']]
        headers = [os.path.join(data['dir'], head) for head in data['headers']]
        source_files.extend(sources)
        source_files.extend(headers)

setup(name='surface_dynamics',
      version=version,
      description="Dynamics on surfaces",
      long_description=long_description,
      author='Vincent Delecroix',
      author_email='vincent.delecroix@u-bordeaux.fr',
      url='http://www.labri.fr/perso/vdelecro/surface-dynamics/latest/',
      license="GPL v2",
      packages=['surface_dynamics',
                'surface_dynamics/misc',
                'surface_dynamics/topology',
                'surface_dynamics/flat_surfaces',
                'surface_dynamics/databases',
                'surface_dynamics/flat_surfaces/origamis',
                'surface_dynamics/interval_exchanges'],
      package_data={
          'surface_dynamics': source_files,
          'surface_dynamics/databases': ['cylinder_diagrams/cyl_diags*', 'generalized_permutation_twins/twins*'],
          'surface_dynamics/flat_surfaces/origamis': ['origamis.db'],
          },
      ext_modules=cythonize(extensions),
    classifiers=[
      'Development Status :: 4 - Beta',
      'Intended Audience :: Science/Research',
      'License :: OSI Approved :: GNU General Public License v2 or later (GPLv2+)',
      'Operating System :: OS Independent',
      'Programming Language :: C',
      'Programming Language :: C++',
      'Programming Language :: Python',
      'Programming Language :: Cython',
      'Topic :: Scientific/Engineering :: Mathematics',
    ],
    keywords='surfaces, dynamics, geometry, flat surfaces, Abelian differentials, quadratic differentials, Riemann surfaces',
)
