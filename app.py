import streamlit as st
from pawpal_system import Owner, Task, Pet, Scheduler

st.set_page_config(page_title="PawPal+", page_icon="🐾", layout="centered")

st.title("🐾 PawPal+")

# ── Session initialization ──────────────────────────────────────────────────
st.subheader("Owner & Pet")

owner_name = st.text_input("Owner name", value="Jordan")
available_hours = st.number_input("Available hours today", min_value=1, max_value=24, value=8)
pet_name = st.text_input("Pet name", value="Mochi")
pet_age = st.number_input("Pet age (years)", min_value=0, max_value=30, value=3)
species = st.selectbox("Species", ["dog", "cat", "other"])

if "owner" not in st.session_state:
    st.session_state.owner = Owner(name=owner_name, availableHours=available_hours)

if "pet" not in st.session_state:
    st.session_state.pet = Pet(name=pet_name, species=species, age=pet_age)

if "scheduler" not in st.session_state:
    st.session_state.scheduler = Scheduler(owner=st.session_state.owner)
    st.session_state.scheduler.pets.append(st.session_state.pet)

# Update available hours on the stored owner object
if st.button("Update available hours"):
    st.session_state.owner.setAvailableHours(available_hours)
    st.success(f"Available hours updated to {st.session_state.owner.availableHours}h")

# Show pet summary
st.markdown(st.session_state.pet.getInfo())

st.divider()

# ── Preferences ─────────────────────────────────────────────────────────────
st.subheader("Owner Preferences")

pref_input = st.text_input("Add a preference (e.g. 'morning walks only')", value="")
if st.button("Add preference"):
    if pref_input:
        st.session_state.owner.addPreference(pref_input)

prefs = st.session_state.owner.getPreferences()
if prefs:
    st.write("Current preferences:", prefs)
else:
    st.info("No preferences added yet.")

st.divider()

# ── Pet special needs ────────────────────────────────────────────────────────
st.subheader("Pet Special Needs")

col_need, col_detail = st.columns(2)
with col_need:
    need_key = st.text_input("Need (e.g. 'medication')", value="")
with col_detail:
    need_detail = st.text_input("Detail (e.g. 'twice daily')", value="")

if st.button("Add special need"):
    if need_key and need_detail:
        st.session_state.pet.addSpecialNeed(need_key, need_detail)

if st.session_state.pet.specialNeeds:
    st.write("Special needs:", st.session_state.pet.specialNeeds)
else:
    st.info("No special needs recorded.")

st.divider()

# ── Tasks ────────────────────────────────────────────────────────────────────
st.subheader("Tasks")

PRIORITY_MAP = {"high": 1, "medium": 2, "low": 3}
PRIORITY_LABEL = {1: "high", 2: "medium", 3: "low"}

col1, col2, col3 = st.columns(3)
with col1:
    task_title = st.text_input("Task title", value="Morning walk")
with col2:
    duration = st.number_input("Duration (minutes)", min_value=1, max_value=240, value=20)
with col3:
    priority = st.selectbox("Priority", ["high", "medium", "low"])

col4, col5 = st.columns(2)
with col4:
    description = st.text_input("Description", value="")
with col5:
    recurrence = st.selectbox("Recurrence", ["once", "daily", "weekly"])

if st.button("Add task"):
    task = Task(
        title=task_title,
        durationMinutes=int(duration),
        priority=PRIORITY_MAP[priority],
        description=description,
        recurrence=recurrence,
        appliesTo=[st.session_state.pet],
    )
    st.session_state.owner.addTask(task)
    st.session_state.scheduler.addTask(task)

todo = st.session_state.owner.getTodoList()
if todo:
    st.write("Current tasks:")
    st.table([
        {
            "title": t.title,
            "duration (min)": t.durationMinutes,
            "priority": PRIORITY_LABEL.get(t.getPriority(), t.getPriority()),
            "description": t.description,
        }
        for t in todo
    ])

    complete_title = st.selectbox("Mark task complete", [t.title for t in todo])
    if st.button("Complete task"):
        next_task = st.session_state.owner.completeTask(complete_title)
        st.session_state.scheduler.removeTask(complete_title)
        if next_task:
            st.session_state.scheduler.addTask(next_task)
            st.success(
                f"'{complete_title}' marked complete. "
                f"Next {next_task.recurrence} occurrence added for "
                f"{next_task.dueDate.strftime('%Y-%m-%d')}."
            )
        else:
            st.success(f"'{complete_title}' marked complete and removed from scheduler.")
else:
    st.info("No tasks yet. Add one above.")

st.divider()

# ── Schedule ─────────────────────────────────────────────────────────────────
st.subheader("Build Schedule")

if st.button("Generate schedule"):
    schedule = st.session_state.scheduler.generateSchedule(
        dayHours=st.session_state.owner.availableHours
    )
    explanation = st.session_state.scheduler.explainSchedule()
    if schedule:
        st.markdown(explanation)
    else:
        st.warning("No tasks were scheduled. Add tasks above and try again.")
