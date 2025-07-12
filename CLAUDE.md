# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## 🚨 SESSION START ACKNOWLEDGMENT

**Upon reading this file, Claude Code MUST immediately display:**

```
🎯 Design Standard v2.1 in use
📍 Location: Docs/Standards/Design Standard v2.1.md
⚠️  MANDATORY compliance for ALL code development
```

**Note**: If a newer version exists in `Docs/Standards/`, update this acknowledgment to reflect the latest version.

## Project Overview

**AndyGoogle** is a digital library management system with web and mobile interfaces. The project follows "Design Standard v2.0" with a "Compatibility First, Consistency Second" philosophy for web development.

## Development Commands

### Server Management
```bash
# Start the web application (with smart port detection)
python StartAndyWeb.py

# Run environment checks only
python StartAndyWeb.py --check

# Show help and options
python StartAndyWeb.py --help

# Install dependencies
pip install -r requirements.txt
```

### Testing
```bash
# Run Python tests
pytest

# Run tests with coverage
pytest --cov=Source
```

### Database Operations
The application uses SQLite database with direct SQL queries (no SQLAlchemy). Database operations are handled through `Source/Core/DatabaseManager.py`.

## Architecture Overview

### Project Structure
```
/
├── Source/                    # Main application code
│   ├── API/                  # FastAPI backend
│   │   └── MainAPI.py       # Main API server
│   ├── Core/                # Business logic
│   │   └── DatabaseManager.py
│   └── Utils/               # Utility modules
├── WebPages/                # Frontend web application
│   ├── desktop-library.html # Main web interface
│   ├── mobile-library.html  # Mobile interface
│   ├── JS/                  # JavaScript modules
│   └── CSS/                 # Stylesheets
├── Data/                    # Application data
│   ├── Databases/           # SQLite database files
│   └── Thumbs/             # Book thumbnails
└── requirements.txt         # Python dependencies
```

### Technology Stack

**Backend:**
- **FastAPI** - REST API framework
- **SQLite** - Database with raw SQL queries
- **Python 3.8+** - Backend language
- **Uvicorn** - ASGI server

**Frontend:**
- **Vanilla JavaScript** - No framework dependencies
- **HTML5** - Semantic markup
- **CSS3** - Responsive styling
- **Bootstrap** (if used) - UI components

**Key Dependencies:**
- `fastapi` - Web framework
- `uvicorn` - ASGI server
- `sqlite3` - Database driver
- `pytest` - Testing framework

### Design Patterns

1. **API Layer**: RESTful endpoints in `/api/*` namespace
2. **Database Layer**: Raw SQL with PascalCase naming for all database elements
3. **Service Layer**: Business logic in `Source/Core/`
4. **Data Models**: Pydantic models for API validation
5. **Error Handling**: Centralized exception handling in FastAPI

### Database Schema

The database uses **PascalCase** naming for all elements per Design Standard v2.0:
- Tables: `Books`, `Categories`, `Subjects`
- Columns: `BookTitle`, `AuthorName`, `CategoryId`, `CreatedDate`
- Relationships: Foreign keys with PascalCase names

## 🚨 MANDATORY DESIGN STANDARDS COMPLIANCE

### Critical Requirement: Latest Design Standard

**BEFORE ANY CODE DEVELOPMENT**, you MUST:

1. **Verify the current Design Standard version shown in the session acknowledgment above**
2. **If acknowledgment shows outdated version**: Check `Docs/Standards/` directory for the highest version and update the acknowledgment
3. **Currently**: Design Standard v2.1 (AIDEV-PascalCase-2.1) 
4. **Location**: `Docs/Standards/Design Standard v2.1.md`
5. **Status**: MANDATORY for ALL code development - NO EXCEPTIONS

**⚠️ Always verify the latest version as standards may update to v2.2, v2.3, etc.**

**The session acknowledgment at the top of this file MUST be updated whenever a new Design Standard version is released.**

### Session Start Protocol - MANDATORY

**EVERY development session MUST begin with this acknowledgment:**

```
🚨 DESIGN STANDARD v2.1 COMPLIANCE ACKNOWLEDGED 🚨

I commit to the following NON-NEGOTIABLE requirements:
✅ Search project knowledge for current Design Standard BEFORE coding
✅ Use ACTUAL CURRENT TIME in ALL headers (never placeholder times)
✅ Update file paths to match ACTUAL deployment locations  
✅ Create unique timestamps for each file (no copy-paste headers)
✅ Verify header accuracy BEFORE functional changes
✅ Announce file path changes with explicit verification

VIOLATION OF THESE REQUIREMENTS = IMMEDIATE SESSION RESTART
```

### Design Standard v2.1 Core Principles

