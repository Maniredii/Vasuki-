import zipfile
import json
import os

zip_path = "vasuki_phase7_output.zip"
if not os.path.exists(zip_path):
    print("Zip file not found!")
    exit(1)

z = zipfile.ZipFile(zip_path)
state_data = json.loads(z.read("checkpoint-650/trainer_state.json").decode("utf-8"))

print("=" * 70)
print("VASUKI Phase 7: Training Run Metrics & Evaluation Log")
print("=" * 70)
print(f"Total Epochs Completed: {state_data.get('epoch', 0):.2f}")
print(f"Total Global Steps:     {state_data.get('global_step', 0)}")

logs = state_data.get("log_history", [])
print("\nLoss Trajectory across Steps:")
print(f"{'Step':<8} | {'Train Loss':<12} | {'Eval Loss':<12} | {'Grad Norm':<10}")
print("-" * 50)
for entry in logs:
    step = entry.get("step", "-")
    train_loss = f"{entry['loss']:.4f}" if "loss" in entry else "-"
    eval_loss = f"{entry['eval_loss']:.4f}" if "eval_loss" in entry else "-"
    grad_norm = f"{entry['grad_norm']:.2f}" if "grad_norm" in entry else "-"
    if train_loss != "-" or eval_loss != "-":
        print(f"{step:<8} | {train_loss:<12} | {eval_loss:<12} | {grad_norm:<10}")

print("=" * 70)
