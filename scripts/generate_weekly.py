import os
from datetime import datetime, timedelta

def main():
    repo_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
    today = datetime.now()
    week_start = today - timedelta(days=6)
    
    summary_lines = [f"# Weekly Summary: {week_start.strftime('%Y-%m-%d')} to {today.strftime('%Y-%m-%d')}\n"]
    entries_found = 0
    
    # Look back over the last 7 days
    for i in range(6, -1, -1):
        date_str = (today - timedelta(days=i)).strftime("%Y-%m-%d")
        file_path = os.path.join(repo_root, "daily", date_str, "README.md")
        
        if os.path.exists(file_path):
            with open(file_path, "r", encoding="utf-8") as f:
                content = f.read()
            
            # Only include it if it's actually been filled out
            if "[Replace this" not in content: 
                summary_lines.append(f"## {date_str}")
                lines = content.split('\n')
                for j, line in enumerate(lines):
                    if "What I built" in line and j + 1 < len(lines):
                        summary_lines.append(f"- **Built:** {lines[j+1].strip()}")
                    elif "What I learned" in line and j + 1 < len(lines):
                        # Grab the first bullet point of learning as a highlight
                        summary_lines.append(f"- **Learned:** {lines[j+1].strip()}")
                        break
                summary_lines.append("") # Empty line for spacing
                entries_found += 1
                
    if entries_found == 0:
        print("No valid entries found for the past 7 days. Go write some code!")
        return
        
    week_number = today.isocalendar()[1]
    summary_dir = os.path.join(repo_root, "weekly-summary")
    os.makedirs(summary_dir, exist_ok=True)
    summary_file = os.path.join(summary_dir, f"{today.year}-W{week_number}-summary.md")
    
    with open(summary_file, "w", encoding="utf-8") as f:
        f.write("\n".join(summary_lines))
        
    print(f"✅ Weekly summary generated at weekly-summary/{os.path.basename(summary_file)}")

if __name__ == "__main__":
    main()
