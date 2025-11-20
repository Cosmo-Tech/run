# Copilot Custom Instructions for Cosmo-Tech Python Project

## Python Development Best Practices
- Use modern Python syntax and features.
- Use semantic versioning
- Prefer type annotations and docstrings for all functions and classes.
- Follow PEP8 for formatting and naming conventions.
- Structure code for readability and maintainability; modularize logic into functions and classes.
- Use f-strings for string interpolation.
- Handle exceptions explicitly and log errors with context.


## Project Structure Conventions
- Place core logic in `run/` and configuration in `run/config.py`.
- Store reusable api templates in `templates/`.
- Keep environment files and CI/CD configs at the project root.
- Update `README.md` with any new conventions or architectural changes.

## General Guidance
- Prioritize clarity, reliability, and maintainability.
- Document non-obvious decisions inline.

## Testing & Automation
- Write tests for new features and bug fixes.
- Use pytest for testing and ensure tests are isolated and repeatable.