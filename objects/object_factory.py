"""
Factory for creating graspable objects.
"""
from .cuboid import CuboidObject
from .cylinder import CylinderObject


class ObjectFactory:
    """
    Factory class for creating different types of graspable objects.
    Follows Factory design pattern.
    """
    
    @staticmethod
    def create_object(object_type, **kwargs):
        """
        Create an object of the specified type.
        
        Args:
            object_type: Type of object ('cuboid' or 'cylinder')
            **kwargs: Additional parameters for object creation
            
        Returns:
            BaseObject: Instance of the requested object type
            
        Raises:
            ValueError: If object_type is not supported
        """
        object_type = object_type.lower()
        
        if object_type == "cuboid":
            return CuboidObject(**kwargs)
        elif object_type == "cylinder":
            return CylinderObject(**kwargs)
        else:
            raise ValueError(
                f"Unsupported object type: '{object_type}'. "
                f"Supported types: 'cuboid', 'cylinder'"
            )
    
    @staticmethod
    def get_supported_types():
        """Return list of supported object types."""
        return ['cuboid', 'cylinder']
