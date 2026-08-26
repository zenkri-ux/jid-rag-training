from typing import Any


ROLE_DATA: dict[str, dict[str, Any]] = {
    "ai engineer": {
        "typical_work": "builds AI-powered product features and production inference pipelines",
        "skills": ["Python", "ML fundamentals", "APIs", "evaluation", "software engineering"],
        "technologies": ["PyTorch", "FastAPI", "Docker", "vector databases"],
    },
    "data scientist": {
        "typical_work": "analyzes data, designs experiments, and develops predictive models",
        "skills": ["statistics", "Python or R", "SQL", "experimentation", "communication"],
        "technologies": ["pandas", "scikit-learn", "Jupyter", "SQL"],
    },
    "data engineer": {
        "typical_work": "builds reliable data ingestion, transformation, and serving systems",
        "skills": ["SQL", "Python", "data modeling", "distributed systems", "operations"],
        "technologies": ["PostgreSQL", "dbt", "Airflow", "Spark", "Docker"],
    },
    "devops engineer": {
        "typical_work": "improves delivery automation, infrastructure reliability, and observability",
        "skills": ["Linux", "networking", "scripting", "CI/CD", "cloud fundamentals"],
        "technologies": ["GitHub Actions", "Docker", "Terraform", "Prometheus"],
    },
}


def compare_roles(role_a: str, role_b: str) -> dict[str, Any] | None:
    first, second = ROLE_DATA.get(role_a.lower()), ROLE_DATA.get(role_b.lower())
    if not first or not second:
        return None
    return {role_a: first, role_b: second}


def detect_comparison(message: str) -> tuple[str, str] | None:
    lower = message.lower()
    mentioned = [role for role in ROLE_DATA if role in lower]
    if len(mentioned) == 2 and any(word in lower for word in ("compare", "difference", "versus", " vs ")):
        return mentioned[0], mentioned[1]
    return None

