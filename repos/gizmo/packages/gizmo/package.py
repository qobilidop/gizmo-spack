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

    version('develop-public', hg='https://bitbucket.org/phopkins/gizmo-public')

    variant('grackle', default=False)

    depends_on('mpi')

    depends_on('fftw@2:2.2+mpi')
    depends_on('gsl')
    depends_on('hdf5')
    depends_on('grackle', when='+grackle')

    def edit(self, spec, prefix):
        env['MPICC'] = spec['mpi'].mpicc
        env['MPICXX'] = spec['mpi'].mpicxx
        env['OPENMP_FLAG'] = self.compiler.openmp_flag

        opt = []
        if '+double' in spec['fftw']:
            opt += ['-DDOUBLEPRECISION_FFTW']
        elif '~float' in spec['fftw']:
            opt += ['-DNOTYPEPREFIX_FFTW']
        env['OPT'] = ' '.join(opt)

        with open('Makefile.systype', 'w') as f:
            f.write(MAKE_TEXT)
        touch('Config.sh')

    def install(self, spec, prefix):
        mkdir(prefix.bin)
        install('GIZMO', prefix.bin)
