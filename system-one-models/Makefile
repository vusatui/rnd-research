# System One / Jev workshops: everything runs in Docker. Host needs only Docker and make.
# Run `make help`. Config: copy .env.example to .env and add a free OPENROUTER_API_KEY.

IMAGE    ?= system-one-workshops:local
PORT     ?= 8787
# MOCK=1     -> offline keyword rules instead of the free LLM (no key, no network). Output says MOCK.
MOCK     ?=
# FALLBACK=mock (default for `make lite`) -> if the free LLM fails, that answer comes from the mock
# rules and the response is labelled MOCK-FALLBACK. Set FALLBACK= to fail loudly instead.
FALLBACK ?= mock
# MOUNT=1 (default) mounts workshop/ and workshop-lite/ read-only, so your edits apply without a rebuild.
MOUNT    ?= 1
EX       ?=
LIMIT    ?= 15
K        ?= 3
THRESHOLD ?= 0.6
PLATFORM ?=
CURL_IMAGE ?= curlimages/curl:8.17.0
EMU_NAME ?= s1-jev-emulator

ROOT := $(abspath $(dir $(lastword $(MAKEFILE_LIST))))
# First existing env file wins: ./.env, then the older per-folder ones.
ENV_FILE := $(firstword $(wildcard $(ROOT)/.env $(ROOT)/presentation/workshop-lite/.env $(ROOT)/workshop/.env))

DOCKER_ENV := $(if $(ENV_FILE),--env-file "$(ENV_FILE)") \
  -e OPENROUTER_API_KEY -e OPENROUTER_MODEL -e JEV_BASE_URL -e JEV_API_KEY -e JEV_MODEL \
  -e TYPESAFE_API_KEY -e OPENAI_API_KEY -e CLOUDFLARE_ACCOUNT_ID -e CLOUDFLARE_API_TOKEN \
  $(if $(MOCK),-e EMULATOR_MOCK=1 -e DECIDER_MOCK=1)
MOUNTS := $(if $(filter 1,$(MOUNT)),-v "$(ROOT)/workshop:/app/workshop:ro" -v "$(ROOT)/presentation/workshop-lite:/app/workshop-lite:ro")
TTY := $(shell [ -t 0 ] && echo -it)
RUN := docker run --rm --init $(TTY) $(DOCKER_ENV) $(MOUNTS)
WS  := $(RUN) -w /app/workshop $(IMAGE)

.DEFAULT_GOAL := help
.PHONY: help build image lite lite-mock emulator curl workshop ex1 ex2 ex3 ex3-sweep ex4 decider models shell test test-live ci clean

help: ## Show this help
	@echo "System One / Jev workshops (Docker + make only)"
	@echo
	@awk 'BEGIN{FS=":.*## "} /^[a-z0-9-]+:.*## /{printf "  make %-10s %s\n", $$1, $$2}' $(MAKEFILE_LIST)
	@echo
	@echo "Options: MOCK=1 (offline, no key)  FALLBACK= (no mock fallback)  EX=ticket|comment|approval"
	@echo "         LIMIT=15 K=3 (ex2)  THRESHOLD=0.6 (ex3)  PORT=8787 (emulator)  MOUNT=0 (use code baked in image)"
	@echo "Env file: $(if $(ENV_FILE),$(ENV_FILE),none found - copy .env.example to .env)"

BUILD_CMD := docker build $(if $(PLATFORM),--platform $(PLATFORM)) -f "$(ROOT)/docker/Dockerfile" -t $(IMAGE) "$(ROOT)"

build: ## Build the Docker image (pinned Python deps, amd64/arm64)
	$(BUILD_CMD)

# quiet (re)build used by the other targets; a no-op in about a second when nothing changed
image:
	@out=$$($(BUILD_CMD) -q 2>&1) || { echo "$$out"; echo "docker build failed"; exit 1; }

lite: image ## Talk demo: Jev emulator + 3 examples (EX=ticket|comment|approval)
	$(RUN) $(if $(FALLBACK),-e EMULATOR_FALLBACK=$(FALLBACK)) $(IMAGE) /app/bin/lite.sh $(EX)

