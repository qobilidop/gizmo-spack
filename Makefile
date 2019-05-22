THIS_DIR = $(PWD)
SPACK_ROOT = $(shell spack location -r)
$(info We are at $(THIS_DIR))
$(info Using spack installed at $(SPACK_ROOT))

.PHONY: install
install:
	cd $(SPACK_ROOT) && git stash && git apply -v $(THIS_DIR)/spack.patch
	-spack env create gizmo environments/gizmo/spack.yaml
	-spack repo add repos/gizmo

.PHONY: uninstall
uninstall:
	-spack env rm -y gizmo
	-spack repo rm gizmo
