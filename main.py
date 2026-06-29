import sys
sys.stdout.reconfigure(encoding="utf-8")

from pawpal_system import Owner, Pet, Task, Scheduler, ScheduledTask

def section(title):
    print(f"\n{'=' * 55}")
    print(f"  {title}")
    print(f"{'=' * 55}")

# ── Owner ──────────────────────────────────────────────────
section("OWNER — create & manage preferences")

crystal = Owner(name="Crystal", availableHours=10)
print(f"Created owner: {crystal.name}, available hours: {crystal.availableHours}")

crystal.addPreference("morning walks")
crystal.addPreference("no tasks after 8pm")
crystal.addPreference("morning walks")          # duplicate — should be ignored
print(f"Preferences (getPreferences): {crystal.getPreferences()}")

crystal.setAvailableHours(8)
print(f"Updated available hours (setAvailableHours): {crystal.availableHours}")

crystal.setAvailableHours(-5)                  # negative — should clamp to 0
print(f"Clamped negative hours (setAvailableHours -5): {crystal.availableHours}")
crystal.setAvailableHours(8)                   # restore

# ── Pet ────────────────────────────────────────────────────
section("PET — create & inspect pets")

luna = Pet(name="Luna", species="Dog", age=3)
luna.addSpecialNeed("medication", "allergy pill with breakfast")
luna.dietary["food"] = "grain-free kibble"

mochi = Pet(name="Mochi", species="Cat", age=5)
mochi.addSpecialNeed("diet", "kidney-friendly food only")

print(f"getSpecies — Luna: {luna.getSpecies()}, Mochi: {mochi.getSpecies()}")
print()
print(f"getInfo — Luna:\n{luna.getInfo()}")
print()
print(f"getInfo — Mochi:\n{mochi.getInfo()}")

# ── Task ───────────────────────────────────────────────────
section("TASK — create tasks, inspect properties")

morning_walk = Task(
    title="Morning Walk",
    durationMinutes=60,
    priority=1,
    description="30-min walk around the block",
    recurrence="daily",
    startHour=7,
    appliesTo=[luna],
)

feeding = Task(
    title="Feed Pets",
    durationMinutes=15,
    priority=1,
    description="Breakfast for Luna and Mochi",
    recurrence="daily",
    startHour=8,
    appliesTo=[luna, mochi],
)

vet_checkup = Task(
    title="Vet Checkup",
    durationMinutes=90,
    priority=2,
    description="Annual wellness exam",
    recurrence="once",
    startHour=10,
    appliesTo=[mochi],
)

grooming = Task(
    title="Grooming Session",
    durationMinutes=45,
    priority=3,
    description="Brush coat and trim nails",
    recurrence="weekly",
    startHour=14,
    appliesTo=[luna],
)

evening_feeding = Task(
    title="Evening Feeding",
    durationMinutes=15,
    priority=1,
    description="Dinner for Luna and Mochi",
    recurrence="daily",
    startHour=18,
    appliesTo=[luna, mochi],
)

medication_check = Task(
    title="Medication Check",
    durationMinutes=10,
    priority=2,
    description="Give Luna her allergy pill",
    recurrence="daily",
    startHour=9,
    appliesTo=[luna],
)

playtime = Task(
    title="Playtime",
    durationMinutes=30,
    priority=3,
    description="Interactive toy session with both pets",
    recurrence="daily",
    startHour=15,
    appliesTo=[luna, mochi],
)

for task in [morning_walk, feeding, vet_checkup, grooming, evening_feeding, medication_check, playtime]:
    print(f"  {task.title}: priority={task.getPriority()}, "
          f"duration={task.getDuration()} min, "
          f"recurring={task.isRecurring()}, "
          f"nextOccurrence={task.getNextOccurrence().strftime('%Y-%m-%d %H:%M')}")

