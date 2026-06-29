# PawPal+ (Module 2 Project)

You are building **PawPal+**, a Streamlit app that helps a pet owner plan care tasks for their pet.

## Scenario

A busy pet owner needs help staying consistent with pet care. They want an assistant that can:

- Track pet care tasks (walks, feeding, meds, enrichment, grooming, etc.)
- Consider constraints (time available, priority, owner preferences)
- Produce a daily plan and explain why it chose that plan

Your job is to design the system first (UML), then implement the logic in Python, then connect it to the Streamlit UI.

## What you will build

Your final app should:

- Let a user enter basic owner + pet info
- Let a user add/edit tasks (duration + priority at minimum)
- Generate a daily schedule/plan based on constraints and priorities
- Display the plan clearly (and ideally explain the reasoning)
- Include tests for the most important scheduling behaviors

## Getting started

### Setup

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

### Suggested workflow

1. Read the scenario carefully and identify requirements and edge cases.
2. Draft a UML diagram (classes, attributes, methods, relationships).
3. Convert UML into Python class stubs (no logic yet).
4. Implement scheduling logic in small increments.
5. Add tests to verify key behaviors.
6. Connect your logic to the Streamlit UI in `app.py`.
7. Refine UML so it matches what you actually built.

## 🖥️ Sample Output

Paste a sample of your app's CLI or Streamlit output here so a reader can see what a generated plan looks like:

```
# e.g.:
# Daily plan for Biscuit (Golden Retriever):
#   08:00 — Morning walk (30 min) [priority: high]
#   09:00 — Feeding (10 min) [priority: high]
#   ...
```

## 🧪 Testing PawPal+

```bash
# Run the full test suite:
pytest

# Run with coverage:
pytest --cov
```

Sample test output:

```
# Paste your pytest output here
```

## 📐 Smarter Scheduling

| Feature | Method(s) | Notes |
|---------|-----------|-------|
| Task sorting | `Scheduler.sortTasks()`, `Scheduler.sort_by_time()` | `sortTasks()` orders by priority then start time; `sort_by_time()` orders chronologically then priority |
| Filtering | `Scheduler.filterTasks(completed, pet_name)` | Filters by completion status, by pet, or both; either argument is optional |
| Skip tasks if time runs out | `Scheduler.filterByTimeAvailable()` | Greedy priority-order walk; drops tasks once the owner's available hours are exhausted |
| Conflict detection | `Scheduler.detectConflicts()` | Flags overlapping task pairs as "same pet" or "owner time" conflicts; returns warning strings |
| Conflict resolution | `Scheduler.handleConflicts()` | Pushes overlapping blocks forward so the schedule stays contiguous; called automatically by `generateSchedule()` |
| Recurring tasks | `Task.isRecurring()`, `Task.getNextOccurrence()`, `Task.markComplete()` | `isRecurring()` checks cadence; `getNextOccurrence()` computes the next datetime (daily/weekly/monthly); `markComplete()` returns a fresh copy advanced by one period |
| Recurring auto-requeue | `Owner.completeTask(taskTitle)` | Removes the completed task and re-adds the next occurrence so the to-do list stays stocked |
| Schedule generation | `Scheduler.generateSchedule(dayHours)` | Combines filtering, slot-packing, and conflict resolution into one call |

## 📸 Demo Walkthrough

Describe your app in numbered steps so a reader can follow along without watching a video:

1. <!-- Describe this step -->
2. <!-- Describe this step -->
3. <!-- Describe this step -->
4. <!-- Describe this step -->
5. <!-- Add more steps as needed -->

**Screenshot or video** *(optional)*: <!-- Insert a screenshot or link to a demo video here -->

## Sample Output
=======================================================
  OWNER — create & manage preferences
=======================================================
Created owner: Crystal, available hours: 10
Preferences (getPreferences): ['morning walks', 'no tasks after 8pm']
Updated available hours (setAvailableHours): 8
Clamped negative hours (setAvailableHours -5): 0

