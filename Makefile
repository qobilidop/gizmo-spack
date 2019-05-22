.PHONY: install
install:
	-spack env create gizmo environments/gizmo/spack.yaml
	-spack repo add repos/gizmo

.PHONY: uninstall
uninstall:
	-spack env rm -y gizmo
	-spack repo rm gizmo