This project follows **Design Standard v2.1** with AI Accountability Framework:

1. **Backend Python**: Uses PascalCase for classes, methods, variables
2. **Frontend Web**: Uses ecosystem-required casing (kebab-case for CSS, camelCase for JavaScript)
3. **API Endpoints**: Follow REST conventions (lowercase, plural)
4. **Database**: PascalCase for all elements

### Mandatory Header Requirements - ZERO TOLERANCE

**ALL files MUST include Design Standard v2.1 compliant headers:**

```python
# File: [EXACT FILENAME WITH EXTENSION]
# Path: [EXACT DEPLOYMENT PATH - NO ASSUMPTIONS]
# Standard: AIDEV-PascalCase-2.1
# Created: YYYY-MM-DD
# Last Modified: YYYY-MM-DD  HH:MM[AM|PM]  ← MUST BE ACTUAL CURRENT TIME
"""
Description: [SPECIFIC PURPOSE - NO GENERIC DESCRIPTIONS]
[Additional context about functionality, dependencies, etc.]
"""
```

**Critical Header Validation Rules:**
1. **File Path Accuracy**: Path MUST match where file will actually be deployed/served
2. **Timestamp Authenticity**: Progressive timestamps showing actual creation sequence (NO copy-paste)
3. **Description Specificity**: Meaningful descriptions, not generic placeholders

**Pre-Code Verification Checklist:**
```
📋 HEADER VERIFICATION CHECKLIST:
□ Current date/time determined: [YYYY-MM-DD HH:MMPM]
□ Target file path confirmed: [Exact/Path/FileName.ext]
□ Deployment location verified: [Where will this actually be served/used?]
□ Header will match deployment reality: [Confirmed/Not Confirmed]
□ Unique timestamp will be used: [Not copied from previous files]

PROCEEDING WITH FILE CREATION/MODIFICATION
```

### Module Size Limits
- Maximum 300 lines per module
- Break larger modules into focused components
- Use clear, descriptive naming

## Development Workflow

### Smart Port Management
The startup script (`StartAndyWeb.py`) includes intelligent port detection:
- Tries ports 8000 → 8001 → 8002 → etc.
- Detects HP Printer conflicts (common on Linux)
- Provides helpful conflict resolution information

### API Endpoints
Main endpoints available:
- `GET /api/books` - Paginated book listing with search/filter
- `GET /api/books/{id}` - Individual book details
- `GET /api/books/{id}/thumbnail` - Book thumbnail image
- `GET /api/books/{id}/pdf` - Book PDF content
- `GET /api/categories` - Available categories
- `GET /api/subjects` - Available subjects (optionally filtered by category)
- `GET /api/stats` - Library statistics
- `GET /api/health` - System health check

### Database Access Patterns

**Always use DatabaseManager class:**
```python
from Core.DatabaseManager import DatabaseManager

DatabaseManager = DatabaseManager(DatabasePath)
if DatabaseManager.Connect():
    Books = DatabaseManager.GetBooksWithPagination(50, 0)
```

**Raw SQL with parameterized queries:**
```sql
SELECT B.BookTitle, C.CategoryName 
FROM Books B 
INNER JOIN Categories C ON B.CategoryId = C.Id 
WHERE B.BookTitle LIKE ?
```

## Testing Guidelines

- Use `pytest` for all Python tests
- Test files in `Tests/` directory with PascalCase naming
- Target 80%+ code coverage
- Test both unit and integration scenarios

## Important Notes

1. **Latest Design Standard MANDATORY** - Always check `Docs/Standards/` for newest version (currently v2.1)
2. **No SQLAlchemy** - Use raw SQL only per Design Standard v2.1
3. **PascalCase Database Elements** - All tables, columns, indexes use PascalCase
4. **Smart Port Detection** - Server automatically finds available ports
5. **Ecosystem Compatibility** - Frontend follows web standards, backend uses PascalCase
6. **Progressive Timestamps** - AI sessions must use actual current time in headers
7. **Zero Tolerance Compliance** - Header violations require immediate session restart
8. **Path Verification Required** - All file paths must match actual deployment locations

## Violation Consequences

**Immediate Session Restart Triggers:**
- Using placeholder timestamps (`HH:MM`, `XX:XX`)
- Identical timestamps across multiple files
- File path not matching deployment reality
- Skipping mandatory session acknowledgment
- Creating files without header verification checklist

**Three-Strike System:**
- **Strike 1**: Header inconsistency - Warning + immediate correction
- **Strike 2**: Repeated violation - Process review required
- **Strike 3**: Systematic failure - Session termination

## Contact & Support

- **Author**: Herb Bowers
- **Email**: HimalayaProject1@gmail.com
- **Project**: Project Himalaya