=======================================================
  PET — create & inspect pets
=======================================================
getSpecies — Luna: Dog, Mochi: Cat

getInfo — Luna:
Luna (Dog, 3 years old)
Special needs: medication: allergy pill with breakfast
Dietary: food: grain-free kibble

getInfo — Mochi:
Mochi (Cat, 5 years old)
Special needs: diet: kidney-friendly food only

=======================================================
  TASK — create tasks, inspect properties
=======================================================
  Morning Walk: priority=1, duration=60 min, recurring=True, nextOccurrence=2026-06-30 07:00
  Feed Pets: priority=1, duration=15 min, recurring=True, nextOccurrence=2026-06-30 08:00
  Vet Checkup: priority=2, duration=90 min, recurring=False, nextOccurrence=2026-06-29 10:00
  Grooming Session: priority=3, duration=45 min, recurring=True, nextOccurrence=2026-06-29 14:00
  Evening Feeding: priority=1, duration=15 min, recurring=True, nextOccurrence=2026-06-29 18:00
  Medication Check: priority=2, duration=10 min, recurring=True, nextOccurrence=2026-06-30 09:00
  Playtime: priority=3, duration=30 min, recurring=True, nextOccurrence=2026-06-29 15:00

Marking 'Vet Checkup' complete (markComplete)...
  isCompleted: True

=======================================================
  OWNER — addTask / getTodoList / completeTask
=======================================================
All tasks added. Todo list (getTodoList) — 6 pending:
  - Morning Walk
  - Feed Pets
  - Grooming Session
  - Evening Feeding
  - Medication Check
  - Playtime

Completing 'Grooming Session' via completeTask...
Todo list after completion — 5 remaining:
  - Morning Walk
  - Feed Pets
  - Evening Feeding
  - Medication Check
  - Playtime

=======================================================
  SCHEDULER — load, sort, filter, generate, explain
=======================================================
loadTasksFromOwner: loaded 6 tasks
addTask 'Bath Time': scheduler now has 7 tasks
removeTask 'Bath Time': scheduler now has 6 tasks

sortTasks (by priority then startHour):
  priority=1 | 07:00 | Morning Walk
  priority=1 | 08:00 | Feed Pets
  priority=1 | 18:00 | Evening Feeding
  priority=2 | 09:00 | Medication Check
  priority=2 | 10:00 | Vet Checkup
  priority=3 | 15:00 | Playtime

filterByTimeAvailable (8 hrs = 480 min):
  Morning Walk (60 min)
  Feed Pets (15 min)
  Evening Feeding (15 min)
  Medication Check (10 min)
  Vet Checkup (90 min)
  Playtime (30 min)

expandRecurringTasks: returned 6 task instances

generateSchedule(dayHours=12):
ScheduledTask.getTimeSlot() for each block:
  00:00 - 01:00 — Morning Walk for Luna
  01:00 - 02:00 — Feed Pets for Luna
  02:00 - 03:00 — Evening Feeding for Luna
  03:00 - 04:00 — Medication Check for Luna
  04:00 - 05:00 — Playtime for Luna

handleConflicts applied internally — resolved schedule:
  00:00 - 01:00 — Morning Walk
  01:00 - 02:00 — Feed Pets
  02:00 - 03:00 — Evening Feeding
  03:00 - 04:00 — Medication Check
  04:00 - 05:00 — Playtime

=======================================================
  TODAY'S SCHEDULE
=======================================================
TIME           TASK                  PET       DURATION    PRIORITY
───────────────────────────────────────────────────────────────────
00:00 - 01:00  Morning Walk          Luna      60 min      High    
01:00 - 02:00  Feed Pets             Luna      15 min      High    
02:00 - 03:00  Evening Feeding       Luna      15 min      High    
03:00 - 04:00  Medication Check      Luna      10 min      Medium  
04:00 - 05:00  Playtime              Luna      30 min      Low 