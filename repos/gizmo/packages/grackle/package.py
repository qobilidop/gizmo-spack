# The official grackle package is referenced:
# https://github.com/spack/spack/blob/master/var/spack/repos/builtin/packages/grackle/package.py
# But we prefer to have this critical software in full control here.

import os.path
import inspect

from spack import *


class Grackle(Package):
    """Grackle is a chemistry and radiative cooling library for astrophysical
    simulations and models.
    """
    homepage = 'http://grackle.readthedocs.io/'
    url = 'https://github.com/grackle-project/grackle/archive/grackle-3.1.1.tar.gz'

    version('3.1.1', sha256='44025faba2ddcd056d75bdece5b3421eb5e5f703a8288ef48e64d3fa2eb7eda1')
    version('3.1', sha256='5705985a70d65bc2478cc589ca26f631a8de90e3c8f129a6b2af69db17c01079')
    version('3.0', sha256='41e9ba1fe18043a98db194a6f5b9c76a7f0296a95a457d2b7d73311195b7d781')
    version('2.2', sha256='5855cb0f93736fd8dd47efeb0abdf36af9339ede86de7f895f527513566c0fae')
    version('2.1', sha256='0a65628f6f40735dc55fcaf7faf938f4ee95350eb8da94c2f3c1dc13f5899930')
    version('2.0.1', sha256='bcdf6b3ff7b7515ae5e9f1f3369b2690ed8b3c450040e92a03e40582f57a0864')
    version('2.0', sha256='df0b9391d38af7f2e74279bb26ef7bfe38e60a32b37ccdc8e74d00aa3b441f48')
    version('1.1', sha256='24dad78a117f166bf102f960147ed70a533f37c7e01f6bad259a875c9a59fd83')
    version('1.0', sha256='eb5ef43748661b0deaf6fe71521cf2bdfffae0269d3f70ca4d2f499c16583590')

    variant('float', default=False, description='Build with float')

    depends_on('hdf5~mpi')
    depends_on('libtool')

    parallel = False

    def install(self, spec, prefix):
        template_name = '{0.architecture}-{0.compiler.name}'
        grackle_architecture = template_name.format(spec)
        substitutions = {
            '@ARCHITECTURE': grackle_architecture,
            '@OMPFLAGS': self.compiler.openmp_flag,
            '@PREFIX': prefix,
        }

        template = join_path(
            os.path.dirname(inspect.getmodule(self).__file__),
            'Make.mach.template'
        )
        makefile = join_path(
            self.stage.source_path,
            'src',
            'clib',
            'Make.mach.{0}'.format(grackle_architecture)
        )
        copy(template, makefile)
        for key, value in substitutions.items():
            filter_file(key, value, makefile)

        configure()
        with working_dir('src/clib'):
            make('clean')
            make('machine-{0}'.format(grackle_architecture))
            make('opt-high')
            if spec.satisfies("+float"):
                make('precision-32')
            make('show-config')
            make()
            mkdirp(prefix.lib)
            make('install')
