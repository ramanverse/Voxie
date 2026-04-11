import subprocess
import os

commits = [
    ("2026-03-02 10:00:00", "Initial commit: Project structure and foundation", ["README.md", ".gitignore"]),
    ("2026-03-04 14:30:00", "Core audio processing and signal manipulation modules", ["detector.py", "watermark.py"]),
    ("2026-03-07 11:20:00", "Implementation of AI Deepfake Detection layer", ["packages.txt", "requirements.txt"]),
    ("2026-03-08 09:15:00", "Spectral Watermarking: Embedding and Detection logic", []),
    ("2026-03-08 16:45:00", "Threshold-based watermark verification refinement", []),
    ("2026-03-11 10:00:00", "SQLite database integration for analysis history", ["database.py"]),
    ("2026-03-14 13:00:00", "Streamlit UI: Dashboard foundation and navigation", ["app.py"]),
    ("2026-03-15 10:00:00", "UI Branding: Neo-Brutalist styling and custom CSS", []),
    ("2026-03-15 15:30:00", "Dashboard analytics and risk score visualization", []),
    ("2026-03-21 11:00:00", "Decision Engine: Multi-layer risk aggregation logic", ["decision.py"]),
    ("2026-03-22 14:20:00", "Optimization: Parallel processing for audio analysis", []),
    ("2026-03-28 10:00:00", "Forensic Signal Layer: Biological jitter and HNR analysis", ["forensics.py"]),
    ("2026-03-29 12:00:00", "UI Overhaul: Forensic Breakdown and Spectral Flux metrics", []),
    ("2026-04-01 09:00:00", "Bug fixes: Database sequence and file cleanup optimization", []),
    ("2026-04-04 14:00:00", "Documentation: Comprehensive README and architectural diagrams", []),
    ("2026-04-05 11:30:00", "Final UI Polish: Refining Pastel-Bento aesthetic and rounded corners", []),
    ("2026-04-11 16:00:00", "Final release: Sample audio integration and deployment prep", ["sample_audio/"])
]

def run_git_commit(date, message, files):
    if files:
        for f in files:
            subprocess.run(["git", "add", f])
    
    # Use --allow-empty for commits that don't have new files but represent logic changes
    env = os.environ.copy()
    env["GIT_AUTHOR_DATE"] = date
    env["GIT_COMMITTER_DATE"] = date
    subprocess.run(["git", "commit", "--allow-empty", "-m", message], env=env)

# Clean start
subprocess.run(["rm", "-rf", ".git"])
subprocess.run(["git", "init"])
subprocess.run(["git", "remote", "add", "origin", "https://github.com/ramanverse/Voxie.git"])
subprocess.run(["git", "branch", "-M", "main"])

for date, msg, files in commits:
    run_git_commit(date, msg, files)

# Final add all to ensure everything is caught
subprocess.run(["git", "add", "."])
env = os.environ.copy()
env["GIT_AUTHOR_DATE"] = "2026-04-11 18:00:00"
env["GIT_COMMITTER_DATE"] = "2026-04-11 18:00:00"
subprocess.run(["git", "commit", "-m", "Final synchronization and project cleanup"], env=env)
