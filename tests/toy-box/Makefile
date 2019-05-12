GIZMO_HG_SRC ?= https://bitbucket.org/phopkins/gizmo-public
MPIRUN ?= OMP_NUM_THREADS=1 mpirun
GIZMO_RUN_MODE ?=

GIZMO_HG = gizmo_hg
GIZMO_CONFIG = gizmo_config.sh
GIZMO_PARAMS = gizmo_params.txt
GIZMO_VERSION = gizmo@local

.PHONY: compile
compile: GIZMO

GIZMO: $(GIZMO_CONFIG) $(GIZMO_HG)
	cp $(GIZMO_CONFIG) $(GIZMO_HG)/Config.sh
	spack diy -d $(GIZMO_HG) -n $(GIZMO_VERSION) && eval `spack env deactivate --sh` && spack uninstall -y $(GIZMO_VERSION)
	ln -s $(GIZMO_HG)/GIZMO $@

$(GIZMO_HG):
	hg clone $(GIZMO_HG_SRC) $@

.PHONY: run-music
run-music:
	cd ic && MUSIC music.conf

.PHONY: run-gizmo
run-gizmo:
	$(MPIRUN) ./GIZMO $(GIZMO_PARAMS) $(GIZMO_RUN_MODE)

.PHONY: purge
purge:
	rm ic/{*.bin,*.txt,snapshot}
	rm -r gizmo_hg/ output/ *.dat *-usedvalues GIZMO
