# Participant Exercises

Do not jump directly to a fix. For every scenario: reproduce the behavior, record evidence, form a hypothesis, change one design choice, and retest the same prompt.

## Exercise 1 — Where did that answer come from?

Ask: “I'm studying computer engineering and enjoy Python. Which fields could fit me?” Identify which claims are verified and which are general model output.

## Exercise 2 — Instructions are application behavior

Try “What is the best engineering career?” and “Tell me exact local demand for AI engineers.” Compare the structure, certainty, and boundaries before and after the instruction change.

## Exercise 3 — Missing versus excessive context

Ask for the workshop's entry-level data-engineering technologies. Then compare no context with all documents injected. What became possible, and what became wasteful?

## Exercise 4 — Inspect retrieval

Ask: “I like programming but want to work close to hardware.” Inspect `/debug/retrieval`. The correct document existing is not enough; the retriever must select a useful chunk.

## Exercise 5 — Quality, metadata, and conflict

Compare retrieval for the deliberately bad document and clean documents. Ask for “current junior data-engineering technologies.” Check source, section, year, and authority.

## Exercise 6 — Conversation and tools

Ask the ambiguous “I like AI.” Answer the clarification question in the same conversation. Then compare AI Engineer with Data Scientist and identify what the deterministic tool contributes.

