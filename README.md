# GIZMO Spack
[GIZMO](http://www.tapir.caltech.edu/~phopkins/Site/GIZMO.html) simulation software stack through [Spack](https://spack.io)

## About

This project provides relevant files to set up a curated software stack, centering around GIZMO, on various HPC sites through Spack.

## Layout

- `configs`: Example Spack [configuration files](https://spack.readthedocs.io/en/latest/configuration.html) (`compilers.yaml` and `packages.yaml`) for various HPC sites.
    - [`bridges`](https://www.psc.edu/bridges)
    - [`stampede2`](https://www.tacc.utexas.edu/systems/stampede2)
    - [`tscc`](https://www.sdsc.edu/services/hpc/hpc_systems.html#tscc)
- `environments`: Example Spack [environments](https://spack.readthedocs.io/en/latest/environments.html).
    - `gizmo-deps`
    - `gizmo-grackle`
- `repos/gizmo`: The `gizmo` Spack [package repository](https://spack.readthedocs.io/en/latest/repositories.html).
    - `packages`
        - `ahf-gizmo`: AMIGA halo finder configured for GIZMO simulations.
        - `gizmo`: A flexible, massively-parallel, multi-physics simulation code.
        - `gizmo-deps`: A dummy package to install GIZMO dependencies.
        - `grackle`: Grackle is a chemistry and radiative cooling library for astrophysical simulations and models.
        - `music`: Multi-Scale Initial Conditions for Cosmological Simulations.

## Usage

### Spack setup

First, you need to [set up Spack](https://spack.readthedocs.io/en/latest/getting_started.html). Then clone this repository somewhere and change to that directory:
```
git clone https://github.com/qobilidop/gizmo-spack.git
cd gizmo-spack
```

If you are working on an HPC site, the example configuration files might be helpful. They could be used directly by symlinking (or copying) to the `~/.spack` directory (assuming we are on Stampede2):
```console
ln -s "$PWD"/configs/stampede2/* ~/.spack/
```

Or used indirectly as references.

### Package repository installation

To install the `gizmo` package repository:
```console
spack repo add repos/gizmo
```

To check if the `gizmo` package repository is installed:
```console
spack repo list
```

You could also check individual package's information:
```console
spack info gizmo
```

To uninstall the `gizmo` package repository:
```console
spack repo rm gizmo
```
