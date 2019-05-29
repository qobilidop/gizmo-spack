from spack import *


CONFIG_FILE = 'Config.sh'
FULL_CONFIG_FILE = 'Config.full.sh'
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

    version('public', hg='https://bitbucket.org/phopkins/gizmo-public')

    variant('mpi_in_place', default=False)
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

        # Overwrite systype config
        with open('Makefile.systype', 'w') as f:
            f.write(MAKE_TEXT)

        # Load configs
        touch(CONFIG_FILE)
        with open(CONFIG_FILE, 'r') as f:
            configs = f.readlines()

        # Update configs
        if '+mpi_in_place' in spec:
            configs += ['USE_MPI_IN_PLACE\n']
        if '+double' in spec['fftw']:
            configs += ['DOUBLEPRECISION_FFTW\n']
        elif '~float' in spec['fftw']:
            configs += ['NOTYPEPREFIX_FFTW\n']

        # Set full configs
        with open(FULL_CONFIG_FILE, 'w') as f:
            f.writelines(configs)

        make('clean')

    build_targets = ['CONFIG=' + FULL_CONFIG_FILE]

    def install(self, spec, prefix):
        mkdir(prefix.bin)
        install('GIZMO', prefix.bin)
