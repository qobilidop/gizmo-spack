from spack import *


class Music(MakefilePackage):
    """Multi-Scale Initial Conditions for Cosmological Simulations"""

    homepage = "https://www-n.oca.eu/ohahn/MUSIC/"
    hg = 'https://bitbucket.org/ohahn/music'

    version('develop')

    variant('fftw3', default=True)
    variant('hdf5', default=False)

    patch('Makefile.patch')

    # FIXME: MUSIC doesn't really depend on MPI,
    # but we are stuck with this to compile properly for now.
    depends_on('mpi')

    depends_on('gsl')

    depends_on('fftw@3:+double+openmp', when='+fftw3')
    depends_on('fftw@2:2.2+double+openmp', when='-fftw3')

    depends_on('hdf5+cxx', when='+hdf5')

    # requires C++11
    def flag_handler(self, name, flags):
        if name == 'cxxflags':
            flags.append(self.compiler.cxx11_flag)
        return (flags, None, None)

    def edit(self, spec, prefix):
        # FIXME: See the MPI notes above. 'c++' should be good here.
        env['CC'] = spec['mpi'].mpicxx

        if '+fftw3' in spec:
            env['FFTW3'] = 'yes'
        else:
            env['FFTW3'] = 'no'

        env['MULTITHREADFFTW'] = 'yes'
        env['CFLAGS'] = self.compiler.openmp_flag
        env['LFLAGS'] = self.compiler.openmp_flag

        env['SINGLEPRECISION'] = 'no'

        if '+hdf5' in spec:
            env['HAVEHDF5'] = 'yes'
        else:
            env['HAVEHDF5'] = 'no'

    def install(self, spec, prefix):
        mkdir(prefix.bin)
        install('MUSIC', prefix.bin)
