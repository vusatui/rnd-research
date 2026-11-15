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
# ex2: METHOD=all|jev|verbal|logprobs|votes|classic|strong  MODEL=<OpenRouter id>  LIMIT=<n tickets>
METHOD   ?= all
MODEL    ?=
LIMIT    ?=
# ex3 economics: S1/S2 = an ex2 result name (or S2=human), ERROR_COST/REVIEW in $
S1       ?= jev
S2       ?= human
ERROR_COST ?= 5
REVIEW   ?= 0.5
QUESTION ?= department
# budget guard for every paid run (stops the run when exceeded)
MAX_SPEND_USD ?= 0.05
PLATFORM ?=
CURL_IMAGE ?= curlimages/curl:8.17.0
EMU_NAME ?= s1-jev-emulator

ROOT := $(abspath $(dir $(lastword $(MAKEFILE_LIST))))
# First existing env file wins: ./.env, then the older per-folder ones.
ENV_FILE := $(firstword $(wildcard $(ROOT)/.env $(ROOT)/presentation/workshop-lite/.env $(ROOT)/workshop/.env))

DOCKER_ENV := $(if $(ENV_FILE),--env-file "$(ENV_FILE)") \
  -e OPENROUTER_API_KEY -e OPENROUTER_MODEL -e JEV_BASE_URL -e JEV_API_KEY -e JEV_MODEL \
  -e TYPESAFE_API_KEY -e OPENAI_API_KEY -e CLOUDFLARE_ACCOUNT_ID -e CLOUDFLARE_API_TOKEN \
  -e MAX_SPEND_USD=$(MAX_SPEND_USD) \
  $(if $(MOCK),-e EMULATOR_MOCK=1 -e WORKSHOP_MOCK=1)
MOUNTS := $(if $(filter 1,$(MOUNT)),-v "$(ROOT)/workshop:/app/workshop:ro" -v "$(ROOT)/workshop/results:/app/workshop/results" -v "$(ROOT)/presentation/workshop-lite:/app/workshop-lite:ro")
TTY := $(shell [ -t 0 ] && echo -it)
RUN := docker run --rm --init $(TTY) $(DOCKER_ENV) $(MOUNTS)
WS  := $(RUN) -w /app/workshop $(IMAGE)

.DEFAULT_GOAL := help
.PHONY: help build image lite lite-mock lite-jev ex1 emulator curl workshop ex2 ex2-estimate eval ex3 homework dataset models shell test test-live ci clean

help: ## Show this help
	@echo "System One / Jev workshops (Docker + make only)"
	@echo
	@awk 'BEGIN{FS=":.*## "} /^[a-z0-9-]+:.*## /{printf "  make %-10s %s\n", $$1, $$2}' $(MAKEFILE_LIST)
	@echo
	@echo "Options: MOCK=1 (offline, no key; ex2 re-scores the committed results)  EX=ticket|comment|approval"
	@echo "         METHOD=all MODEL= LIMIT= (ex2)  S1=jev S2=human ERROR_COST=5 REVIEW=0.5 (ex3)  MAX_SPEND_USD=0.05"
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

lite-jev: image ## Ex1 against REAL Jev via OpenRouter (same client, paid, ~$0.00002/request)
	$(RUN) -e JEV_BASE_URL=https://openrouter.ai/api -e JEV_MODEL=jev-latest $(IMAGE) sh -c 'JEV_API_KEY=$$OPENROUTER_API_KEY /app/bin/lite.sh $(EX)'

ex1: lite ## Exercise 1 = the lite demo: one request, several questions, thresholds per action

emulator: image ## Run only the Jev emulator on http://127.0.0.1:8787 (Ctrl+C stops)
	@echo "Emulator on http://127.0.0.1:$(PORT)/v1/systemone  (NOT Jev; MOCK=1 for offline rules)"
	$(RUN) --name $(EMU_NAME) -p 127.0.0.1:$(PORT):8787 $(if $(FALLBACK),-e EMULATOR_FALLBACK=$(FALLBACK)) $(IMAGE) python /app/workshop-lite/jev_emulator.py

curl: ## Plain-curl request to a running `make emulator` (curl runs in Docker)
	docker run --rm --network container:$(EMU_NAME) -v "$(ROOT)/presentation/workshop-lite/curl_example.sh:/curl_example.sh:ro" \
	  -e JEV_BASE_URL=http://127.0.0.1:8787 --entrypoint sh $(CURL_IMAGE) /curl_example.sh

workshop: image ## Exercises 2 + 3 from the committed results (no key needed)
	$(WS) sh -c 'WORKSHOP_MOCK=1 python ex2_confidence/run.py && echo && python eval.py --reliability && echo && python ex3_fast_first/economics.py'

ex2-estimate: image ## Ex2: $ estimate for METHOD/LIMIT, no calls
	$(WS) python ex2_confidence/run.py --method $(METHOD) $(if $(MODEL),--model $(MODEL)) $(if $(LIMIT),--limit $(LIMIT)) --estimate

ex2: image ## Ex2: verbalized vs computed confidence on 150 tickets (paid, ~$0.03; MOCK=1 replays)
	$(WS) python ex2_confidence/run.py --method $(METHOD) $(if $(MODEL),--model $(MODEL)) $(if $(LIMIT),--limit $(LIMIT))

eval: image ## Score every results/ex2_*.jsonl: accuracy, ECE, reliability, auto@95, cost (QUESTION=department|urgency)
	$(WS) python eval.py --reliability --question $(QUESTION)

ex3: image ## Ex3: fast-first economics, threshold sweep (S1, S2, ERROR_COST, REVIEW)
	$(WS) python ex3_fast_first/economics.py --s1 $(S1) --s2 $(S2) --error-cost $(ERROR_COST) --review $(REVIEW)

homework: image ## Homework: same ticket to every decision API you have a key for
	$(WS) python homework/compare_apis.py

dataset: image ## Regenerate data/tickets.jsonl (free generator + labellers; see data/DATASET.md)
	$(RUN) -v "$(ROOT)/workshop/data:/app/workshop/data" -w /app/workshop $(IMAGE) python data/make_dataset.py

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
