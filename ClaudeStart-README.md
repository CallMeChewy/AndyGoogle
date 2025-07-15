# 🚀 ClaudeStart - Smart Session Manager

One-command solution for Claude Code session management with automatic archiving and context restoration.

## Quick Usage

```bash
# Smart start (archive current + restore context + launch Claude)
./ClaudeStart

# Start fresh session
./ClaudeStart --new

# Archive current session only
./ClaudeStart --archive-only

# List all sessions
./ClaudeStart --list

# Restore specific session and launch
./ClaudeStart --restore claude_session_20250715_143022
```

## What ClaudeStart Does

### 🔄 **Smart Workflow**
1. **Detects active session** - Checks if meaningful work exists
2. **Prompts for archiving** - Saves current progress with summary
3. **Shows available sessions** - Lists recent work for context
4. **Launches Claude** - Starts with restoration guidance

### 📦 **Automatic Archiving**
- Prompts for session summary
- Auto-generates description if skipped
- Preserves full context (git status, files, environment)
- Creates human-readable markdown summary

### 🎯 **Context Restoration**
- Shows recent sessions for reference
- Provides restoration commands
- Gives Claude startup guidance
- Maintains project continuity

## Interactive Experience

```bash
$ ./ClaudeStart

🏔️  ClaudeStart - Project Himalaya Session Manager
==================================================
🤔 Detected active session. Archive before starting new Claude session?
  [y] Yes, archive current work
  [n] No, start fresh  
  [s] Skip and show recent sessions only
Choice [y/n/s]: y

📦 Archiving current session...
📝 Enter session summary (or press Enter for auto-generated):
> Project Himalaya launch: social media campaign ready

✅ Session archived successfully

📋 Recent Claude sessions:
  • claude_session_20250715_143022
  • claude_session_20250715_120815
  • claude_session_20250714_165432

🚀 Starting Claude Code...

💡 Context restoration tip:
When Claude starts, say:
"Continue from previous session - Project Himalaya social media launch"

🏔️ Project Himalaya workflow ready!
```

## Installation

```bash
# Make executable (already done)
chmod +x ClaudeStart

# Optional: Add to PATH for global access
echo 'export PATH="$PATH:/home/herb/Desktop/AndyGoogle"' >> ~/.bashrc
source ~/.bashrc

# Then use from anywhere:
ClaudeStart
```

## Features

✅ **Prevents work loss** - Never forget to archive sessions  
✅ **Smart detection** - Only archives when meaningful work exists  
✅ **Flexible options** - Handle any workflow scenario  
✅ **Context guidance** - Clear instructions for Claude restoration  
✅ **Color-coded output** - Easy to read and understand  
✅ **Error handling** - Graceful fallbacks and helpful messages  

## Perfect for Project Himalaya

ClaudeStart eliminates the "human forgetfulness" problem:
- **End of day**: `./ClaudeStart --archive-only`
- **Next morning**: `./ClaudeStart` (auto-restores context)
- **Emergency archive**: Always prompts before potentially losing work

Never lose Project Himalaya momentum again! 🏔️