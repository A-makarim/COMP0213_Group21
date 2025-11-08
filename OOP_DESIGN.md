# OOP Design Documentation

## Overview
This grasp planning system implements proper Object-Oriented Programming principles as required by COMP0213 coursework.

## Class Structure

### 1. Abstract Base Classes

#### `BaseGripper` (robots/gripper.py)
- **Purpose**: Abstract base class for all grippers
- **Abstract Methods**:
  - `open_gripper()`: Must be implemented by subclasses
  - `close_gripper()`: Must be implemented by subclasses
- **Concrete Methods**:
  - `get_joint_info()`: Retrieves joint information
  - `set_position()`: Moves gripper to specified pose
  - `move_up_smoothly()`: Lifts gripper gradually
  - `get_id()`: Returns PyBullet body ID

#### `BaseObject` (objects/base_object.py)
- **Purpose**: Abstract base class for all graspable objects
- **Abstract Methods**:
  - `create_shape()`: Must return visual and collision shapes
  - `get_grasp_center()`: Must return center point for grasping
- **Concrete Methods**:
  - `get_spawn_position()`: Returns spawn coordinates
  - `reset_position()`: Resets object to initial state
  - `get_id()`: Returns PyBullet body ID
  - `get_height()`: Returns object height

### 2. Concrete Implementations

#### Grippers
- **`PR2Gripper`**: Two-finger parallel gripper
  - Implements open/close with joint positions 0.548 (open) and 0.0 (closed)
  - Uses direct approach (no pre-grasp phase)

- **`SDHGripper`**: Three-finger Schunk Dexterous Hand
  - Implements open/close with joint positions -0.5 (open) and 1.0 (closed)
  - Uses gradual approach phase with progressive finger closing
  - Fingers spread outward on initialization

- **`CustomGripper`**: Placeholder for extensibility

#### Objects
- **`CuboidObject`**: Rectangular box (5cm × 5cm × 80cm)
  - Creates box collision and visual shapes
  - Grasp center at geometric center

- **`CylinderObject`**: Circular cylinder (radius 6cm, height 80cm)
  - Creates cylinder collision and visual shapes
  - Grasp center at geometric center

### 3. Factory Pattern

#### `GripperFactory` (robots/gripper_factory.py)
```python
gripper = GripperFactory.create_gripper("pr2", position, orientation)
```
- Encapsulates gripper instantiation logic
- Provides centralized creation point
- Easy to extend with new gripper types

#### `ObjectFactory` (objects/object_factory.py)
```python
obj = ObjectFactory.create_object("cuboid", width=0.05, height=0.8)
```
- Encapsulates object instantiation logic
- Provides centralized creation point
- Easy to extend with new object types

## OOP Principles Applied

### 1. **Abstraction**
- Base classes define interfaces without implementation details
- Users interact with abstract interfaces, not concrete implementations

### 2. **Encapsulation**
- Object properties hidden behind getter methods
- Configuration data stored in dictionaries
- Internal methods prefixed with `_` (e.g., `_create_object()`)

### 3. **Inheritance**
- All grippers inherit from `BaseGripper`
- All objects inherit from `BaseObject`
- Shared functionality in base class, specific behavior in subclasses

### 4. **Polymorphism**
- Different grippers respond differently to `open_gripper()` call
- Different objects create different shapes with `create_shape()`
- Code works with base class references, actual behavior determined at runtime

## Configuration-Driven Design

### GRIPPER_CONFIG Dictionary
```python
GRIPPER_CONFIG = {
    "pr2": {
        "cuboid_radius": 0.25,
        "approach_distance": 0.0
    },
    "sdh": {
        "cuboid_radius": 0.22,
        "approach_distance": 0.05
    }
}
```
- Separates configuration from code
- Easy to tune parameters per gripper
- Supports adding new gripper configurations

## Extensibility

### Adding a New Gripper
1. Create new class inheriting from `BaseGripper`
2. Implement `open_gripper()` and `close_gripper()`
3. Add to `GripperFactory.create_gripper()`
4. Add configuration to `GRIPPER_CONFIG`

### Adding a New Object
1. Create new class inheriting from `BaseObject`
2. Implement `create_shape()` and `get_grasp_center()`
3. Add to `ObjectFactory.create_object()`

## Design Patterns Summary

| Pattern | Location | Purpose |
|---------|----------|---------|
| Abstract Base Class | `BaseGripper`, `BaseObject` | Define interfaces for extensibility |
| Factory | `GripperFactory`, `ObjectFactory` | Centralize object creation |
| Strategy | Gripper approach methods | Different grasping strategies per gripper |
| Template Method | `BaseObject._create_object()` | Define algorithm skeleton, subclasses fill details |

## Benefits of This Design

1. **Maintainability**: Changes to one gripper don't affect others
2. **Extensibility**: Easy to add new grippers and objects
3. **Testability**: Each class can be tested independently
4. **Reusability**: Base classes provide common functionality
5. **Clarity**: Clear separation of concerns and responsibilities
