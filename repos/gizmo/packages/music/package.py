from spack import *


class Music(MakefilePackage):
    """Multi-Scale Initial Conditions for Cosmological Simulations"""

    homepage = "https://www-n.oca.eu/ohahn/MUSIC/"
    hg = 'https://bitbucket.org/ohahn/music'

    version('develop')

    variant('fftw3', default=True)
    variant('openmp', default=True)
    variant('float', default=False)
    variant('hdf5', default=True)

    patch('Makefile.patch')

    depends_on('mpi')
    depends_on('gsl')

    depends_on('fftw-api@3', when='+fftw3')
    depends_on('fftw-api@2', when='-fftw3')

    depends_on('fftw+openmp', when='+openmp')

    depends_on('fftw+float', when='+float')
    depends_on('fftw+double', when='-float')

    depends_on('hdf5+cxx', when='+hdf5')

    def edit(self, spec, prefix):
        env['CC'] = spec['mpi'].mpicxx

        if '+fftw3' in spec:
            env['FFTW3'] = 'yes'
        else:
            env['FFTW3'] = 'no'

        if '+openmp' in spec:
            env['MULTITHREADFFTW'] = 'yes'
            env['CFLAGS'] = self.compiler.openmp_flag
            env['LFLAGS'] = self.compiler.openmp_flag
        else:
            env['MULTITHREADFFTW'] = 'no'

        if '+float' in spec:
            env['SINGLEPRECISION'] = 'yes'
        else:
            env['SINGLEPRECISION'] = 'no'

        if '+hdf5' in spec:
            env['HAVEHDF5'] = 'yes'
        else:
            env['HAVEHDF5'] = 'no'

    def install(self, spec, prefix):
        mkdir(prefix.bin)
        install('MUSIC', prefix.bin)
