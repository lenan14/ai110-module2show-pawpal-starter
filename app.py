import streamlit as st
from pawpal_system import (
    Owner, Pet, Task, Scheduler,
    TaskType, PetType
)

st.set_page_config(page_title="PawPal+", page_icon="🐾", layout="wide")

st.title("🐾 PawPal+")

st.markdown(
    """
An intelligent pet care planner that helps you schedule tasks for your pets 
based on your available time, task priority, and pet constraints.
"""
)

# ============================================================================
# Session State Initialization
# ============================================================================

def initialize_session_state():
    """Initialize session state if needed"""
    if "owner" not in st.session_state:
        st.session_state.owner = None
    if "scheduler" not in st.session_state:
        st.session_state.scheduler = None
    if "current_pet" not in st.session_state:
        st.session_state.current_pet = None


initialize_session_state()

# ============================================================================
# Sidebar: Owner Setup
# ============================================================================

st.sidebar.subheader("👤 Owner Setup")

owner_name = st.sidebar.text_input(
    "Owner name",
    value="Jordan" if st.session_state.owner is None else st.session_state.owner.name,
    key="owner_name_input"
)

available_hours = st.sidebar.slider(
    "Available hours per day",
    min_value=0.5,
    max_value=24.0,
    value=4.0 if st.session_state.owner is None else st.session_state.owner.daily_hours_available,
    step=0.5,
    key="hours_slider"
)

if st.sidebar.button("Create/Update Owner", key="create_owner_btn"):
    st.session_state.owner = Owner(
        name=owner_name,
        daily_hours_available=available_hours
    )
    st.session_state.scheduler = Scheduler(owner=st.session_state.owner)
    st.sidebar.success(f"✓ Owner '{owner_name}' created!")

# ============================================================================
# Sidebar: Add Pets
# ============================================================================

if st.session_state.owner is not None:
    st.sidebar.divider()
    st.sidebar.subheader("🐶 Add Pets")
    
    pet_name = st.sidebar.text_input("Pet name", key="pet_name_input")
    pet_type = st.sidebar.selectbox(
        "Species",
        ["dog", "cat", "bird", "rabbit", "other"],
        key="pet_type_select"
    )
    pet_age = st.sidebar.number_input(
        "Age (years)",
        min_value=0,
        max_value=30,
        value=3,
        key="pet_age_input"
    )
    
    special_needs = st.sidebar.text_input(
        "Special needs (comma-separated)",
        placeholder="e.g., senior, diabetic, needs_exercise",
        key="special_needs_input"
    )
    
    if st.sidebar.button("Add Pet", key="add_pet_btn"):
        if pet_name:
            needs_list = [n.strip() for n in special_needs.split(",") if n.strip()]
            pet = Pet(
                name=pet_name,
                pet_type=PetType[pet_type.upper()],
                age=pet_age,
                special_needs=needs_list
            )
            st.session_state.scheduler.add_pet(pet)
            st.sidebar.success(f"✓ Pet '{pet_name}' added!")
            st.rerun()
    
    # Display added pets
    if st.session_state.scheduler.pets:
        st.sidebar.markdown("**Your Pets:**")
        for pet in st.session_state.scheduler.pets:
            st.sidebar.markdown(f"• {pet.get_info()}")

# ============================================================================
# Main Content: Task Management
# ============================================================================

