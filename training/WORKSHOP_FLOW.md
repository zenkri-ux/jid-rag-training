# Workshop Flow — Instructor Live Console

Keep this document open during delivery. Commands assume the repository root. Switch stages from the **Workshop journey** rail; the selected stage takes effect on the next message without editing `.env` or rebuilding.

## Before students arrive

**Time:** 15–30 minutes before.  
**Explain:** nothing yet; make the room reliable.  
**Execute:** copy `.env.example` to `.env`, keep `ASSISTANT_STAGE=basic`, then `docker compose up --build`. Open `/`, `/health`, `/docs`, and `/debug/retrieval`.  
**Expected:** health returns `status=ok`; UI shows `stage: basic`; Qdrant is healthy.  
**If not:** use `docker compose ps` and `docker compose logs assistant-api`; fall back to `DEMO_MODE=true`.  
**Takeaway:** infrastructure failures are not part of this workshop.

## Session 1 (90 minutes)

### 1. AI to neural networks

**Time:** 0–22 min.  
**Explain:** AI ⊃ ML ⊃ deep learning; inputs, weights, layers, activations, outputs; training versus inference. Draw the three-input career-fit toy network from `session-1.md`.  
**Ask students:** “Did a 500-rule program learn? During inference, which weights change?”  
**Expected:** students separate broad AI, learned patterns, and fixed-weight inference.  
**Concept:** neural-network intuition.  
**Key takeaway:** training learns parameters; inference applies them.

### 2. LLM mental model

**Time:** 22–40 min.  
**Explain:** tokens, next-token prediction, conceptual transformer attention, finite context, temperature, and hallucination.  
**Ask:** “Does the model search its training files when answering?”  
**Expected:** no; it computes from learned parameters plus current context.  
**Concept:** model knowledge versus context versus external knowledge.  
**Key takeaway:** plausibility and factual correctness are different targets.

### 3. Prompt engineering

**Time:** 40–55 min.  
**Explain:** instructions, simulated role, context, constraints, output contract, examples, decomposition; message-layer priority and retrieved text as untrusted data.  
**Ask:** improve `You are an assistant that helps engineering students` on the board.  
**Expected:** clarification, uncertainty, citations, and anti-fabrication boundaries emerge.  
**Concept:** prompting as interface and policy design.  
**Key takeaway:** prompts shape behavior but cannot manufacture evidence or guarantee compliance.

### 4. RAG discovered from a failure

**Time:** 55–75 min.  
**Ask:** “According to our private guide, what should a junior data engineer learn?”  
**Expected:** the base model cannot reliably know. Students suggest supplying documents, then notice that supplying all documents will not scale.  
**Explain:** preprocessing → chunks → embeddings → Qdrant → retrieval → context → generation.  
**Ask:** “What does a similarity score certify?”  
**Expected:** similarity only, not truth.  
**Concept:** RAG and document quality.  
**Key takeaway:** retrieval supplies candidate evidence; it does not eliminate hallucination.

### 5. Architecture handoff

**Time:** 75–90 min.  
**Explain:** walk through the architecture Mermaid diagram and map every box to a repository directory.  
**Ask students:** predict where a failure could occur for a wrong cited answer.  
**Expected:** source, parsing, chunking, embedding, filtering, orchestration, generation, or validation.  
**Command:** `docker compose up --build`, then `curl http://localhost:8000/health`.  
**Concept:** layered assistant architecture.  
**Key takeaway:** each component gives us a testable boundary.

## Session 2 (90 minutes)

### 0. Start and orient

**Time:** 0–8 min.  
**Explain:** today is a debugging loop, not a feature tour. Show UI, source panel, `/docs`, and code map.  
**Students execute:** setup commands from README and health check.  
**Expected:** UI works in `basic`; source panel is empty.  
**Ask after:** “Why is a deliberately weak assistant more useful to begin with?”  
**Concept:** controlled baseline.  
**Takeaway:** improvements need a reproducible before-state.

### 1. Baseline without provenance

**Time:** 8–18 min.  
**Students ask:** “I'm studying computer engineering and enjoy Python. Which fields could fit me?”  
**Expected:** generic plausible guidance; no sources.  
**Ask after:** “Where did each claim come from, and which can we trust?”  
**Concept:** model knowledge, hallucination, evidence.  
**Modification:** collect requirements on the board; do not switch yet.  
**Takeaway:** fluent is not the same as traceable.

### 2. Engineer the behavior contract

