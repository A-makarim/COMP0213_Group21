"""
Performance Assessment Module
Evaluates grasp attempts and records metrics to CSV format
"""
import pybullet as p
import time
import os
import csv


class PerformanceMetrics:
    """
    Assesses grasp performance and logs results to file
    """
    
    def __init__(self, output_path="grasp_metrics.csv"):
        self.output_path = output_path
        self.column_names = [
            "Position X", "Position Y", "Position Z",
            "Orientation Roll", "Orientation Pitch", "Orientation Yaw",
            "Initial Z", "Final Z", "Delta Z",
            "Success"
        ]
        self._initialize_csv()

    def _initialize_csv(self):
        """Create CSV file with headers if it doesn't exist"""
        if not os.path.isfile(self.output_path):
            with open(self.output_path, mode="w", newline="") as f:
                csv_writer = csv.writer(f)
                csv_writer.writerow(self.column_names)

    def assess_grasp_quality(self, target_id, start_position):
        """
        Determine grasp success based on vertical displacement
        
        Returns:
            status_code: Integer indicating success level
            vertical_delta: Change in Z position
            end_position: Final object position
        """
        time.sleep(0.5)
        
        if not p.isConnected():
            return 0, 0.0, start_position

        end_position, _ = p.getBasePositionAndOrientation(target_id)
        
        z_initial = start_position[2]
        z_final = end_position[2]
        vertical_delta = z_final - z_initial

        # Determine success level based on lift height
        if vertical_delta > 0.1:
            status_code = 1  # Full success
        elif 0.05 <= vertical_delta <= 0.1:
            status_code = 2  # Partial success
        else:
            status_code = 0  # Failed

        return status_code, vertical_delta, end_position

    def record_attempt(self, metrics_data):
        """
        Log grasp attempt metrics to CSV (checks for duplicates)
        
        Args:
            metrics_data: List containing [pos_x, pos_y, pos_z, roll, pitch, yaw,
                                          init_z, final_z, delta_z, success]
        """
        existing_records = set()
        
        if os.path.isfile(self.output_path):
            with open(self.output_path, mode="r") as f:
                reader = csv.reader(f)
                next(reader, None)  # Skip header row
                for record in reader:
                    existing_records.add(tuple(record))

        record_tuple = tuple(map(str, metrics_data))
        
        if record_tuple not in existing_records:
            with open(self.output_path, mode="a", newline="") as f:
                csv_writer = csv.writer(f)
                csv_writer.writerow(metrics_data)
        else:
            print("[WARNING] Duplicate entry detected - skipping")
