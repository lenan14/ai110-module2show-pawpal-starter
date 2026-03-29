"""
PawPal+ System Design
Core logic layer with Owner, Pet, Task, and Scheduler classes
"""

from dataclasses import dataclass, field
from typing import List, Optional
from enum import Enum


class TaskType(Enum):
    """Types of pet care tasks"""
    WALK = "walk"
    FEEDING = "feeding"
    MEDICATION = "medication"
    ENRICHMENT = "enrichment"
    GROOMING = "grooming"
    TRAINING = "training"


class PetType(Enum):
    """Types of pets"""
    DOG = "dog"
    CAT = "cat"
    BIRD = "bird"
    RABBIT = "rabbit"
    OTHER = "other"


@dataclass
class Owner:
    """Represents a pet owner"""
    name: str
    daily_hours_available: float  # Hours available per day (e.g., 4.5)
    preferences: dict = field(default_factory=dict)  # Custom preferences
    
    def set_availability(self, hours: float) -> None:
        """Set the owner's available hours per day"""
        pass
    
    def get_preferences(self) -> dict:
        """Retrieve owner preferences"""
        pass


@dataclass
class Pet:
    """Represents a pet"""
    name: str
    pet_type: PetType
    age: int  # In years
    special_needs: List[str] = field(default_factory=list)  # e.g., ["diabetic", "senior"]
    
    def get_info(self) -> str:
        """Return a description of the pet"""
        pass
    
    def has_constraint(self, constraint: str) -> bool:
        """Check if pet has a specific constraint"""
        pass


@dataclass
class Task:
    """Represents a pet care task"""
    name: str
    duration_minutes: int
    priority: int  # 1-5 scale, 5 being highest
    task_type: TaskType
    description: str = ""
    repeat_frequency: str = "daily"  # "daily", "weekly", "as-needed"
    assigned_pet: Optional[str] = None  # Pet name or None if for all pets
    
    def validate(self) -> bool:
        """Ensure task has valid attributes"""
        pass
    
    def get_details(self) -> str:
        """Return task details as a string"""
        pass


@dataclass
class Scheduler:
    """Main scheduler that creates daily plans"""
    owner: Owner
    pets: List[Pet] = field(default_factory=list)
    tasks: List[Task] = field(default_factory=list)
    
    def add_pet(self, pet: Pet) -> None:
        """Add a pet to be scheduled for"""
        pass
    
    def add_task(self, task: Task) -> None:
        """Add a task to the scheduler"""
        pass
    
    def generate_daily_plan(self) -> List[Task]:
        """Create an optimized schedule for today"""
        pass
    
    def explain_reasoning(self, plan: List[Task]) -> str:
        """Explain why tasks were scheduled in this order"""
        pass
    
    def calculate_total_duration(self, plan: List[Task]) -> int:
        """Calculate total time needed for a plan (in minutes)"""
        pass
