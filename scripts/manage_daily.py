import os
import sys
import subprocess
from datetime import datetime

TEMPLATE = """# What I built
[Replace this with a 1-sentence summary of what you built]

# What I learned
[Replace this with bullet points of key takeaways]

# What's next
[Replace this with tomorrow's goals]
"""

def run_cmd(cmd):
    """Executes a shell command and returns output and status code."""
    result = subprocess.run(cmd, shell=True, text=True, capture_output=True)
    return result.stdout.strip(), result.returncode

def main():
    # Setup paths
    # Assuming script is in /scripts, so repo root is one level up
    repo_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
    today = datetime.now().strftime("%Y-%m-%d")
    daily_dir = os.path.join(repo_root, "daily", today)
    file_path = os.path.join(daily_dir, "README.md")
    
    # 1. Scaffolding Phase: Create file if it doesn't exist
    if not os.path.exists(file_path):
        os.makedirs(daily_dir, exist_ok=True)
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(TEMPLATE)
        print(f"✅ Created template for today at daily/{today}/README.md")
        print("💡 Fill it out and run this script again to commit your work.")
        sys.exit(0)
        
    # 2. Content Validation Phase: Check for unmodified template
    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()
        
    if "[Replace this" in content or content.strip() == TEMPLATE.strip():
        print("⚠️  Warning: Today's entry still contains template placeholders.")
        print("   Please update the file with real content before committing.")
        sys.exit(1)
        
    # 3. Dynamic Commit Message Generation
    lines = content.split('\n')
    commit_msg = f"Daily update: {today}"
    for i, line in enumerate(lines):
        if "What I built" in line and i + 1 < len(lines):
            potential_msg = lines[i+1].strip()
            if potential_msg:
                commit_msg = potential_msg
                break
                
    # 4. Stage changes
    # Use relative path for git commands from repo root
    rel_path = f"daily/{today}/README.md"
    run_cmd(f'cd "{repo_root}" && git add "{rel_path}"')
    
    # 5. Idempotency Check: Verify the diff isn't empty
    diff_output, _ = run_cmd(f'cd "{repo_root}" && git diff --cached --name-only')
    # Windows paths in git bash might use forward slashes, so we check just the filename/path
    if "README.md" not in diff_output:
        print("ℹ️  No new content to commit. (Did you already commit today?)")
        sys.exit(0)
        
    # 6. Commit and Push
    _, code = run_cmd(f'cd "{repo_root}" && git commit -m "{commit_msg}"')
    if code == 0:
        print(f"🎉 Successfully committed: '{commit_msg}'")
        push_out, push_code = run_cmd(f'cd "{repo_root}" && git push')
        if push_code == 0:
            print("🚀 Successfully pushed to remote!")
        else:
            print(f"❌ Error pushing to remote: {push_out}")
            sys.exit(1)
    else:
        print("❌ Failed to commit.")
        sys.exit(1)

if __name__ == "__main__":
    main()
