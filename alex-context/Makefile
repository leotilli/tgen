#
# Experiment management for Tgen
#

# Environment settings
SHELL = /bin/bash
TGEN = ../run_tgen.py
MEM = 8g
QP = --engine=slurm  # XXX you need to update your qsubmit settings here!
ifdef LOCAL
  QP = --engine=console
endif
QSUBMIT = qsubmit --logdir '$(TRY_DIR)' --mem $(MEM) --jobname T.$(TRY_NUM).$(RUN_NAME) $(QP) $(QHOLD)# using OB's qsubmit script
ifdef PYPY
  ACTIVATE = source ~/work/tools/virtualenv-pypy-x86_64/bin/activate
else
  ACTIVATE = echo -n
endif
ifdef DEBUG
  DEBUG_LOG_TRAIN = -d $(TRY_DIR)/train.debug-log.txt.gz
  DEBUG_LOG_GEN = -d $(TRY_DIR)/gen.debug-log.txt
endif
ifdef DEBUG_GEN
  DEBUG_LOG_GEN = -d $(TRY_DIR)/gen.debug-log.txt
endif
MTEVAL = ../util/mteval-v11b.pl
POSTPROCESS = ./postprocess/postprocess.py
AVERAGE_SCORES = ../util/average_scores.pl
GREP_SCORES = ../util/grep_scores.pl --bleu-range=62:70 --nist-range=6:8
DESC_EXP = ../util/describe_experiment.pl
LOG_CUTOFF= 10000
NUM_EXP = 20  # number of experiments to list in `make desc'

LOGFILES = $$file/T.* $$file/{asearch_gen.,gen.,seq2seq_gen.,}log.txt # logfile pattern to use for score printing
SCOREFILE = SCORE

# Runs directories
RUNS_DIR  := runs# main directory for experiment outputs
TRY_NUM   := $(shell perl -e '$$m=0; for(<$(RUNS_DIR)/*>){/\/(\d+)_/ and $$1 > $$m and $$m=$$1;} printf "%03d", $$m+1;')# experiment number
RUN_NAME  := experiment# default name, to be overridden by targets
DATE      := $(shell date +%Y-%m-%d_%H-%M-%S)
TRY_DIR    = $(RUNS_DIR)/$(TRY_NUM)_$(DATE)_$(RUN_NAME)# experiment output directory
TRAINING_SET := training2

ifdef D # Shortcut D -> DESC
  DESC := $(D)
endif
ifdef J # Shortcut J -> JOBS
  JOBS := $(J)
endif

ifdef JOBS
  PARALLEL := -j $(JOBS) -e "T.$(TRY_NUM)"
endif

# Input data file defaults

