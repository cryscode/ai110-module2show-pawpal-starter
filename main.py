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

# Tasks intentionally added OUT OF ORDER (by time) to test sorting
morning_walk = Task(
    title="Morning Walk",
    durationMinutes=60,
    priority=1,
    description="30-min walk around the block",
    recurrence="daily",
    startTime="07:00",
    appliesTo=[luna],
)

feeding = Task(
    title="Feed Pets",
    durationMinutes=15,
    priority=1,
    description="Breakfast for Luna and Mochi",
    recurrence="daily",
    startTime="08:00",
    appliesTo=[luna, mochi],
)

vet_checkup = Task(
    title="Vet Checkup",
    durationMinutes=90,
    priority=2,
    description="Annual wellness exam",
    recurrence="once",
    startTime="10:00",
    appliesTo=[mochi],
)

grooming = Task(
    title="Grooming Session",
    durationMinutes=45,
    priority=3,
    description="Brush coat and trim nails",
    recurrence="weekly",
    startTime="14:00",
    appliesTo=[luna],
)

evening_feeding = Task(
    title="Evening Feeding",
    durationMinutes=15,
    priority=1,
    description="Dinner for Luna and Mochi",
    recurrence="daily",
    startTime="18:00",
    appliesTo=[luna, mochi],
)

medication_check = Task(
    title="Medication Check",
    durationMinutes=10,
    priority=2,
    description="Give Luna her allergy pill",
    recurrence="daily",
    startTime="09:00",
    appliesTo=[luna],
)

playtime = Task(
    title="Playtime",
    durationMinutes=30,
    priority=3,
    description="Interactive toy session with both pets",
    recurrence="daily",
    startTime="15:00",
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
    startTime="11:00",
    appliesTo=[luna],
)
scheduler.addTask(bonus_task)
print(f"addTask 'Bath Time': scheduler now has {len(scheduler.tasks)} tasks")

scheduler.removeTask("Bath Time")
print(f"removeTask 'Bath Time': scheduler now has {len(scheduler.tasks)} tasks")

# ── NEW: sort_by_time ─────────────────────────────────────
# Tasks were added out of order above; sort_by_time re-orders them
# chronologically using the HH:MM string as the sort key.
#
# Why does sorting "HH:MM" strings work?
#   Python's sorted() compares strings character-by-character.
#   Because times are zero-padded ("07:00" not "7:00"),
#   lexicographic order == chronological order:
#     "07:00" < "08:00" < "09:00" < ... < "18:00"
#   The lambda passes (startTime, priority) so same-time tasks
#   are broken by priority (1 = highest urgency first).
section("SORT — sort_by_time() by HH:MM string, then priority")

print("Tasks in original (out-of-order) state:")
for t in scheduler.tasks:
    status = "done" if t.isCompleted else "pending"
    print(f"  [{t.startTime}] priority={t.priority}  {t.title:<22} ({status})")

print()
print("After sort_by_time()  →  sorted(tasks, key=lambda t: (t.startTime, t.priority)):")
for t in scheduler.sort_by_time():
    status = "done" if t.isCompleted else "pending"
    print(f"  [{t.startTime}] priority={t.priority}  {t.title:<22} ({status})")

# ── NEW: filterTasks ──────────────────────────────────────
section("FILTER — filterTasks(completed, pet_name)")

print("filterTasks(completed=False)  →  pending tasks only:")
for t in scheduler.filterTasks(completed=False):
    print(f"  {t.title:<22} done={t.isCompleted}")

print()
print("filterTasks(completed=True)   →  completed tasks only:")
for t in scheduler.filterTasks(completed=True):
    print(f"  {t.title:<22} done={t.isCompleted}")

print()
print("filterTasks(pet_name='Luna')  →  Luna's tasks only:")
for t in scheduler.filterTasks(pet_name="Luna"):
    print(f"  {t.title:<22} pets={[p.name for p in t.appliesTo]}")

print()
print("filterTasks(pet_name='Mochi') →  Mochi's tasks only:")
for t in scheduler.filterTasks(pet_name="Mochi"):
    print(f"  {t.title:<22} pets={[p.name for p in t.appliesTo]}")

print()
print("filterTasks(completed=False, pet_name='Luna')  →  Luna's pending tasks:")
for t in scheduler.filterTasks(completed=False, pet_name="Luna"):
    print(f"  {t.title:<22} priority={t.priority}")

# ── sortTasks (existing method) ───────────────────────────
print()
print("sortTasks() — priority first, then time, then duration desc:")
for t in scheduler.sortTasks():
    print(f"  priority={t.priority} | [{t.startTime}] | {t.title}")

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
print("-" * len(header))

for s in sorted(scheduler.schedule, key=lambda s: s.startTime):
    print(
        f"{s.getTimeSlot():<{col['time']}}"
        f"{s.task.title:<{col['task']}}"
        f"{s.pet.name:<{col['pet']}}"
        f"{str(s.task.durationMinutes) + ' min':<{col['duration']}}"
        f"{priority_label.get(s.task.priority, 'Unknown'):<{col['priority']}}"
    )

# ── CONFLICT DETECTION ────────────────────────────────────
section("CONFLICT DETECTION — detectConflicts()")

# Same-pet conflict: both tasks involve Luna and start at 07:00
morning_medication = Task(
    title="Morning Medication",
    durationMinutes=10,
    priority=1,
    description="Give Luna her allergy pill with breakfast",
    recurrence="daily",
    startTime="07:00",
    appliesTo=[luna],
)

# Owner-time conflict: different pets but overlaps Morning Walk (07:00–08:00)
mochi_breakfast = Task(
    title="Mochi Breakfast",
    durationMinutes=30,
    priority=1,
    description="Wet food for Mochi",
    recurrence="daily",
    startTime="07:30",
    appliesTo=[mochi],
)

conflict_scheduler = Scheduler(owner=crystal, pets=[luna, mochi])
conflict_scheduler.addTask(morning_walk)       # 07:00–08:00, Luna
conflict_scheduler.addTask(morning_medication) # 07:00–07:10, Luna  → same-pet conflict
conflict_scheduler.addTask(mochi_breakfast)    # 07:30–08:00, Mochi → owner-time conflict
conflict_scheduler.addTask(feeding)            # 08:00–08:15, Luna+Mochi (no conflict)

warnings = conflict_scheduler.detectConflicts()
print(f"Tasks loaded: {len(conflict_scheduler.tasks)}")
print(f"Conflicts found: {len(warnings)}\n")
for w in warnings:
    print(f"  {w}")
if not warnings:
    print("  (no conflicts)")