if st.session_state.owner is not None and st.session_state.scheduler is not None:
    
    # Tabs for different views
    tab1, tab2, tab3, tab4 = st.tabs(
        ["📋 Add Tasks", "📅 Daily Schedule", "⚙️ Manage Tasks", "📊 Analytics"]
    )
    
    # ========================================================================
    # TAB 1: Add Tasks
    # ========================================================================
    
    with tab1:
        st.subheader("Add a New Task")
        
        col1, col2 = st.columns(2)
        
        with col1:
            task_name = st.text_input("Task name", key="task_name_input")
            task_type = st.selectbox(
                "Task type",
                [t.value for t in TaskType],
                key="task_type_select"
            )
            duration = st.number_input(
                "Duration (minutes)",
                min_value=5,
                max_value=480,
                value=30,
                step=5,
                key="duration_input"
            )
        
        with col2:
            priority = st.slider(
                "Priority",
                min_value=1,
                max_value=5,
                value=3,
                key="priority_slider"
            )
            scheduled_time = st.text_input(
                "Scheduled time (HH:MM)",
                value="08:00",
                key="time_input",
                placeholder="08:00"
            )
            assigned_pet = st.selectbox(
                "Assign to pet",
                [p.name for p in st.session_state.scheduler.pets] + ["General"],
                key="pet_select"
            )
        
        description = st.text_area(
            "Description",
            placeholder="What is this task about?",
            key="description_input"
        )
        
        if st.button("Add Task", key="add_task_btn"):
            if task_name and assigned_pet:
                assign_pet = None if assigned_pet == "General" else assigned_pet
                task = Task(
                    name=task_name,
                    duration_minutes=duration,
                    priority=priority,
                    task_type=TaskType[task_type.upper()],
                    description=description,
                    assigned_pet=assign_pet,
                    scheduled_time=scheduled_time
                )
                
                if task.validate():
                    st.session_state.scheduler.add_task(task)
                    st.success(f"✓ Task '{task_name}' added!")
                    st.rerun()
                else:
                    st.error("❌ Invalid task. Check duration and priority.")
    
    # ========================================================================
    # TAB 2: Daily Schedule
    # ========================================================================
    
    with tab2:
        st.subheader("📅 Today's Schedule")
        
        col1, col2 = st.columns([2, 1])
        
        with col1:
            # Generate and display plan
            plan = st.session_state.scheduler.generate_daily_plan()
            explanation = st.session_state.scheduler.explain_reasoning(plan)
            
            st.info(explanation)
        
        with col2:
            st.metric(
                "Available Time",
                f"{st.session_state.owner.daily_hours_available:.1f} hrs"
            )
            st.metric(
                "Tasks Scheduled",
                len(plan)
            )
            if plan:
                total_mins = st.session_state.scheduler.calculate_total_duration(plan)
                st.metric(
                    "Time Needed",
                    f"{total_mins//60}h {total_mins%60}m"
                )
        
        # Conflict detection
        conflicts = st.session_state.scheduler.detect_conflicts()
        if conflicts:
            st.warning(f"⚠️ {len(conflicts)} scheduling conflict(s) detected!")
            for task1, task2, time in conflicts:
                st.write(f"• **{task1.name}** and **{task2.name}** @ {time}")
        
        # Display schedule in table
        if plan:
            st.subheader("Scheduled Tasks")
            
            schedule_data = []
            for task in plan:
                schedule_data.append({
                    "Time": task.scheduled_time or "—",
                    "Task": task.name,
                    "Pet": task.assigned_pet or "General",
                    "Duration": f"{task.duration_minutes} min",
                    "Priority": f"{task.priority}/5"
                })
            
            st.table(schedule_data)
    
    # ========================================================================
    # TAB 3: Manage Tasks
    # ========================================================================
    
    with tab3:
        st.subheader("Manage Tasks")
        
        # Filter options
        col1, col2, col3 = st.columns(3)
        
        with col1:
            sort_by = st.radio(
                "Sort by",
                ["Time", "Priority"],
                key="sort_radio"
            )
        
        with col2:
            show_completed = st.checkbox(
                "Show completed tasks",
                value=False,
                key="show_completed_check"
            )
        
        with col3:
            filter_pet = st.selectbox(
                "Filter by pet",
                ["All"] + [p.name for p in st.session_state.scheduler.pets],
                key="filter_pet_select"
            )
        
        # Get filtered tasks
        if show_completed:
            tasks = st.session_state.scheduler.tasks
        else:
            tasks = st.session_state.scheduler.get_incomplete_tasks()
        
        if filter_pet != "All":
            tasks = [t for t in tasks if t.assigned_pet == filter_pet]
        
        # Sort tasks
        if sort_by == "Time":
            tasks = st.session_state.scheduler.sort_by_time(tasks)
        else:
            tasks = st.session_state.scheduler.sort_by_priority(tasks)
        
        # Display tasks with actions
        if tasks:
            for i, task in enumerate(tasks):
                col1, col2, col3 = st.columns([3, 1, 1])
                
                with col1:
                    st.write(task.get_details())
                
                with col2:
                    if not task.is_completed:
                        if st.button("✓ Complete", key=f"complete_{i}"):
                            task.mark_complete()
                            # Handle recurrence
                            new_task = st.session_state.scheduler.handle_recurring_task(task)
                            if new_task:
                                st.success(f"✓ Recurring task created for tomorrow")
                            st.rerun()
                    else:
                        if st.button("↩️ Undo", key=f"undo_{i}"):
                            task.mark_incomplete()
                            st.rerun()
                
                with col3:
                    if st.button("🗑️ Delete", key=f"delete_{i}"):
                        st.session_state.scheduler.tasks.remove(task)
                        st.rerun()
        else:
            st.info("No tasks to display.")
    
    # ========================================================================
    # TAB 4: Analytics
    # ========================================================================
    
    with tab4:
        st.subheader("📊 Schedule Analytics")
        
        all_tasks = st.session_state.scheduler.tasks
        incomplete = st.session_state.scheduler.get_incomplete_tasks()
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("Total Tasks", len(all_tasks))
        
        with col2:
            st.metric("Incomplete", len(incomplete))
        
        with col3:
            completed = len([t for t in all_tasks if t.is_completed])
            st.metric("Completed", completed)
        
        with col4:
            if all_tasks:
                completion_rate = (completed / len(all_tasks)) * 100
                st.metric("Completion Rate", f"{completion_rate:.0f}%")
        
        st.divider()
        
        # Tasks by pet
        if st.session_state.scheduler.pets:
            st.subheader("Tasks by Pet")
            for pet in st.session_state.scheduler.pets:
                pet_tasks = st.session_state.scheduler.get_tasks_for_pet(pet.name)
                pet_incomplete = [t for t in pet_tasks if not t.is_completed]
                st.write(f"**{pet.name}**: {len(pet_incomplete)} incomplete task(s)")
        
        # Time distribution
        if incomplete:
            st.subheader("Time Needed by Priority")
            
            priority_time = {}
            for task in incomplete:
                if task.priority not in priority_time:
                    priority_time[task.priority] = 0
                priority_time[task.priority] += task.duration_minutes
            
            for priority in sorted(priority_time.keys(), reverse=True):
                time_mins = priority_time[priority]
                st.write(f"Priority {priority}: {time_mins} minutes ({time_mins/60:.1f} hours)")

else:
    st.warning("👈 Please create an owner first to get started!")

col1, col2, col3 = st.columns(3)
with col1:
    task_title = st.text_input("Task title", value="Morning walk")
with col2:
    duration = st.number_input("Duration (minutes)", min_value=1, max_value=240, value=20)
with col3:
    priority = st.selectbox("Priority", ["low", "medium", "high"], index=2)

if st.button("Add task"):
    st.session_state.tasks.append(
        {"title": task_title, "duration_minutes": int(duration), "priority": priority}
    )

if st.session_state.tasks:
    st.write("Current tasks:")
    st.table(st.session_state.tasks)
else:
    st.info("No tasks yet. Add one above.")

st.divider()

st.subheader("Build Schedule")
st.caption("This button should call your scheduling logic once you implement it.")

if st.button("Generate schedule"):
    st.warning(
        "Not implemented yet. Next step: create your scheduling logic (classes/functions) and call it here."
    )
    st.markdown(
        """
Suggested approach:
1. Design your UML (draft).
2. Create class stubs (no logic).
3. Implement scheduling behavior.
4. Connect your scheduler here and display results.
"""
    )