SEQ2SEQ_CONFIG = config/seq2seq.py
ASEARCH_CONFIG = config/asearch.py
CLASSIF_CONFIG = config/classif.py
TRAIN_PORTION = 1.0
TRAIN_DAS = data/$(TRAINING_SET)/train-das.txt
TRAIN_TREES = data/$(TRAINING_SET)/train-text.pickle.gz
TRAIN_ABSTR = data/$(TRAINING_SET)/train-abst.txt
TRAIN_CONC = data/$(TRAINING_SET)/train-conc.sgm
TRAIN_CONTEXT = data/$(TRAINING_SET)/train-context.pickle.gz
TRAIN_CONTEXTTOKS = data/$(TRAINING_SET)/train-context.txt
TRAIN_TOKS = data/$(TRAINING_SET)/train-text.txt
GRAMMATEMES = data/$(TRAINING_SET)/grammatemes.tsv
TEST_DAS = data/$(TRAINING_SET)/devel-das.txt
TEST_REF = data/$(TRAINING_SET)/devel-das.sgm
TEST_TREES = data/$(TRAINING_SET)/devel-text.pickle.gz
TEST_ABSTR = data/$(TRAINING_SET)/devel-abst.txt
TEST_CONC = data/$(TRAINING_SET)/devel-conc.sgm
TEST_CONTEXT = data/$(TRAINING_SET)/devel-context.pickle.gz
TEST_TOKS = data/$(TRAINING_SET)/devel-text.txt
TEST_CONTEXTTOKS = data/$(TRAINING_SET)/devel-context.txt
TEST_REFTOKS = data/$(TRAINING_SET)/devel-ref.txt
ifdef EVAL_TEST
  TEST_DAS = data/$(TRAINING_SET)/test-das.txt
  TEST_REF = data/$(TRAINING_SET)/test-das.sgm
  TEST_TREES = data/$(TRAINING_SET)/test-text.pickle.gz
  TEST_ABSTR = data/$(TRAINING_SET)/test-abst.txt
  TEST_CONC = data/$(TRAINING_SET)/test-conc.sgm
  TEST_CONTEXT = data/$(TRAINING_SET)/test-context.pickle.gz
  TEST_TOKS = data/$(TRAINING_SET)/test-text.txt
  TEST_CONTEXTTOKS = data/$(TRAINING_SET)/test-context.txt
  TEST_REFTOKS = data/$(TRAINING_SET)/test-ref.txt
  VALID_DAS = data/$(TRAINING_SET)/devel-das.txt
  VALID_TREES = data/$(TRAINING_SET)/devel-text.pickle.gz
  VALID_CONTEXT = data/$(TRAINING_SET)/devel-context.pickle.gz
  VALID_TOKS = data/$(TRAINING_SET)/devel-text.txt
  VALID_CONTEXTTOKS = data/$(TRAINING_SET)/devel-context.txt
  VALID_REFTOKS = data/$(TRAINING_SET)/devel-ref.txt
endif
SURFACE_SCEN = ../bagel-data/surface/en_synthesis.scen

XS_INSTEAD = 0
EVAL_SELECTOR = ref0
TARGET_SELECTOR = gen

# Help text

define HELP_MESSAGE
Tgen experiments
================

make desc [NUM_EXP=20] [REFRESH=1]
* List experiments with descriptions and (possibly) scores.
* Change NUM_EXP if you need to see more than 20 latest results.
* Refresh scores to obtain new results by setting REFRESH=1 (makes it slower).

make seq2seq_cv_run J=[XX] D='Description'
* Run an experiment where seq2seq
  training is directly followed by testing generation.
  - set RANDS=1 to use 5 different random seeds (and average the results)
  - set EVAL_TEST=1 to evaluate on test data instead of development data

make score-XXX
* Retrieve a score for run without RANDS.

make cv_score-XXX
* Retrieve a score for run with RANDS.
---

Use QP='--console' if you want the job to run interactively instead
of submitting to the cluster.

Use ACTIVATE='source path/to/virtualenv/bin/activate' to run
within a Virtualenv instead of the default Python.

Use PYPY=1 to activate the preset PyPy Virtualenv.

Use DEBUG=1 to activate debugging outputs. Use DEBUG_GEN=1 to activate
debugging only for testing (in CV runs).
endef
export HELP_MESSAGE

#
# Targets
#

# Auxiliary targets

help:
	@echo "$$HELP_MESSAGE" | egrep --color '^(\s*make.*|)'

