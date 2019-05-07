import os
from spack import *


MAKE_TEXT = """\
CC       = $(MPICC)
CXX      = $(MPICXX)
FC       = $(MPICC)
OPTIMIZE = $(OPENMP_FLAG)

HDF5INCL = -DH5_USE_16_API
HDF5LIB  = -lhdf5 -lz
MPICHLIB =
"""


class Gizmo(MakefilePackage):
    """A flexible, massively-parallel, multi-physics simulation code."""

    homepage = "http://www.tapir.caltech.edu/~phopkins/Site/GIZMO.html"
    hg = 'https://bitbucket.org/phopkins/gizmo-public'

    version('develop')

    variant('hdf5', default=True)
    variant('grackle', default=False)

    depends_on('mpi')
    depends_on('gsl')
    depends_on('fftw@2:2.2+openmp+mpi')
    depends_on('hdf5+cxx+mpi', when='+hdf5')
    depends_on('grackle', when='+grackle')

    def edit(self, spec, prefix):
        env['MPICC'] = spec['mpi'].mpicc
        env['MPICXX'] = spec['mpi'].mpicxx
        env['OPENMP_FLAG'] = self.compiler.openmp_flag
        with open('Makefile.systype', 'w') as f:
            f.write(MAKE_TEXT)

    def install(self, spec, prefix):
        pass
