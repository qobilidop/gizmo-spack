from spack import *


MAKEFILE_CONFIG_TEXT = """\
# CC
# FC
OPTIMIZE =
# CCFLAGS
# LNFLAGS
# DEFINEFLAGS
MAKE = make
"""


class AhfGizmo(MakefilePackage):
    """AMIGA halo finder configured for GIZMO simulations."""

    homepage = 'http://popia.ft.uam.es/AHF/'
    url = 'http://popia.ft.uam.es/AHF/files/ahf-v1.0-100.tgz'

    version('1.0-100', sha256='2ff3d92a7d8031871fd202683657bb5ccae2d7f286568819980404f939107cca')

    variant('hdf5', default=True)
    variant('mpi', default=True)
    variant('openmp', default=True)

    depends_on('hdf5', when='+hdf5')
    depends_on('mpi', when='+mpi')

    def edit(self, spec, prefix):
        with open('Makefile.config', 'w') as f:
            f.write(MAKEFILE_CONFIG_TEXT)

        ccflags = ['-std=c99']
        lnflags = []
        defineflags = [
            '-DMULTIMASS',
            '-DGAS_PARTICLES',
            '-DREFINE_BARYONIC_MASS'
        ]

        if '+hdf5' in spec:
            ccflags += ['-DH5_USE_16_API']
            lnflags += ['-lhdf5']
            defineflags += ['-DWITH_HDF5']

        if '+mpi' in spec:
            env['CC'] = spec['mpi'].mpicc
            env['FC'] = spec['mpi'].mpifc
            defineflags += ['-DWITH_MPI']
        else:
            env['CC'] = 'cc'
            env['FC'] = 'f90'

        if '+openmp' in spec:
            ccflags += [self.compiler.openmp_flag]
            defineflags += ['-DWITH_OPENMP']

        env['CCFLAGS'] = ' '.join(ccflags)
        env['LNFLAGS'] = ' '.join(lnflags)
        env['DEFINEFLAGS'] = ' '.join(defineflags)

    def build(self, spec, prefix):
        make('AHF')

    def install(self, spec, prefix):
        mkdir(prefix.bin)
        install(
            'bin/AHF-v' + str(spec.version),
            join_path(prefix.bin, 'AHF')
        )
