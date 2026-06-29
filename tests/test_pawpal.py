import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from pawpal_system import Owner, Pet, Task


def test_mark_complete_changes_status():
    """Calling markComplete() should flip isCompleted from False to True."""
    task = Task(title="Feed cat", durationMinutes=10, priority=1, description="Morning feeding")
    assert task.isCompleted is False
    task.markComplete()
    assert task.isCompleted is True


def test_adding_task_to_pet_increases_task_count():
    """Adding a task that applies to a pet should increase the pet's task count."""
    pet = Pet(name="Whiskers", species="Cat", age=3)
    owner = Owner(name="Alice", availableHours=8)

    tasks_for_pet = lambda: [t for t in owner.tasks if pet in t.appliesTo]
    assert len(tasks_for_pet()) == 0

    task = Task(title="Groom Whiskers", durationMinutes=15, priority=2, description="Weekly grooming", appliesTo=[pet])
    owner.addTask(task)

    assert len(tasks_for_pet()) == 1
