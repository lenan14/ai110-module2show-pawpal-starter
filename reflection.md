# PawPal+ Project Reflection

## 1. System Design

Three Core Actions:
1. **Enter owner and pet information** — Owner creates a profile with available hours and pet details (name, type, age, special needs)
2. **Add and edit care tasks** — Owner adds tasks (walk, feeding, medication, etc.) with duration and priority level
3. **Generate and view daily schedule** — App creates an optimized daily plan that fits within owner's time, respects priorities, and explains the reasoning

**a. Initial design**

**UML Class Structure:**

My initial design includes four core classes and two enumerations:

1. **Owner** - Represents the pet owner
   - Attributes: name, daily_hours_available, preferences
   - Responsibilities: Track availability and user preferences for pet care
   - Methods: set_availability(), get_preferences()

2. **Pet** - Represents individual pets
   - Attributes: name, pet_type (enum), age, special_needs (list)
   - Responsibilities: Store pet details and track any special constraints
   - Methods: get_info(), has_constraint()

3. **Task** - Represents a pet care task
   - Attributes: name, duration_minutes, priority (1-5), task_type (enum), description, repeat_frequency, assigned_pet
   - Responsibilities: Define a schedulable activity with duration and importance
   - Methods: validate(), get_details()

4. **Scheduler** - Main orchestrator for daily planning
   - Attributes: owner (1), pets (many), tasks (many)
   - Responsibilities: Create optimized daily schedules, manage pets/tasks, explain reasoning
   - Methods: add_pet(), add_task(), generate_daily_plan(), explain_reasoning(), calculate_total_duration()

5. **Enums** - TaskType and PetType for type safety and clarity

**Key Design Decisions:**
- Used Python dataclasses for clean, minimal boilerplate
- Task priority (1-5 scale) allows ranking importance
- Optional assigned_pet field supports both pet-specific and general tasks
- Scheduler holds references to Owner, Pets, and Tasks - it's the central component
- Relationships: Scheduler manages 1 Owner, schedules for multiple Pets, organizes multiple Tasks

**b. Design changes**

- Initial implementation phase: No changes yet. This skeleton will be reviewed and refined during implementation as we build out the scheduling logic in Phase 2-3.

---

## 2. Scheduling Logic and Tradeoffs

**a. Constraints and priorities**

- What constraints does your scheduler consider (for example: time, priority, preferences)?
- How did you decide which constraints mattered most?

**b. Tradeoffs**

- Describe one tradeoff your scheduler makes.
- Why is that tradeoff reasonable for this scenario?

---

## 3. AI Collaboration

**a. How you used AI**

- How did you use AI tools during this project (for example: design brainstorming, debugging, refactoring)?
- What kinds of prompts or questions were most helpful?

**b. Judgment and verification**

- Describe one moment where you did not accept an AI suggestion as-is.
- How did you evaluate or verify what the AI suggested?

---

## 4. Testing and Verification

**a. What you tested**

- What behaviors did you test?
- Why were these tests important?

**b. Confidence**

- How confident are you that your scheduler works correctly?
- What edge cases would you test next if you had more time?

---

## 5. Reflection

**a. What went well**

- What part of this project are you most satisfied with?

**b. What you would improve**

- If you had another iteration, what would you improve or redesign?

**c. Key takeaway**

- What is one important thing you learned about designing systems or working with AI on this project?