# List all experiments, find scores in logs (of various versions)
desc:
	@ls -d $(RUNS_DIR)/* | sort | tail -n $(NUM_EXP) | while read file; do \
		if [[ -f $$file/$(SCOREFILE) && -z "$(REFRESH)" ]]; then \
			cat $$file/$(SCOREFILE) ; \
			continue ; \
		fi ; \
		echo -ne $$file ":\t" | sed 's/runs\///;s/_/\t/;s/_/ /;s/_/\t/' > $$file/$(SCOREFILE);  \
		$(GREP_SCORES) $(LOGFILES) >> $$file/$(SCOREFILE) ; \
		echo -ne '    ' >> $$file/$(SCOREFILE) ; \
		cat $$file/ABOUT | tr  '\n' ' ' >> $$file/$(SCOREFILE); \
		echo >> $$file/$(SCOREFILE); \
		cat $$file/$(SCOREFILE); \
	done

printvars:
	$(foreach V, $(sort $(.VARIABLES)), $(if $(filter-out environment% default automatic, $(origin $V)), $(info $V=$($V) ($(value $V)))))

printgit:
	@git status
	@echo -e "\n*** *** ***\n"
	@git log --pretty=format:"%h - %an, %ar : %s" -1
	@echo -e "\n*** *** ***\n"
	@git diff


prepare_dir:
	# create the experiment directory, print description and git version
	mkdir -p $(TRY_DIR)
	if [[ "$(RUN_TYPE)" == "seq2seq" ]]; then \
		CONFIG=$(SEQ2SEQ_CONFIG) ; \
	else \
		CONFIG=$(PERCRANK_CONFIG) ; \
	fi; \
	[[ -n "$(DEBUG)" || -n "$(DEBUG_GEN)" ]] && DEBUG_SETTING=-d ; \
	[[ -n "$(RANDS)" ]] && RANDS_SETTING=-r ; \
	[[ -n "$(EVAL_TEST)" ]] && EVAL_SETTING=-e ; \
	$(DESC_EXP) -t "$(TRAINING_SET)" -p "$(TRAIN_PORTION)" -j "$(JOBS)" -c "$(CV_NUMS)" $$EVAL_SETTING $$DEBUG_SETTING $$RANDS_SETTING $$CONFIG > $(TRY_DIR)/ABOUT ; \
	echo "$(DESC)" >> $(TRY_DIR)/ABOUT
	make printvars > $(TRY_DIR)/VARS
	make printgit > $(TRY_DIR)/GIT_VERSION

# Main targets

asearch_cv_run: RUN_TYPE := asearch
asearch_cv_run: cv_run

seq2seq_cv_run: RUN_TYPE := seq2seq
seq2seq_cv_run: cv_run

cv_run: RUN_NAME := cv_run
cv_run: prepare_dir
cv_run:
	if [[ -n "$(RANDS)" ]]; then \
		SEEDS=(s0 s1 s2 s3 s4); \
	else \
		SEEDS=(""); \
	fi; \
	for SEED in "$${SEEDS[@]}"; do \
		TRAIN_RUN=seq2seq_train ; \
		TEST_RUN=seq2seq_gen_cv ; \
		make $$TRAIN_RUN TRY_DIR=$(TRY_DIR)/$$SEED SEED=$$SEED TRY_NUM=$(TRY_NUM) 2>&1 | tee -a $(TRY_DIR)/cv.log.txt ; \
		JOB_NUM=`cat $(TRY_DIR)/cv.log.txt | grep '^Your job' | tail -n 1 | sed 's/^Your job \([0-9]\+\).*/\1/;' ` ; \
		if [[ -n "$$JOB_NUM" ]]; then \
		    JOB_NUM="--hold $$JOB_NUM"; \
		fi; \
		make $$TEST_RUN TRY_DIR=$(TRY_DIR)/$$SEED TRY_NUM=$(TRY_NUM) QP="$(QP)" QHOLD="$$JOB_NUM"; \
	done

cv_score-%:
	$(eval TRY_DIR := $(shell ls -d $(RUNS_DIR)/$**))
	$(eval TRY_NUM := $*)
	make cv_score TRY_DIR=$(TRY_DIR) TRY_NUM=$(TRY_NUM)

