# AGENT GENERAL INFO 

## Log Your Tracks

<important>

You will perform the tasks as described in the challenges described in the `README.md` with the guidance of the user.
During the challenge, and upon completion you will also log:

- User instructions given to you
- Clarifying questions you asked the user and any answers you received
- Any assumptions you made 
- Any assumptions the user made
- Any issues you encountered and how you resolved them and guidance you received from the user
- Any other relevant information about your process

These will be logged in `.agent_log/[year].log`

</important>

---

# LANGUAGE SELECTION

**Selected Language: Python 3.11+**

Python is chosen for this challenge due to:
- Excellent data analysis libraries (pandas, numpy)
- Strong optimization libraries (scipy, pulp)
- Rapid prototyping capabilities
- Comprehensive testing ecosystem
- Clear, readable syntax

---

# DOCUMENTATION STRUCTURE

All detailed guidance is organized in `implementation/docs/`:

## 📁 [Project Structure](implementation/docs/project-structure.md)
- Directory layout and organization
- Module responsibilities (models, services, strategies, utils)
- Test organization
- Configuration files
- File naming conventions

## ✅ [Quality Standards](implementation/docs/quality-standards.md)
- Testing requirements (80% coverage minimum)
- Code quality tools (black, isort, mypy, flake8, pylint)
- Tool configurations
- Pre-commit workflow
- Documentation standards

## 🔴🟢🔵 [TDD Guide](implementation/docs/tdd-guide.md)
- Red-Green-Refactor cycle explained
- TDD workflow for Quantmas challenges
- Best practices (AAA pattern, fixtures, descriptive names)
- Common mistakes to avoid
- Benefits of TDD

## 🐍 [Python Standards](implementation/docs/python-standards.md)
- Type hints (mandatory)
- Dataclasses for data structures
- Error handling and custom exceptions
- Logging patterns
- Code organization
- Naming conventions
- Pythonic patterns

## 🔄 [Workflow](implementation/docs/workflow.md)
- Step-by-step problem-solving process
- From understanding problem to submission
- Data exploration techniques
- Strategy development
- Output generation
- Quality checks
- Troubleshooting guide

---

# QUICK START

## For New Challenge

1. **Understand**: Read `problems/year_X/problem.md` and examine data files
2. **Setup**: Create project structure (see [Project Structure](implementation/docs/project-structure.md))
3. **TDD**: Follow Red-Green-Refactor cycle (see [TDD Guide](implementation/docs/tdd-guide.md))
4. **Quality**: Maintain 80% coverage and pass all checks (see [Quality Standards](implementation/docs/quality-standards.md))
5. **Document**: Update README and docs
6. **Submit**: Run `bash ./test-and-submit.sh`

## Essential Commands

```bash
# Setup
cd implementation
pip install -r requirements.txt requirements-dev.txt

# Development
pytest --cov=src --cov-report=html  # Run tests with coverage
black src/ test/                     # Format code
mypy src/                            # Type check
flake8 src/                          # Lint

# Run solution
python -m src.main

# Submit
bash ./test-and-submit.sh
```

---

# CORE PRINCIPLES

## Test-Driven Development (TDD)

**Always follow the Red-Green-Refactor cycle:**

1. 🔴 **RED**: Write a failing test first
2. 🟢 **GREEN**: Write minimal code to pass
3. 🔵 **REFACTOR**: Improve code quality

See [TDD Guide](implementation/docs/tdd-guide.md) for detailed examples.

## Quality Standards

**Mandatory requirements:**
- ✅ Test coverage ≥ 80%
- ✅ All functions have type hints
- ✅ mypy passes with no errors
- ✅ flake8 passes with no errors
- ✅ pylint score ≥ 8.0/10

See [Quality Standards](implementation/docs/quality-standards.md) for details.

## Code Organization

**Follow the module structure:**
- `models/` - Immutable data structures (dataclasses)
- `services/` - Business logic (data loading, trading engine)
- `strategies/` - Algorithm implementations
- `utils/` - Helper functions and validators

See [Project Structure](implementation/docs/project-structure.md) for details.

## Python Best Practices

**Key conventions:**
- Type hints on all functions
- Dataclasses for data structures
- Custom exceptions for errors
- Structured logging
- F-strings for formatting
- List comprehensions where appropriate

See [Python Standards](implementation/docs/python-standards.md) for details.

---

# COMMIT GUIDELINES

## Format

```
[Year X] Brief description

Detailed explanation if needed:
- What was changed
- Why it was changed

Co-authored-by: Ona <no-reply@ona.com>
```

## When to Commit

- After completing each Red-Green-Refactor cycle
- When tests pass and coverage is maintained
- After adding documentation
- **Only when explicitly asked by user**

---

# COLLABORATION WITH USER

## When to Ask Questions
- Problem statement ambiguity
- Unclear business rules
- Trade-off decisions
- Before major architectural changes

## What to Report
- Completion of major milestones
- Test coverage status
- Issues encountered
- Performance metrics
- Final results

## What to Log (in .agent_log/2025.log)
- All user instructions
- Questions and answers
- Assumptions made
- Issues and resolutions
- Key decisions and rationale
- Test results
- Final scores and learnings

---

# PROBLEM-SOLVING WORKFLOW

High-level process (see [Workflow](implementation/docs/workflow.md) for details):

1. **Understand** - Read problem, examine data, clarify ambiguities
2. **Setup** - Create project structure, install dependencies
3. **Explore** - Analyze data, identify patterns
4. **Build** - Implement using TDD (models → services → strategies)
5. **Optimize** - Improve strategy, measure performance
6. **Generate** - Create output in correct format
7. **Validate** - Run all quality checks
8. **Document** - Update README and docs
9. **Submit** - Run submission script

---

# QUANTMAS REQUIREMENTS

## Project Structure

```
implementation/
├── src/              # Source code
├── test/             # Tests (≥80% coverage)
├── docs/             # Documentation
├── requirements.txt  # Dependencies
└── README.md         # How to run
```

## Output Location

All outputs must be in:
```
problems/year_X/output/
```

## Submission

```bash
bash ./test-and-submit.sh
```

---

# REFERENCE DOCUMENTATION

For detailed information, see:

- 📁 **[Project Structure](implementation/docs/project-structure.md)** - How to organize code
- ✅ **[Quality Standards](implementation/docs/quality-standards.md)** - Testing and tooling
- 🔴🟢🔵 **[TDD Guide](implementation/docs/tdd-guide.md)** - Test-driven development
- 🐍 **[Python Standards](implementation/docs/python-standards.md)** - Coding conventions
- 🔄 **[Workflow](implementation/docs/workflow.md)** - Problem-solving process

---

**Remember**: Quality over speed. Write tests first, maintain coverage, and follow the TDD cycle. The documentation is your guide—refer to it often!
