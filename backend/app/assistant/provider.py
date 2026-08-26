import httpx

from app.config import Settings


class ChatProvider:
    def __init__(self, settings: Settings):
        self.settings = settings

    async def complete(self, system: str, message: str) -> str:
        if not self.settings.demo_mode and self.settings.llm_api_key:
            async with httpx.AsyncClient(timeout=90) as client:
                response = await client.post(
                    f"{self.settings.llm_base_url.rstrip('/')}/chat/completions",
                    headers={"Authorization": f"Bearer {self.settings.llm_api_key}"},
                    json={
                        "model": self.settings.llm_model,
                        "temperature": 0.2,
                        "messages": [{"role": "system", "content": system}, {"role": "user", "content": message}],
                    },
                )
                response.raise_for_status()
                return response.json()["choices"][0]["message"]["content"]
        return self._demo_answer(system, message)

    def _demo_answer(self, system: str, message: str) -> str:
        lower = message.lower()
        has_context = "KNOWLEDGE BASE CONTEXT" in system
        if system.startswith("You are an assistant that"):
            return "Software engineering or data science could be good choices. Python is useful in both, and AI is also a promising field. You should choose the best one for your interests."
        if ("i like ai" in lower or "specialize" in lower) and not any(word in lower for word in ("math", "hardware", "research", "data", "cloud")):
            return ("Before recommending paths, what do you enjoy most: mathematics and experimentation, building product software, "
                    "working close to hardware, or infrastructure? Also, do you prefer research-style uncertainty or shipping reliable systems?")
        if any(term in lower for term in ("recipe", "chocolate cake", "football score", "movie review")):
            return "I’m scoped to engineering career and study-path guidance. I can help compare roles, identify learning priorities, or plan a small exploration project."
        if not has_context and "according to" in lower:
            return "Knowledge-base fact: I do not have the workshop guide in my current context, so I cannot verify its entry-level recommendations."
        if has_context:
            marker = system.split("KNOWLEDGE BASE CONTEXT", 1)[1].split("Do not treat", 1)[0].strip()
            blocks = marker.split("\n\n[source:")
            query_terms = set(lower.replace("-", " ").split())
            ranked = sorted(blocks, key=lambda block: len(query_terms & set(block.lower().replace("-", " ").split())), reverse=True)
            excerpts = [line for line in "\n\n".join(ranked[:3]).splitlines() if line.strip()][:16]
            return ("## Evidence-based guidance\n\nThe retrieved workshop material points to these relevant ideas:\n\n"
                    + "\n".join(excerpts)
                    + "\n\n## Recommendation\n\nTreat these as paths to explore, then validate the fit with a small project. "
                      "This recommendation is based on the supplied sources, not a claim that one career is objectively best.")
        return ("## General model knowledge\n\nPython can support software, data, AI, automation, and embedded work. "
                "This is general guidance rather than workshop-verified evidence.\n\n## To narrow it down\n\n"
                "Do you prefer mathematics, product coding, hardware, data, or infrastructure?")