cv_score:
	$(AVERAGE_SCORES) $(TRY_DIR)/*/T.*.*_gen.o* | tee $(TRY_DIR)/gen.log.txt

score-%:
	$(eval TRY_DIR := $(shell ls -d $(RUNS_DIR)/$**))
	$(eval TRY_NUM := $*)
	make score TRY_DIR=$(TRY_DIR) TRY_NUM=$(TRY_NUM)

score:
	$(AVERAGE_SCORES) $(TRY_DIR)/T.*.*_gen.o* | tee $(TRY_DIR)/gen.log.txt

seq2seq_train: RUN_NAME := seq2seq_train
seq2seq_train: RUN_TYPE := seq2seq
seq2seq_train: prepare_dir
seq2seq_train:
	# copy needed files (to ensure replication), then run the experiment
	cp $(SEQ2SEQ_CONFIG) $(TRY_DIR)/seq2seq_config.py
	cp $(TRAIN_DAS) $(TRY_DIR)/train-das.txt
	if [[ -n "$(TOKS)" ]]; then \
		cp $(TRAIN_TOKS) $(TRY_DIR)/train-text.txt; \
		cp $(TRAIN_CONTEXTTOKS) $(TRY_DIR)/train-context.txt; \
		TRAIN_DATA=$(TRY_DIR)/train-text.txt ; \
		TRAIN_CONTEXTDATA=$(TRY_DIR)/train-context.txt ; \
	else \
		cp $(TRAIN_TREES) $(TRY_DIR)/train-text.pickle.gz; \
		cp $(TRAIN_CONTEXT) $(TRY_DIR)/train-context.pickle.gz; \
		TRAIN_DATA=$(TRY_DIR)/train-text.pickle.gz ; \
		TRAIN_CONTEXTDATA=$(TRY_DIR)/train-context.pickle.gz; \
	fi; \
	if [[ -n "$(EVAL_TEST)" ]]; then \
		cp $(VALID_DAS) $(TRY_DIR)/devel-das.txt ; \
		if [[ -n "$(TOKS)" ]]; then \
		    cp $(VALID_TOKS) $(TRY_DIR)/devel-text.txt ; \
		    cp $(VALID_CONTEXTTOKS) $(TRY_DIR)/devel-context.txt ; \
		    VALID_DATA_SPEC="-v \"$(TRY_DIR)/devel-das.txt,$(TRY_DIR)/devel-text.txt,$(TRY_DIR)/devel-context.txt\""; \
		else \
		    cp $(VALID_TREES) $(TRY_DIR)/devel-text.pickle.gz ; \
		    cp $(VALID_CONTEXT) $(TRY_DIR)/devel-context.pickle.gz ; \
		    VALID_DATA_SPEC="-v \"$(TRY_DIR)/devel-das.txt,$(TRY_DIR)/devel-text.pickle.gz,$(TRY_DIR)/devel-context.pickle.gz\""; \
		fi; \
	fi; \
	$(QSUBMIT) '$(ACTIVATE); \
		$(TGEN) seq2seq_train $(DEBUG_LOG_TRAIN) \
		-s $(TRAIN_PORTION) $(PARALLEL) -r "$(SEED)" \
		-c '"$$TRAIN_CONTEXTDATA"' '"$$VALID_DATA_SPEC"' \
		$(TRY_DIR)/seq2seq_config.py $(TRY_DIR)/train-das.txt '"$$TRAIN_DATA"' \
		$(TRY_DIR)/seq2seq.pickle.gz' 2>&1 | tee $(TRY_DIR)/seq2seq_train.log.txt

seq2seq_gen_cv:
	make prepare_test_data TRY_DIR=$(TRY_DIR)
	make seq2seq_gen_process TRY_DIR=$(TRY_DIR) TRY_NUM=$(TRY_NUM) QP="$(QP)" QHOLD="$(QHOLD)"

prepare_test_data:
	cp $(TEST_DAS) $(TRY_DIR)/test-das.txt
	cp $(TEST_ABSTR) $(TRY_DIR)/test-abstr.txt
	if [[ -n "$(TOKS)" ]]; then \
		cp $(TEST_REFTOKS) $(TRY_DIR)/test-ref.txt ; \
		cp $(TEST_TOKS) $(TRY_DIR)/test-text.txt ; \
		cp $(TEST_CONTEXTTOKS) $(TRY_DIR)/test-context.txt ; \
	else \
		cp $(TEST_REF) $(TRY_DIR)/test-das.sgm ; \
		cp $(TEST_TREES) $(TRY_DIR)/test-text.pickle.gz ; \
	        cp $(GRAMMATEMES) $(TRY_DIR)/grammatemes.tsv ; \
	        cp $(TEST_CONC) $(TRY_DIR)/test-conc.sgm ; \
		cp $(TEST_CONTEXT) $(TRY_DIR)/test-context.pickle.gz ; \
	fi

seq2seq_gen_process: RUN_NAME := seq2seq_gen
seq2seq_gen_process: GEN_MODEL := $(TRY_DIR)/seq2seq.pickle.gz
seq2seq_gen_process: SELECTOR_CONFIG := -r "$(EVAL_SELECTOR)" -t "$(TARGET_SELECTOR)"
seq2seq_gen_process: GEN_CONFIG :=
seq2seq_gen_process: gen_process

gen_process:
	# run just the generator, or generator + Treex + mteval.
	if [[ -n "$(TOKS)" ]]; then \
		$(QSUBMIT) '$(ACTIVATE); \
		    $(TGEN) $(RUN_NAME) -e $(TRY_DIR)/test-ref.txt $(DEBUG_LOG_GEN) \
		    -a $(TRY_DIR)/test-abstr.txt \
		    -c $(TRY_DIR)/test-context.txt \
		    -w $(TRY_DIR)/out-toks.txt $(GEN_CONFIG) \
		    $(GEN_MODEL) $(TRY_DIR)/test-das.txt;' \
		    2>&1 | tee $(TRY_DIR)/$(RUN_NAME).log.txt ; \
	else \
	    $(QSUBMIT) '$(ACTIVATE); \
		    $(TGEN) $(RUN_NAME) -e $(TRY_DIR)/test-text.pickle.gz $(DEBUG_LOG_GEN) \
		    $(SELECTOR_CONFIG) \
		    -c $(TRY_DIR)/test-context.pickle.gz \
		    -w $(TRY_DIR)/out-trees.yaml.gz $(GEN_CONFIG) \
		    $(GEN_MODEL) $(TRY_DIR)/test-das.txt; \
		    treex -Len -Sgen Read::YAML from=$(TRY_DIR)/out-trees.yaml.gz \
			    T2T::AssignDefaultGrammatemes grammateme_file=$(TRY_DIR)/grammatemes.tsv da_file=$(TRY_DIR)/test-das.txt \
			    Misc::DeabstractDialogueSlots abstraction_file=$(TRY_DIR)/test-abstr.txt xs_instead=$(XS_INSTEAD) skip_factor=3 \
			    $(SURFACE_SCEN) Write::Treex \
			    Util::Eval document="$$.set_path(\"\"); $$.set_file_stem(\"test\");" \
			    Write::SgmMTEval to=$(TRY_DIR)/out-text.sgm set_id=AlexContext sys_id=TGEN add_header=tstset; \
		    $(POSTPROCESS) $(TRY_DIR)/out-text.sgm; \
		    $(MTEVAL) -s $(TRY_DIR)/test-das.sgm -r $(TRY_DIR)/test-conc.sgm -t $(TRY_DIR)/out-text.sgm' \
		    2>&1 | tee $(TRY_DIR)/$(RUN_NAME).log.txt ; \
	fi

# Rerun an experiment (TRY_DIR, TRY_NUM, RUN_NAME must be set!)
rerun:
	LAST_LOGFILE=`ls -t $(TRY_DIR)/T.*.$(RUN_NAME).* | head -n 1` ; \
	COMMAND=`cat $$LAST_LOGFILE | sed '1,/^== Directory/d;/^== Hard res/,$$d;s/^== Command:\s*//;'` ; \
	echo "Rerunning command: $$COMMAND"; \
	$(QSUBMIT) "$$COMMAND" 2>&1 | tee -a $(TRY_DIR)/$(RUN_NAME).log.txt ;

