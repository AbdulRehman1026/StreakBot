import os
import pytz
import datetime
from git import Repo
from dotenv import load_dotenv

# Load variables from .env file
load_dotenv()

# Environment variables
GITHUB_USERNAME = os.getenv("GITHUB_USERNAME")
GITHUB_EMAIL = os.getenv("GITHUB_EMAIL")
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
REPO_PATH = os.getenv("REPO_PATH", ".")
PUSH_HOUR = int(os.getenv("PUSH_TIME", 23))  # Default to 11 PM

# Define Pakistan timezone
pakistan_tz = pytz.timezone("Asia/Karachi")
now = datetime.datetime.now(pakistan_tz)

def should_push(now):
    return now.hour == PUSH_HOUR and now.minute == 0

def format_date(now):
    return now.strftime("%d/%B/%Y")  # Example: 21/July/2025

def make_commit():
    repo = Repo(REPO_PATH)
    repo.config_writer().set_value("user", "email", GITHUB_EMAIL).release()
    repo.config_writer().set_value("user", "name", GITHUB_USERNAME).release()

    streak_file_path = os.path.join(REPO_PATH, "streak.txt")
    
    # Prepare the line to add
    line = f"Default push by the StreakBot at 11 pm, on {format_date(now)}\n"
    
    # Append the line
    with open(streak_file_path, "a") as f:
        f.write(line)
    
    # Git operations
    repo.git.add("streak.txt")
    repo.index.commit(f"StreakBot push for {format_date(now)}")
    origin = repo.remote(name="origin")
    origin.push()
    print(f"[+] Commit pushed for {format_date(now)}.")

if should_push(now):
    print(f"[✓] It's {PUSH_HOUR}:00 PKT — running push...")
    make_commit()
else:
    print(f"[-] Not push time yet — current time is {now.strftime('%H:%M')} PKT")
