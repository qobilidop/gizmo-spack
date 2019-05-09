from spack.pkg.gizmo.gizmo import Gizmo


class GizmoDeps(Gizmo):
    """A dummy package to install GIZMO dependencies."""

    # Disable all phases to install dependencies only
    phases = []