lite-mock: ## Talk demo fully offline (MOCK rules, no key, no network)
	@$(MAKE) --no-print-directory lite MOCK=1

emulator: image ## Run only the Jev emulator on http://127.0.0.1:8787 (Ctrl+C stops)
	@echo "Emulator on http://127.0.0.1:$(PORT)/v1/systemone  (NOT Jev; MOCK=1 for offline rules)"
	$(RUN) --name $(EMU_NAME) -p 127.0.0.1:$(PORT):8787 $(if $(FALLBACK),-e EMULATOR_FALLBACK=$(FALLBACK)) $(IMAGE) python /app/workshop-lite/jev_emulator.py

curl: ## Plain-curl request to a running `make emulator` (curl runs in Docker)
	docker run --rm --network container:$(EMU_NAME) -v "$(ROOT)/presentation/workshop-lite/curl_example.sh:/curl_example.sh:ro" \
	  -e JEV_BASE_URL=http://127.0.0.1:8787 --entrypoint sh $(CURL_IMAGE) /curl_example.sh

workshop: image ## Deep dive: ex1, ex2, ex3 in a row (MOCK=1 for offline)
	$(WS) sh -c 'python ex1_classic_baseline/baseline.py && echo && python ex2_llm_as_decider/run.py --limit $(LIMIT) --k $(K) && echo && python ex3_cascade/cascade.py --threshold $(THRESHOLD)'

ex1: image ## Deep dive ex1: classic classifier baseline (no LLM, no key)
	$(WS) python ex1_classic_baseline/baseline.py

ex2: image ## Deep dive ex2: free LLM forced into decision shape (LIMIT, K)
	$(WS) python ex2_llm_as_decider/run.py --limit $(LIMIT) --k $(K)

ex3: image ## Deep dive ex3: confidence-gated cascade, LLM as System 2 (THRESHOLD)
	$(WS) python ex3_cascade/cascade.py --threshold $(THRESHOLD)

ex3-sweep: image ## Deep dive ex3: threshold sweep with a human queue (no LLM)
	$(WS) sh -c 'for t in 0.3 0.5 0.7 0.9; do python ex3_cascade/cascade.py --no-llm --threshold $$t | grep "^threshold"; done'

ex4: image ## Deep dive ex4: real decision APIs (skips providers without keys)
	$(WS) python ex4_decision_apis/compare.py

decider: image ## Deep dive: one decider.py call (choice + noul + score)
	$(WS) python decider.py

models: image ## List current free OpenRouter models (needs network)
	$(WS) python list_free_models.py

shell: image ## Open a shell in the container
	docker run --rm -i $(TTY) $(DOCKER_ENV) $(MOUNTS) -w /app $(IMAGE) bash

test: image ## Offline smoke tests (MOCK, --network none, no key): what CI runs
	docker run --rm --network none $(IMAGE) /app/bin/smoke.sh
	@echo "--- curl example against a MOCK emulator (no network) ---"
	@docker rm -f s1-emu-test >/dev/null 2>&1 || true
	@docker run -d --rm --name s1-emu-test --network none -e EMULATOR_MOCK=1 -e EMULATOR_HOST=127.0.0.1 $(IMAGE) python /app/workshop-lite/jev_emulator.py >/dev/null
	@for i in $$(seq 1 50); do docker exec s1-emu-test python -c "import urllib.request; urllib.request.urlopen('http://127.0.0.1:8787/health', timeout=1)" 2>/dev/null && break; sleep 0.2; done
	@out=$$($(MAKE) --no-print-directory curl EMU_NAME=s1-emu-test 2>&1); rc=$$?; docker rm -f s1-emu-test >/dev/null 2>&1; \
	  echo "$$out" | tail -1; [ $$rc -eq 0 ] && echo "$$out" | grep -q '"tone"' && echo "PASS  curl example (MOCK)" || { echo "FAIL  curl example"; exit 1; }

test-live: image ## One real call through the free OpenRouter model (needs key)
	docker run --rm $(DOCKER_ENV) $(IMAGE) /app/bin/live_check.sh

clean: ## Remove the local image
	-docker rmi $(IMAGE)
