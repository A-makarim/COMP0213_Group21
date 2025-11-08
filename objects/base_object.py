"""
Base class for graspable objects in the simulation.
Follows OOP principles with abstract base class and inheritance.
"""
from abc import ABC, abstractmethod
import pybullet as p


class BaseObject(ABC):
    """
    Abstract base class for graspable objects.
    All objects must implement the create_shape method.
    """
    
    def __init__(self, height=0.8, mass=0.1, color=None):
        """
        Initialize base object properties.
        
        Args:
            height: Height of the object in meters
            mass: Mass of the object in kg
            color: RGBA color list [R, G, B, A], defaults to white
        """
        self.height = height
        self.mass = mass
        self.color = color if color else [1, 1, 1, 1]
        self.object_id = None
        self._create_object()
    
    def _create_object(self):
        """Create the object in PyBullet simulation."""
        visual_shape_id, collision_shape_id = self.create_shape()
        
        self.object_id = p.createMultiBody(
            baseMass=self.mass,
            baseInertialFramePosition=[0, 0, 0],
            baseCollisionShapeIndex=collision_shape_id,
            baseVisualShapeIndex=visual_shape_id,
            basePosition=self.get_spawn_position(),
            useMaximalCoordinates=False
        )
        
        # Set object dynamics
        p.changeDynamics(
            self.object_id, -1,
            lateralFriction=1.2,
            spinningFriction=0.1
        )
    
    @abstractmethod
    def create_shape(self):
        """
        Create visual and collision shapes for the object.
        Must be implemented by subclasses.
        
        Returns:
            tuple: (visual_shape_id, collision_shape_id)
        """
        pass
    
    @abstractmethod
    def get_grasp_center(self):
        """
        Get the center point for grasp planning.
        Must be implemented by subclasses.
        
        Returns:
            list: [x, y, z] coordinates of grasp center
        """
        pass
    
    def get_spawn_position(self):
        """
        Get the spawn position for the object.
        Default: center at height/2 above ground.
        
        Returns:
            list: [x, y, z] spawn position
        """
        return [0, 0, self.height / 2]
    
    def get_id(self):
        """Return the PyBullet body ID."""
        return self.object_id
    
    def get_height(self):
        """Return object height."""
        return self.height
    
    def reset_position(self, position=None, orientation=None):
        """
        Reset object to initial position and orientation.
        
        Args:
            position: [x, y, z] position, defaults to spawn position
            orientation: Quaternion [x, y, z, w], defaults to upright
        """
        if position is None:
            position = self.get_spawn_position()
        if orientation is None:
            orientation = [0, 0, 0, 1]
        
        p.resetBasePositionAndOrientation(self.object_id, position, orientation)