**Time:** 18–30 min.  
**Students test:** “What is the objectively best engineering career?” and “Give exact local demand for AI engineers.”  
**Expected:** the weak prompt lacks boundaries.  
**Ask:** “Which instruction would make this behavior testable?”  
**Modify:** click **Better instructions** in the Workshop journey. Inspect `ENGINEERING_PROMPT`.  
**Retest:** identical prompts.  
**Expected improvement:** uncertainty, non-absolute guidance, or appropriate lack-of-evidence statement.  
**Concept:** system/application instructions and output behavior.  
**Takeaway:** better behavior still does not provide private facts.

### 3. Knowledge gap, then too much knowledge

**Time:** 30–42 min.  
**Students ask:** “According to our engineering career guide, which technologies are recommended for an entry-level data engineer?”  
**Expected at `instructions`:** cannot verify the private guide.  
**Ask:** “How can the application give the model this information?”  
**Modify:** click **Knowledge context** in the Workshop journey.  
**Retest:** answer can use the guide.  
**Ask after:** “What breaks with 1,000 documents? Which irrelevant document also entered the prompt?”  
**Concept:** context limits, relevance, cost, distraction.  
**Takeaway:** external knowledge needs selection.

### 4. Add and inspect RAG

**Time:** 42–58 min.  
**Modify:** click **Basic RAG** in the Workshop journey. The index was prepared at startup.  
**Students ask:** “I like programming but also want to work close to hardware.”  
**Execute:** `curl "http://localhost:8000/debug/retrieval?q=programming%20close%20to%20hardware"`.  
**Expected:** ranked source chunks including embedded or adjacent material; UI shows citations.  
**Ask after:** “If the right fact exists but is not in top-k, can the LLM use it? Is score answer confidence?”  
**Concept:** chunks, embeddings, Qdrant, top-k, context injection.  
**Modification:** inspect `chunker.py`, `TOP_K`, and retrieved text; change one parameter only if time allows, reindex, retest.  
**Takeaway:** inspect retrieval before blaming generation.

### 5. Improve evidence quality and retrieval policy

**Time:** 58–74 min.  
**Students inspect:** the bad mixed document and clean role documents. Debug-query `software electronics data robots cloud career`. Then ask “What technologies are currently emphasized for junior data engineers?”  
**Expected at `rag`:** unhelpful chunk boundaries and/or mixed old/new evidence are visible.  
**Ask after:** “Which failure came from the model? Which came from documents or selection policy?”  
**Explain:** headings, chunk scope, overlap, role/seniority/year/authority metadata, and transparent conflict handling.  
**Modify:** click **Better retrieval** in the Workshop journey.  
**Retest:** same current-junior query.  
**Expected improvement:** entry-level filtering and newer evidence ordered first, with provenance retained.  
**Concept:** knowledge quality, metadata filtering, dates, conflicts.  
**Takeaway:** the knowledge pipeline is part of product quality.

### 6. From question-answering to orchestration

**Time:** 74–86 min.  
**Students ask:** “I like AI. What should I specialize in?”  
**Expected:** insufficient information; identify useful clarification dimensions.  
**Modify:** click **Final assistant** in the Workshop journey. Answer its clarification in the same browser conversation.  
**Then ask:** “Compare AI Engineer and Data Scientist in skills, typical work, and technologies.”  
**Expected:** response reports `compare_roles` as the used tool and combines deterministic structured data with retrieved context.  
**Ask after:** “Why use a function instead of letting the LLM invent both sides? What still needs validation?”  
**Concept:** conversation state, tool calling, bounded deterministic logic.  
**Takeaway:** orchestrators gather context, retrieve, call tools, and then generate.

### 7. Evaluate and close

**Time:** 86–90 min.  
**Execute:** show `tests/evaluation_questions.json`; optionally run `python scripts/test_questions.py`.  
**Expected:** varied prose, so review sources and behavioral criteria instead of exact strings.  
**Ask:** “Which metric belongs to retrieval, citations, behavior, and usefulness?”  
**Concept:** component evaluation and regression debugging.  
**Takeaway:** evaluate the system at multiple boundaries; RAG is not a truth switch.

## Optional advanced scenarios

- Compare real embeddings with demo feature hashing and explain the pedagogical boundary.
- Add explicit Qdrant filters through a debug query parameter.
- Introduce an adversarial instruction inside a document and verify it remains data.
- Add citation validation that rejects source names not present in retrieved chunks.
- Create a small human-scored evaluation sheet for relevance, groundedness, clarity, and appropriate uncertainty.
