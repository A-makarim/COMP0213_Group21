# How to Use This Repository

This project simulates robotic grasps in PyBullet, collects data, trains a classifier (Random Forest), and evaluates grasp success. It’s organized for quick experiments and clear, object‑oriented structure.

Everything is working. noise and random.uniform and config parameters can be refiend more
Training datasets needs to be generateds, option(2)
Then test the classifier, option(3)
Get plots for courseworkreport, option(4) 

#

## Setup (Windows)
```powershell
# 1) Get the code
git clone https://github.com/A-makarim/Object-Oriented-Programming-Pybullet-Coursework-.git
cd Object-Oriented-Programming-Pybullet-Coursework-

# 2) Create and activate a virtual environment
python -m venv venv
venv\Scripts\activate

# 3) Install dependencies
pip install -r requirements.txt
```

## Project Structure
```
main.py                 # Menu-driven workflow: generate → train → test → visualize
train_model.py          # Model training helpers
evaluate.py             # Evaluation and metrics
visualize.py            # Visualization module
robots/                 # Gripper implementations (PR2, SDH)
  gripper.py
  gripper_factory.py
objects/                # Object implementations (Cuboid, Cylinder)
  base_object.py
  cuboid.py
  cylinder.py
  object_factory.py
data/                   # CSV datasets (training/test and with predictions)
models/                 # Trained models (.pkl) and URDFs
images/                 # Generated plots
requirements.txt
```## Run the Workflow
Launch the interactive menu and follow the on-screen prompts:
```powershell
python main.py
```
You’ll:
1) Generate training data (choose gripper and object) → CSV saved in `data/`
2) Train the classifier → model file (.pkl) saved in `models/`
3) Test the classifier → predictions appended to a new CSV in `data/`
4) Visualize results → plots saved in `images/`

## Data Files
- Training CSV examples: `data/grasp_data_cuboid.csv`, `data/grasp_data_cylinder.csv`
- After testing, updated CSVs with predictions: `data/updated_*_with_predictions.csv`

Columns (training):
```
Position X, Position Y, Position Z,
Orientation Roll, Orientation Pitch, Orientation Yaw,
Initial Z, Final Z, Delta Z, Success
