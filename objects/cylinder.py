"""
Cylinder object for grasp planning.
"""
import pybullet as p
from .base_object import BaseObject


class CylinderObject(BaseObject):
    """
    Cylindrical object for grasping experiments.
    """
    
    def __init__(self, radius=0.04, height=0.8, mass=0.1, color=None):
        """
        Initialize a cylinder object.
        
        Args:
            radius: Radius of cylinder in meters
            height: Height of cylinder in meters
            mass: Mass in kg
            color: RGBA color list
        """
        self.radius = radius
        super().__init__(height=height, mass=mass, color=color)
    
    def create_shape(self):
        """
        Create cylinder visual and collision shapes.
        
        Returns:
            tuple: (visual_shape_id, collision_shape_id)
        """
        visual_shape_id = p.createVisualShape(
            shapeType=p.GEOM_CYLINDER,
            radius=self.radius,
            length=self.height,
            rgbaColor=self.color
        )
        
        collision_shape_id = p.createCollisionShape(
            shapeType=p.GEOM_CYLINDER,
            radius=self.radius,
            height=self.height
        )
        
        return visual_shape_id, collision_shape_id
    
    def get_grasp_center(self):
        """
        Get the center point for grasp planning.
        For cylinder: center of the object at mid-height.
        
        Returns:
            list: [x, y, z] coordinates
        """
        return [0, 0, self.height / 2]
    
    def get_dimensions(self):
        """Return cylinder dimensions."""
        return {
            'radius': self.radius,
            'height': self.height
        }
