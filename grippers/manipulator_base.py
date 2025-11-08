"""
Manipulator Interface Module
Abstract base classes for robotic end-effectors
"""
import pybullet as p
import time
from abc import ABC, abstractmethod


class ManipulatorInterface(ABC):
    """
    Abstract interface defining manipulator behavior contract
    Concrete implementations must provide activation and deactivation logic
    """
    
    def __init__(self, spawn_position, spawn_orientation, model_path):
        """
        Initialize manipulator with given configuration
        
        Args:
            spawn_position: Initial XYZ coordinates
            spawn_orientation: Initial quaternion orientation
            model_path: Path to URDF model file
        """
        self.spawn_position = spawn_position
        self.spawn_orientation = spawn_orientation
        self.model_path = model_path

        self.body_id = p.loadURDF(
            self.model_path,
            basePosition=self.spawn_position,
            baseOrientation=self.spawn_orientation,
            useFixedBase=False
        )

        # Configure physics properties for easy manipulation
        p.changeDynamics(self.body_id, -1, mass=0)

        self.movable_joints, self.static_joints = self._extract_joint_indices()

    def _extract_joint_indices(self):
        """Extract movable and fixed joint indices"""
        movable, static = [], []
        total_joints = p.getNumJoints(self.body_id)
        
        for joint_idx in range(total_joints):
            joint_data = p.getJointInfo(self.body_id, joint_idx)
            if joint_data[2] != p.JOINT_FIXED:
                movable.append(joint_idx)
            else:
                static.append(joint_idx)
                
        return movable, static

    def get_body_id(self):
        """Returns PyBullet body identifier"""
        return self.body_id

    def run_simulation(self, num_steps=500, step_delay=0.001):
        """Execute physics simulation for specified iterations"""
        for _ in range(num_steps):
            p.stepSimulation()
            time.sleep(step_delay)

    @abstractmethod
    def activate(self):
        """
        Activate manipulator (open fingers/jaws)
        Must be overridden by subclass
        """
        raise NotImplementedError("Subclass must implement activate()")

    @abstractmethod
    def deactivate(self):
        """
        Deactivate manipulator (close fingers/jaws for grasping)
        Must be overridden by subclass
        """
        raise NotImplementedError("Subclass must implement deactivate()")

    def relocate(self, new_position, new_orientation):
        """Update manipulator pose in simulation"""
        p.resetBasePositionAndOrientation(
            self.body_id, new_position, new_orientation
        )

    def execute_vertical_motion(self, target_height, motion_steps=200, step_time=0.01):
        """
        Smoothly move manipulator vertically using velocity control
        
        Args:
            target_height: Desired Z coordinate
            motion_steps: Number of simulation steps
            step_time: Time delay per step
        """
        current_pose, current_rot = p.getBasePositionAndOrientation(self.body_id)
        initial_height = current_pose[2]
        height_increment = (target_height - initial_height) / motion_steps if motion_steps > 0 else 0.0
        vertical_velocity = height_increment / step_time if step_time > 0 else 0.0

        for _ in range(motion_steps):
            p.resetBaseVelocity(
                self.body_id, linearVelocity=[0, 0, vertical_velocity]
            )
            p.stepSimulation()
            time.sleep(step_time)

        # Halt motion
        p.resetBaseVelocity(self.body_id, linearVelocity=[0, 0, 0])


class TwoFingerManipulator(ManipulatorInterface):
    """PR2-style two-finger parallel jaw gripper"""
    
    def __init__(self, spawn_position, spawn_orientation):
        super().__init__(spawn_position, spawn_orientation, "pr2_gripper.urdf")

    def activate(self):
        """Open jaw configuration"""
        jaw_open_angles = [0.548, 0.548]
        
        for joint_id, angle in zip(self.movable_joints, jaw_open_angles):
            p.setJointMotorControl2(
                bodyIndex=self.body_id,
                jointIndex=joint_id,
                controlMode=p.POSITION_CONTROL,
                targetPosition=angle,
                force=500
            )

    def deactivate(self):
        """Close jaw to grasp"""
        jaw_close_angles = [0.0, 0.0]
        
        for joint_id, angle in zip(self.movable_joints, jaw_close_angles):
            p.setJointMotorControl2(
                bodyIndex=self.body_id,
                jointIndex=joint_id,
                controlMode=p.POSITION_CONTROL,
                targetPosition=angle,
                force=500
            )
