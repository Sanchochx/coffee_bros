# TASK EXECUTION WORKFLOW

**Context Files:**
- @context/IMPLEMENTATION_PLAN.md (user stories and phases)
- @context/arch_status.md (current architecture state)
- @CLAUDE.md (project details, tech stack, coding standards)

---

## Execution Process

1. **Find Next User Story**
   - Locate the first unchecked user story (marked with [ ]) in IMPLEMENTATION_PLAN.md
   - Read the linked user story file to understand all acceptance criteria

2. **Implement Each Acceptance Criterion**
   - Work through criteria ONE AT A TIME (don't skip ahead)
   - For each criterion:
     - Explain what you're building and why
     - Create/modify files in correct directories (follow project structure in CLAUDE.md)
     - Apply coding standards and conventions from CLAUDE.md
     - Mark the criterion as done [x] in the user story file when complete

3. **Complete the User Story**
   - After ALL acceptance criteria are [x], mark the user story as complete [x] in IMPLEMENTATION_PLAN.md

4. **Update Architecture Documentation**
   - Update arch_status.md with:
     - New/modified files and their locations
     - New features/systems implemented
     - Current folder structure changes
     - Any important architectural decisions made

5. **Checkpoint**
   - Show me a summary of what was implemented
   - Ask for confirmation before moving to the next user story

6. **Create Phase Summary (when completing a full phase)**
   - After finishing all user stories in a phase, create a comprehensive summary including in a document with user-store-name-resume.md:
     - **Changes Made:** High-level overview of what was implemented
     - **Files Modified/Created:** List each file with a brief explanation of its purpose and changes
     - **Rationale:** Clear explanation for an LLM context of what was completed, why these changes matter, and how they fit into the overall architecture
     - **Next Steps:** What phase comes next and any dependencies or prerequisites
   - This summary helps future LLM sessions understand the project state without re-reading all code

7. check the user story in the implementation plan

8. wait for my instruction and review dont do anything else that is not included here.

9. wait for my instruction and review dont do anything else that is not included here
---

## Important Guidelines

- **Follow CLAUDE.md** for all technical decisions (architecture, coding standards, file organization)
- **Work incrementally** - complete one criterion before starting the next
- **Update documentation** as you go, not at the end
- **Implementation only** - don't write tests unless the user story explicitly requires them
- **Ask questions** if acceptance criteria are unclear or conflict with existing architecture