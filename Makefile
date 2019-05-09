.PHONY: install
install:
	spack env create gizmo environments/gizmo/spack.yaml || true
	spack repo add repos/gizmo || true

.PHONY: uninstall
uninstall:
	spack env rm -y gizmo || true
	spack repo rm gizmo || true
