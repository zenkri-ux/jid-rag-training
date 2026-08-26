# Security Policy

## Supported use

This repository is an educational, local-only workshop application. It is not designed to be exposed directly to the public internet.

## Reporting a vulnerability

Please report security issues privately through GitHub's **Security advisories** tab instead of opening a public issue. Do not include API keys, personal data, or exploit details in public discussions.

## Credential handling

- Copy `.env.example` to `.env` and keep real credentials only in `.env`.
- Never commit `.env` or paste credentials into issues, logs, screenshots, or training material.
- Revoke and replace any credential that may have been exposed.

## Production deployment

Before deploying beyond localhost, add authentication and authorization, protect debugging and reindexing endpoints, configure rate limits, restrict network access, centralize sanitized logging, and complete a deployment-specific security review.
