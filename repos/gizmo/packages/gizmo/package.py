from spack import *


CONFIG_FILE = 'Config.sh'
FULL_CONFIG_FILE = 'Config.full.sh'
MAKE_SYS_FILE = 'Makefile.systype'
MAKE_SYS_TEMPLATE = """\
CC       = {CC}
CXX      = {CXX}
FC       = {FC} {FC_FLAGS}
OPTIMIZE = {OPTIMIZE}

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
        make_configs = {
            'CC': spec['mpi'].mpicc,
            'CXX': spec['mpi'].mpicxx,
            'FC': spec['mpi'].mpifc,
            'FC_FLAGS': '',
            'OPTIMIZE': self.compiler.openmp_flag,
        }
        if self.compiler.name == 'intel':
            make_configs['FC_FLAGS'] = '-nofor_main'

        # Overwrite systype config
        with open(MAKE_SYS_FILE, 'w') as f:
            f.write(MAKE_SYS_TEMPLATE.format(**make_configs))

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
