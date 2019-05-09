from spack import *


class GizmoDeps(Package):
    """A dummy package to install GIZMO dependencies."""

    homepage = "http://www.tapir.caltech.edu/~phopkins/Site/GIZMO.html"

    version('public', hg='https://bitbucket.org/phopkins/gizmo-public')

    variant('hdf5', default=True)
    variant('grackle', default=False)

    depends_on('mpi')
    depends_on('gsl')
    depends_on('fftw-api@2')
    depends_on('fftw+mpi')
    depends_on('hdf5', when='+hdf5')
    depends_on('grackle', when='+grackle')

    phases = []
