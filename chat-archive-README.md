# 🏔️ Claude Code Chat Archiver

Archive and restore Claude Code terminal sessions with full context.

## Quick Start

### Archive Current Session
```bash
# Basic archive
python3 claude-chat-archiver.py --summary "Project Himalaya launch planning"

# Archive without terminal history
python3 claude-chat-archiver.py --summary "GitGuard development" --no-history
```

### List Archived Sessions
```bash
python3 claude-chat-archiver.py --action list
```

### Restore Session Context
```bash
python3 claude-chat-archiver.py --action restore --session-id claude_session_20250715_143022
```

## What Gets Archived

✅ **Chat Summary** - Manual description of session  
✅ **System Context** - Working directory, git status, environment  
✅ **Terminal History** - Recent commands (optional)  
✅ **Recent Files** - Files modified in last 24 hours  
✅ **Metadata** - Timestamps, session type  

## Archive Structure

```
ChatArchives/
├── claude_session_20250715_143022.json    # Full archive data
├── claude_session_20250715_143022.md      # Human-readable summary
└── claude_session_20250715_144530.json    # Next session...
```

## Session Restoration Workflow

1. **Archive current session** before closing
2. **Tomorrow**: List archived sessions
3. **Restore context** with session ID
4. **Start new Claude session** with restored context

## Example Usage

```bash
# End of today's work
python3 claude-chat-archiver.py --summary "Published Dev.to article, ready for social media launch"

# Tomorrow morning
python3 claude-chat-archiver.py --action list
python3 claude-chat-archiver.py --action restore --session-id claude_session_20250715_143022

# Start Claude and reference the restored context
claude-code
# Say: "Continue Project Himalaya from archived session - social media launch ready"
```

## Features

- 🔄 **Seamless restoration** - Full context preservation
- 📁 **Organized storage** - Chronological archive system  
- 📝 **Human-readable** - Markdown summaries for quick reference
- 🚀 **Fast workflow** - One command to archive, one to restore
- 🔍 **Context-rich** - Git status, environment, recent files

Perfect for maintaining continuity across Claude Code sessions! 🎯