# markComplete demo
print()
print("Marking 'Vet Checkup' complete (markComplete)...")
vet_checkup.markComplete()
print(f"  isCompleted: {vet_checkup.isCompleted}")

# ── Owner task management ──────────────────────────────────
section("OWNER — addTask / getTodoList / completeTask")

for task in [morning_walk, feeding, vet_checkup, grooming, evening_feeding, medication_check, playtime]:
    crystal.addTask(task)

print(f"All tasks added. Todo list (getTodoList) — {len(crystal.getTodoList())} pending:")
for t in crystal.getTodoList():
    print(f"  - {t.title}")

print()
print("Completing 'Grooming Session' via completeTask...")
crystal.completeTask("Grooming Session")
print(f"Todo list after completion — {len(crystal.getTodoList())} remaining:")
for t in crystal.getTodoList():
    print(f"  - {t.title}")

# ── Scheduler ─────────────────────────────────────────────
section("SCHEDULER — load, sort, filter, generate, explain")

scheduler = Scheduler(owner=crystal, pets=[luna, mochi])

# loadTasksFromOwner
loaded = scheduler.loadTasksFromOwner()
print(f"loadTasksFromOwner: loaded {len(loaded)} tasks")

# addTask / removeTask
bonus_task = Task(
    title="Bath Time",
    durationMinutes=20,
    priority=3,
    description="Quick rinse and dry",
    recurrence="weekly",
    startHour=11,
    appliesTo=[luna],
)
scheduler.addTask(bonus_task)
print(f"addTask 'Bath Time': scheduler now has {len(scheduler.tasks)} tasks")

scheduler.removeTask("Bath Time")
print(f"removeTask 'Bath Time': scheduler now has {len(scheduler.tasks)} tasks")

# sortTasks
print()
print("sortTasks (by priority then startHour):")
for t in scheduler.sortTasks():
    print(f"  priority={t.priority} | {t.startHour:02d}:00 | {t.title}")

# filterByTimeAvailable
print()
filtered = scheduler.filterByTimeAvailable()
print(f"filterByTimeAvailable ({crystal.availableHours} hrs = {crystal.availableHours * 60} min):")
for t in filtered:
    print(f"  {t.title} ({t.durationMinutes} min)")

# expandRecurringTasks
expanded = scheduler.expandRecurringTasks()
print(f"\nexpandRecurringTasks: returned {len(expanded)} task instances")

# generateSchedule
print()
print("generateSchedule(dayHours=12):")
scheduler.generateSchedule(dayHours=12)

# ScheduledTask.getTimeSlot demo
print("ScheduledTask.getTimeSlot() for each block:")
for s in scheduler.schedule:
    print(f"  {s.getTimeSlot()} — {s.task.title} for {s.pet.name}")

# handleConflicts (called internally; show the post-conflict schedule)
print()
print("handleConflicts applied internally — resolved schedule:")
for s in scheduler.handleConflicts():
    print(f"  {s.getTimeSlot()} — {s.task.title}")

# explainSchedule — formatted as an aligned table
section("TODAY'S SCHEDULE")

priority_label = {1: "High", 2: "Medium", 3: "Low"}
col = {"time": 15, "task": 22, "pet": 10, "duration": 12, "priority": 8}

header = (
    f"{'TIME':<{col['time']}}"
    f"{'TASK':<{col['task']}}"
    f"{'PET':<{col['pet']}}"
    f"{'DURATION':<{col['duration']}}"
    f"{'PRIORITY':<{col['priority']}}"
)
print(header)
print("─" * len(header))

for s in sorted(scheduler.schedule, key=lambda s: s.startTime):
    print(
        f"{s.getTimeSlot():<{col['time']}}"
        f"{s.task.title:<{col['task']}}"
        f"{s.pet.name:<{col['pet']}}"
        f"{str(s.task.durationMinutes) + ' min':<{col['duration']}}"
        f"{priority_label.get(s.task.priority, 'Unknown'):<{col['priority']}}"
    )
