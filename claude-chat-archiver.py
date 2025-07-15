#!/usr/bin/env python3
"""
Claude Code Chat Archiver
Archives Claude Code terminal sessions with context and metadata
"""

import os
import datetime
import json
import subprocess
import argparse
from pathlib import Path

class ClaudeChatArchiver:
    def __init__(self, archive_dir="/home/herb/Desktop/AndyGoogle/ChatArchives"):
        self.archive_dir = Path(archive_dir)
        self.archive_dir.mkdir(exist_ok=True)
        self.session_date = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        
    def capture_terminal_session(self):
        """Capture current terminal session history"""
        try:
            # Get bash history
            history_cmd = subprocess.run(['history'], 
                                       shell=True, 
                                       capture_output=True, 
                                       text=True)
            return history_cmd.stdout
        except Exception as e:
            return f"Error capturing history: {str(e)}"
    
    def capture_current_context(self):
        """Capture current working directory and git status"""
        context = {
            "timestamp": datetime.datetime.now().isoformat(),
            "working_directory": os.getcwd(),
            "git_status": self.get_git_status(),
            "environment": dict(os.environ),
            "recent_files": self.get_recent_files()
        }
        return context
    
    def get_git_status(self):
        """Get git repository status if available"""
        try:
            result = subprocess.run(['git', 'status', '--porcelain'], 
                                  capture_output=True, text=True)
            return result.stdout
        except:
            return "Not a git repository"
    
    def get_recent_files(self):
        """Get recently modified files in current directory"""
        try:
            result = subprocess.run(['find', '.', '-type', 'f', '-mtime', '-1'], 
                                  capture_output=True, text=True)
            return result.stdout.split('\n')[:20]  # Last 20 files
        except:
            return []
    
    def create_chat_summary(self, summary_text=""):
        """Create manual chat summary"""
        return {
            "session_id": f"claude_session_{self.session_date}",
            "summary": summary_text,
            "key_accomplishments": [],
            "next_actions": [],
            "important_files": [],
            "context_notes": ""
        }
    
    def archive_session(self, summary_text="", include_history=True):
        """Archive complete session with all context"""
        
        # Create session archive
        archive_data = {
            "metadata": {
                "session_date": self.session_date,
                "archive_time": datetime.datetime.now().isoformat(),
                "session_type": "claude_code_cli"
            },
            "chat_summary": self.create_chat_summary(summary_text),
            "system_context": self.capture_current_context()
        }
        
        if include_history:
            archive_data["terminal_history"] = self.capture_terminal_session()
        
        # Save archive file
        archive_file = self.archive_dir / f"claude_session_{self.session_date}.json"
        with open(archive_file, 'w') as f:
            json.dump(archive_data, f, indent=2)
        
        # Create human-readable summary
        self.create_readable_summary(archive_data, archive_file)
        
        return archive_file
    
    def create_readable_summary(self, archive_data, archive_file):
        """Create human-readable session summary"""
        summary_file = archive_file.with_suffix('.md')
        
        content = f"""# Claude Code Session Archive
        
## Session: {archive_data['metadata']['session_date']}
**Archived:** {archive_data['metadata']['archive_time']}

## Chat Summary
{archive_data['chat_summary']['summary']}

## System Context
- **Working Directory:** {archive_data['system_context']['working_directory']}
- **Git Status:** 
```
{archive_data['system_context']['git_status']}
```

## Recent Files
{chr(10).join(f"- {f}" for f in archive_data['system_context']['recent_files'][:10])}

## Restoration Commands
```bash
# Navigate to working directory
cd {archive_data['system_context']['working_directory']}

# Start new Claude session with context
claude-code

# Restore context by saying:
"Continue from archived session {archive_data['metadata']['session_date']}"
```

## Archive Files
- **Full Archive:** {archive_file.name}
- **Summary:** {summary_file.name}
"""
        
        with open(summary_file, 'w') as f:
            f.write(content)
    
    def list_archived_sessions(self):
        """List all archived sessions"""
        archives = list(self.archive_dir.glob("claude_session_*.json"))
        
        print(f"📁 Found {len(archives)} archived sessions:")
        for archive in sorted(archives, reverse=True):
            print(f"  • {archive.stem}")
        
        return archives
    
    def restore_session_context(self, session_id):
        """Load and display session context for restoration"""
        archive_file = self.archive_dir / f"{session_id}.json"
        
        if not archive_file.exists():
            print(f"❌ Session {session_id} not found")
            return None
        
        with open(archive_file, 'r') as f:
            archive_data = json.load(f)
        
        print(f"🔄 Restoring context for session: {session_id}")
        print(f"📅 Original date: {archive_data['metadata']['session_date']}")
        print(f"📁 Working directory: {archive_data['system_context']['working_directory']}")
        print(f"📝 Summary: {archive_data['chat_summary']['summary']}")
        
        return archive_data

def main():
    parser = argparse.ArgumentParser(description='Archive Claude Code chat sessions')
    parser.add_argument('--action', choices=['archive', 'list', 'restore'], 
                       default='archive', help='Action to perform')
    parser.add_argument('--summary', type=str, default='', 
                       help='Session summary text')
    parser.add_argument('--session-id', type=str, 
                       help='Session ID for restoration')
    parser.add_argument('--no-history', action='store_true', 
                       help='Skip terminal history capture')
    
    args = parser.parse_args()
    
    archiver = ClaudeChatArchiver()
    
    if args.action == 'archive':
        print("🏔️ Archiving Claude Code session...")
        archive_file = archiver.archive_session(
            summary_text=args.summary,
            include_history=not args.no_history
        )
        print(f"✅ Session archived: {archive_file}")
        
    elif args.action == 'list':
        archiver.list_archived_sessions()
        
    elif args.action == 'restore':
        if not args.session_id:
            print("❌ Please provide --session-id for restoration")
            return
        archiver.restore_session_context(args.session_id)

if __name__ == "__main__":
    main()