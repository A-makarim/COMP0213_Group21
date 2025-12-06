"""
batch_generate.py - Automated batch data generation for all gripper-object combinations

Run this script to generate grasp data for all 4 combinations:
- PR2 gripper × cuboid
- PR2 gripper × cylinder
- SDH gripper × cuboid
- SDH gripper × cylinder

The script will run data generation for each combination sequentially and append
to existing CSV files, allowing you to accumulate large datasets over multiple runs.

Usage:
    python batch_generate.py --grasps 100
    python batch_generate.py --grasps 50 --gui
    python batch_generate.py --grasps 200 --combinations pr2-cuboid sdh-cylinder
"""

import argparse
import os
import sys
import time
from datetime import datetime

# Import from main.py
from main import generate_data_for_shape


def print_banner(text):
    """Print a formatted banner."""
    print("\n" + "=" * 70)
    print(f"  {text}")
    print("=" * 70 + "\n")


def run_batch_generation(grasps_per_case, combinations=None, use_gui=False):
    """
    Run data generation for all specified gripper-object combinations.
    
    Args:
        grasps_per_case: Number of grasps to generate per combination
        combinations: List of combinations to run (e.g., ['pr2-cuboid', 'sdh-cylinder'])
                     If None, runs all 4 combinations
        use_gui: Whether to use GUI mode (slower but visual feedback)
    """
    # Define all possible combinations
    all_combinations = [
        ("pr2", "cuboid"),
        ("pr2", "cylinder"),
        ("sdh", "cuboid"),
        ("sdh", "cylinder")
    ]
    
    # Filter combinations if specified
    if combinations:
        combo_dict = {f"{g}-{o}": (g, o) for g, o in all_combinations}
        selected = [combo_dict[c] for c in combinations if c in combo_dict]
        if not selected:
            print("[ERROR] No valid combinations specified. Available: pr2-cuboid, pr2-cylinder, sdh-cuboid, sdh-cylinder")
            return
    else:
        selected = all_combinations
    
    # Print configuration
    print_banner("BATCH DATA GENERATION")
    print(f"Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"Grasps per combination: {grasps_per_case}")
    print(f"Total combinations: {len(selected)}")
    print(f"Total grasps this run: {grasps_per_case * len(selected)}")
    print(f"GUI mode: {'Enabled' if use_gui else 'Disabled (DIRECT mode - faster)'}")
    print(f"\nCombinations to process:")
    for gripper, shape in selected:
        print(f"  - {gripper.upper()} gripper × {shape}")
    print()
    
    # Track statistics
    start_time = time.time()
    results = []
    
    # Run each combination
    for idx, (gripper_type, object_type) in enumerate(selected, 1):
        combo_name = f"{gripper_type.upper()} × {object_type}"
        print_banner(f"Combination {idx}/{len(selected)}: {combo_name}")
        
        combo_start = time.time()
        
        try:
            # Call the generation function from main.py
            print(f"[INFO] Starting generation of {grasps_per_case} grasps...")
            generate_data_for_shape(
                object_type=object_type,
                num_grasps=grasps_per_case,
                gripper_type=gripper_type
            )
            
            combo_duration = time.time() - combo_start
            results.append({
                'combination': combo_name,
                'grasps': grasps_per_case,
                'duration': combo_duration,
                'status': 'SUCCESS'
            })
            
            print(f"\n[SUCCESS] Completed {combo_name} in {combo_duration:.1f} seconds")
            print(f"           ({combo_duration/grasps_per_case:.2f} seconds per grasp)")
            
        except KeyboardInterrupt:
            print("\n[WARNING] User interrupted batch generation.")
            results.append({
                'combination': combo_name,
                'grasps': 0,
                'duration': time.time() - combo_start,
                'status': 'INTERRUPTED'
            })
            break
            
        except Exception as e:
            combo_duration = time.time() - combo_start
            print(f"\n[ERROR] Failed to generate data for {combo_name}: {str(e)}")
            results.append({
                'combination': combo_name,
                'grasps': 0,
                'duration': combo_duration,
                'status': f'FAILED: {str(e)}'
            })
    
    # Print final summary
    total_duration = time.time() - start_time
    successful = sum(1 for r in results if r['status'] == 'SUCCESS')
    total_grasps = sum(r['grasps'] for r in results)
    
    print_banner("BATCH GENERATION SUMMARY")
    print(f"Total time: {total_duration:.1f} seconds ({total_duration/60:.1f} minutes)")
    print(f"Successful combinations: {successful}/{len(selected)}")
    print(f"Total grasps generated: {total_grasps}")
    if total_grasps > 0:
        print(f"Average time per grasp: {total_duration/total_grasps:.2f} seconds")
    print("\nDetailed Results:")
    for result in results:
        status_icon = "✓" if result['status'] == 'SUCCESS' else "✗"
        print(f"  {status_icon} {result['combination']:20} | "
              f"Grasps: {result['grasps']:4} | "
              f"Duration: {result['duration']:6.1f}s | "
              f"Status: {result['status']}")
    
    print("\n[INFO] Data files location: ./data/")
    print("[INFO] Files: grasp_data_{gripper}_{shape}.csv")
    print("=" * 70 + "\n")
    
    return results


def main():
    parser = argparse.ArgumentParser(
        description="Batch generate grasp data for all gripper-object combinations",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Generate 100 grasps per combination (400 total)
  python batch_generate.py --grasps 100
  
  # Generate 50 grasps with GUI visualization
  python batch_generate.py --grasps 50 --gui
  
  # Generate only specific combinations
  python batch_generate.py --grasps 200 --combinations pr2-cuboid sdh-cylinder
  
  # Quick test run (10 grasps each)
  python batch_generate.py --grasps 10
        """
    )
    
    parser.add_argument(
        '--grasps',
        type=int,
        required=True,
        help='Number of grasps to generate per combination'
    )
    
    parser.add_argument(
        '--gui',
        action='store_true',
        help='Use GUI mode (slower, but provides visual feedback)'
    )
    
    parser.add_argument(
        '--combinations',
        nargs='+',
        choices=['pr2-cuboid', 'pr2-cylinder', 'sdh-cuboid', 'sdh-cylinder'],
        help='Specific combinations to run (default: all 4)'
    )
    
    args = parser.parse_args()
    
    # Validate grasps
    if args.grasps < 1:
        print("[ERROR] Number of grasps must be at least 1")
        sys.exit(1)
    
    # Run batch generation
    try:
        run_batch_generation(
            grasps_per_case=args.grasps,
            combinations=args.combinations,
            use_gui=args.gui
        )
    except KeyboardInterrupt:
        print("\n[INFO] Batch generation interrupted by user.")
        sys.exit(0)


if __name__ == "__main__":
    main()
