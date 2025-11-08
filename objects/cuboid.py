"""
Cuboid object for grasp planning.
"""
import pybullet as p
from .base_object import BaseObject


class CuboidObject(BaseObject):
    """
    Cuboid (rectangular box) object for grasping experiments.
    """
    
    def __init__(self, width=0.05, depth=0.05, height=0.8, mass=0.1, color=None):
        """
        Initialize a cuboid object.
        
        Args:
            width: Width along X-axis in meters
            depth: Depth along Y-axis in meters  
            height: Height along Z-axis in meters
            mass: Mass in kg
            color: RGBA color list
        """
        self.width = width
        self.depth = depth
        self.size = [width, depth, height]
        super().__init__(height=height, mass=mass, color=color)
    
    def create_shape(self):
        """
        Create cuboid visual and collision shapes.
        
        Returns:
            tuple: (visual_shape_id, collision_shape_id)
        """
        half_extents = [self.width / 2, self.depth / 2, self.height / 2]
        
        visual_shape_id = p.createVisualShape(
            shapeType=p.GEOM_BOX,
            halfExtents=half_extents,
            rgbaColor=self.color
        )
        
        collision_shape_id = p.createCollisionShape(
            shapeType=p.GEOM_BOX,
            halfExtents=half_extents
        )
        
        return visual_shape_id, collision_shape_id
    
    def get_grasp_center(self):
        """
        Get the center point for grasp planning.
        For cuboid: center of the object at mid-height.
        
        Returns:
            list: [x, y, z] coordinates
        """
        return [0, 0, self.height / 2]
    
    def get_dimensions(self):
        """Return cuboid dimensions."""
        return {
            'width': self.width,
            'depth': self.depth,
            'height': self.height
        }
