"""
Factory for creating gripper instances.
"""
from .gripper import PR2Gripper, SDHGripper, CustomGripper


class GripperFactory:
    """
    Factory class for creating different types of grippers.
    Follows Factory design pattern.
    """
    
    @staticmethod
    def create_gripper(gripper_type, position, orientation):
        """
        Create a gripper of the specified type.
        
        Args:
            gripper_type: Type of gripper ('pr2', 'sdh', or 'custom')
            position: Initial position [x, y, z]
            orientation: Initial orientation as quaternion [x, y, z, w]
            
        Returns:
            BaseGripper: Instance of the requested gripper type
            
        Raises:
            ValueError: If gripper_type is not supported
        """
        gripper_type = gripper_type.lower()
        
        if gripper_type == "pr2":
            return PR2Gripper(position, orientation)
        elif gripper_type == "sdh":
            return SDHGripper(position, orientation)
        elif gripper_type == "custom":
            return CustomGripper(position, orientation)
        else:
            raise ValueError(
                f"Unsupported gripper type: '{gripper_type}'. "
                f"Supported types: 'pr2', 'sdh', 'custom'"
            )
    
    @staticmethod
    def get_supported_types():
        """Return list of supported gripper types."""
        return ['pr2', 'sdh', 'custom']
