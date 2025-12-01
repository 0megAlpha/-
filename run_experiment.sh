#!/usr/bin/env bash
# Minimal launcher with your original env block restored.
# - Uses bash (not sh)
# - Initializes conda in a non-interactive shell
# - Activates the target env
# - Restores your GPU/env block EXACTLY as provided
# - Runs your command

set -euo pipefail

echo "=== Starting Black-box Model Experiment ==="

# # 1) Locate conda executable (prefer PATH; fallback to common install paths).
# if command -v conda >/dev/null 2>&1; then
#   CONDA_EXE="$(command -v conda)"
# elif [ -x "$HOME/miniconda3/bin/conda" ]; then
#   CONDA_EXE="$HOME/miniconda3/bin/conda"
# elif [ -x "/home/jovyan/miniconda3/bin/conda" ]; then
#   CONDA_EXE="/home/jovyan/miniconda3/bin/conda"
# else
#   echo "Error: 'conda' not found. Install Miniconda or add it to PATH."
#   exit 1
# fi

# # 2) Initialize conda for this bash process (no profile files needed).
# eval "$("$CONDA_EXE" shell.bash hook)"

# # 3) Activate your environment.
# echo "Activating conda environment..."
# conda activate correlated-knowledge-jailbreak || {
#   echo "Error: Failed to activate 'correlated-knowledge-jailbreak'"
#   exit 1
# }
# echo "Conda environment activated: $(python -V)"

# 4) === YOUR ORIGINAL ENV VAR BLOCK (restored, unchanged) ===
echo "Setting GPU environment variables..."
# Whitebox model uses GPU 0, Judge model uses GPU 1
# Total: 2 GPUs needed, using 0,1
export CUDA_LAUNCH_BLOCKING=1
export CUDA_CACHE_PATH=/tmp/cuda_cache
export CUDA_VISIBLE_DEVICES=0,1
export TOKENIZERS_PARALLELISM=false 
export NLTK_DATA=/home/rongzhe/nltk_data
echo "CUDA_VISIBLE_DEVICES set to: $CUDA_VISIBLE_DEVICES"
# === end of your original block ===

# 5) Ensure we run from the repo root (directory of this script).
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

# (Optional) quick sanity checks.
if [ ! -f "main.py" ]; then
  echo "Error: main.py not found in $(pwd)"
  exit 1
fi
if [ ! -f "config/config.yml" ]; then
  echo "Error: config/config.yml not found"
  exit 1
fi
echo "Configuration file found"

# 6) Run your original command.
# Usage examples:
# - Full pipeline:   python main.py --config config/config.yml --phase full --verbose
# - Jailbreak only:  python main.py --config config/config.yml --phase jailbreak --verbose
# - Judge only:      python main.py --config config/config.yml --phase judge --verbose
# - Resume:          python main.py --config config/config.yml --phase resume --verbose
echo "Starting experiment with main.py..."
python main.py --config config/config.yml --phase full --verbose

echo
echo "=== Experiment finished ==="
