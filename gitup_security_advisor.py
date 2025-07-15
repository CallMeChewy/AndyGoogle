#!/usr/bin/env python3
# File: gitup_security_advisor.py
# Path: /home/herb/Desktop/AndyGoogle/gitup_security_advisor.py
# Standard: AIDEV-PascalCase-2.1
# Created: 2025-07-15
# Last Modified: 2025-07-15  04:22PM
"""
GitUp Security Advisor - Interactive security decision interface
Compares .gitignore vs proposed .gitupignore patterns and allows user decisions.
"""

import json
import os
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional
import subprocess

class GitUpSecurityAdvisor:
    def __init__(self, project_path: str = "."):
        self.project_path = Path(project_path).resolve()
        self.gitignore_path = self.project_path / ".gitignore"
        self.gitupignore_path = self.project_path / ".gitupignore"
        self.gitupignore_meta_path = self.project_path / ".gitupignore.meta"
        
        # Current security issues from GitGuard
        self.current_issues = []
        self.load_current_issues()
        
    def load_current_issues(self):
        """Load current security issues from GitGuard scan"""
        try:
            result = subprocess.run(
                ['gitguard', 'scan', '--path', str(self.project_path), '--full', '--format', 'json'],
                capture_output=True,
                text=True,
                timeout=60
            )
            
            if result.returncode == 0:
                scan_data = json.loads(result.stdout)
                self.current_issues = scan_data.get('issues', [])
            else:
                # Try to parse JSON from stderr if that's where it went
                try:
                    scan_data = json.loads(result.stderr)
                    self.current_issues = scan_data.get('issues', [])
                except:
                    print(f"Warning: GitGuard scan failed: {result.stderr}")
                
        except Exception as e:
            print(f"Warning: Could not load GitGuard scan: {e}")
    
    def analyze_gitignore_coverage(self) -> Dict:
        """Analyze what's covered by .gitignore vs what should be in .gitupignore"""
        
        # Read current .gitignore
        gitignore_patterns = []
        if self.gitignore_path.exists():
            with open(self.gitignore_path, 'r') as f:
                gitignore_patterns = [line.strip() for line in f.readlines() 
                                    if line.strip() and not line.startswith('#')]
        
        # Read current .gitupignore
        gitupignore_patterns = []
        if self.gitupignore_path.exists():
            with open(self.gitupignore_path, 'r') as f:
                gitupignore_patterns = [line.strip() for line in f.readlines() 
                                      if line.strip() and not line.startswith('#')]
        
        # Analyze current security issues
        analysis = {
            'timestamp': datetime.now().isoformat(),
            'gitignore_patterns': gitignore_patterns,
            'gitupignore_patterns': gitupignore_patterns,
            'current_issues': self.current_issues,
            'recommendations': []
        }
        
        # Generate recommendations for each issue
        for issue in self.current_issues:
            file_path = issue['file_path']
            
            # Check if already covered by .gitignore
            is_gitignore_covered = self._is_covered_by_patterns(file_path, gitignore_patterns)
            is_gitupignore_covered = self._is_covered_by_patterns(file_path, gitupignore_patterns)
            
            recommendation = {
                'issue': issue,
                'file_path': file_path,
                'severity': issue['severity'],
                'category': issue['category'],
                'description': issue['description'],
                'is_gitignore_covered': is_gitignore_covered,
                'is_gitupignore_covered': is_gitupignore_covered,
                'recommended_action': self._get_recommended_action(issue, is_gitignore_covered, is_gitupignore_covered),
                'proposed_pattern': self._generate_pattern_for_file(file_path)
            }
            
            analysis['recommendations'].append(recommendation)
        
        return analysis
    
    def _is_covered_by_patterns(self, file_path: str, patterns: List[str]) -> bool:
        """Check if file is covered by any of the given patterns"""
        import fnmatch
        
        for pattern in patterns:
            if fnmatch.fnmatch(file_path, pattern):
                return True
            if fnmatch.fnmatch(file_path, f"*/{pattern}"):
                return True
            if pattern.endswith('/') and file_path.startswith(pattern):
                return True
        
        return False
    
    def _get_recommended_action(self, issue: Dict, is_gitignore_covered: bool, is_gitupignore_covered: bool) -> str:
        """Get recommended action for an issue"""
        if is_gitignore_covered and is_gitupignore_covered:
            return "already_handled"
        elif is_gitignore_covered:
            return "add_to_gitupignore"
        elif is_gitupignore_covered:
            return "add_to_gitignore"
        else:
            if issue['severity'] == 'CRITICAL':
                return "add_to_gitignore"
            else:
                return "add_to_gitupignore"
    
    def _generate_pattern_for_file(self, file_path: str) -> str:
        """Generate appropriate ignore pattern for a file"""
        # For specific files, use exact path
        if file_path.endswith('.db'):
            return file_path
        elif file_path.endswith('.json') and ('config' in file_path or 'secret' in file_path):
            return file_path
        elif 'Cache' in file_path or 'cache' in file_path:
            return f"{os.path.dirname(file_path)}/"
        else:
            return file_path
    
    def generate_diff_report(self) -> str:
        """Generate a diff report showing .gitignore vs proposed .gitupignore"""
        analysis = self.analyze_gitignore_coverage()
        
        report = []
        report.append("=" * 80)
        report.append("🔒 GITUP SECURITY ADVISOR - DIFF REPORT")
        report.append("=" * 80)
        report.append(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        report.append(f"Project: {self.project_path}")
        report.append(f"Total Issues: {len(analysis['current_issues'])}")
        report.append("")
        
        # Summary
        report.append("📊 SUMMARY")
        report.append("-" * 40)
        
        action_counts = {}
        for rec in analysis['recommendations']:
            action = rec['recommended_action']
            action_counts[action] = action_counts.get(action, 0) + 1
        
        for action, count in action_counts.items():
            report.append(f"  {action.replace('_', ' ').title()}: {count}")
        
        report.append("")
        
        # Detailed recommendations
        report.append("🎯 DETAILED RECOMMENDATIONS")
        report.append("-" * 40)
        
        for i, rec in enumerate(analysis['recommendations'], 1):
            report.append(f"")
            report.append(f"[{i}] {rec['severity']} - {rec['file_path']}")
            report.append(f"    Category: {rec['category']}")
            report.append(f"    Description: {rec['description']}")
            report.append(f"    .gitignore covered: {'✅' if rec['is_gitignore_covered'] else '❌'}")
            report.append(f"    .gitupignore covered: {'✅' if rec['is_gitupignore_covered'] else '❌'}")
            report.append(f"    Recommended action: {rec['recommended_action'].replace('_', ' ').title()}")
            report.append(f"    Proposed pattern: {rec['proposed_pattern']}")
        
        report.append("")
        report.append("📋 USER DECISION MATRIX")
        report.append("-" * 40)
        report.append("For each issue above, you can choose:")
        report.append("  [A] Accept - Add to .gitignore (permanent ignore)")
        report.append("  [G] GitUp - Add to .gitupignore (security-aware ignore)")
        report.append("  [I] Ignore - Don't add to either (keep flagging)")
        report.append("  [R] Resolve - Fix the issue instead of ignoring")
        report.append("")
        
        return "\n".join(report)
    
    def prompt_user_decisions(self) -> Dict:
        """Prompt user for decisions on each security issue"""
        analysis = self.analyze_gitignore_coverage()
        decisions = {
            'timestamp': datetime.now().isoformat(),
            'user_decisions': [],
            'audit_trail': []
        }
        
        print(self.generate_diff_report())
        print("\n" + "=" * 80)
        print("🎯 INTERACTIVE DECISION PROCESS")
        print("=" * 80)
        
        for i, rec in enumerate(analysis['recommendations'], 1):
            print(f"\n[{i}/{len(analysis['recommendations'])}] {rec['severity']} - {rec['file_path']}")
            print(f"    {rec['description']}")
            print(f"    Recommended: {rec['recommended_action'].replace('_', ' ').title()}")
            
            while True:
                choice = input("\n    Your decision [A]ccept/[G]itUp/[I]gnore/[R]esolve: ").strip().upper()
                
                if choice in ['A', 'G', 'I', 'R']:
                    decision = {
                        'issue_id': i,
                        'file_path': rec['file_path'],
                        'severity': rec['severity'],
                        'user_choice': choice,
                        'user_choice_full': {
                            'A': 'accept_to_gitignore',
                            'G': 'add_to_gitupignore',
                            'I': 'ignore_keep_flagging',
                            'R': 'resolve_issue'
                        }[choice],
                        'recommended_action': rec['recommended_action'],
                        'proposed_pattern': rec['proposed_pattern'],
                        'timestamp': datetime.now().isoformat()
                    }
                    
                    # Ask for reason if not following recommendation
                    if (choice == 'A' and rec['recommended_action'] != 'add_to_gitignore') or \
                       (choice == 'G' and rec['recommended_action'] != 'add_to_gitupignore'):
                        reason = input("    Reason for different choice: ").strip()
                        decision['user_reason'] = reason
                    
                    decisions['user_decisions'].append(decision)
                    break
                else:
                    print("    Invalid choice. Please enter A, G, I, or R.")
        
        return decisions
    
    def apply_user_decisions(self, decisions: Dict):
        """Apply user decisions to .gitignore and .gitupignore files"""
        
        # Load existing patterns
        gitignore_patterns = []
        if self.gitignore_path.exists():
            with open(self.gitignore_path, 'r') as f:
                gitignore_patterns = f.readlines()
        
        gitupignore_patterns = []
        if self.gitupignore_path.exists():
            with open(self.gitupignore_path, 'r') as f:
                gitupignore_patterns = f.readlines()
        
        # Apply decisions
        gitignore_additions = []
        gitupignore_additions = []
        
        for decision in decisions['user_decisions']:
            if decision['user_choice'] == 'A':  # Accept to .gitignore
                pattern = decision['proposed_pattern']
                if pattern not in [p.strip() for p in gitignore_patterns]:
                    gitignore_additions.append(f"# GitUp Security: {decision['file_path']} - {decision['severity']}\n")
                    gitignore_additions.append(f"{pattern}\n")
            
            elif decision['user_choice'] == 'G':  # Add to .gitupignore
                pattern = decision['proposed_pattern']
                if pattern not in [p.strip() for p in gitupignore_patterns]:
                    gitupignore_additions.append(f"# Security Exception: {decision['file_path']} - {decision['severity']}\n")
                    gitupignore_additions.append(f"{pattern}\n")
        
        # Write updated .gitignore
        if gitignore_additions:
            with open(self.gitignore_path, 'a') as f:
                f.write("\n# GitUp Security Additions\n")
                f.write(f"# Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
                f.writelines(gitignore_additions)
        
        # Write updated .gitupignore
        if gitupignore_additions:
            with open(self.gitupignore_path, 'a') as f:
                f.write("\n# GitUp Security Exceptions\n")
                f.write(f"# Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
                f.writelines(gitupignore_additions)
        
        # Write audit metadata
        self.save_audit_metadata(decisions)
        
        print(f"\n✅ Applied {len(gitignore_additions)} additions to .gitignore")
        print(f"✅ Applied {len(gitupignore_additions)} additions to .gitupignore")
        print(f"📋 Audit trail saved to {self.gitupignore_meta_path}")
    
    def save_audit_metadata(self, decisions: Dict):
        """Save audit metadata to .gitupignore.meta"""
        
        # Load existing metadata
        existing_meta = {}
        if self.gitupignore_meta_path.exists():
            try:
                with open(self.gitupignore_meta_path, 'r') as f:
                    existing_meta = json.load(f)
            except:
                existing_meta = {}
        
        # Add new session
        session_id = datetime.now().strftime('%Y%m%d_%H%M%S')
        existing_meta[session_id] = {
            'timestamp': decisions['timestamp'],
            'project_path': str(self.project_path),
            'total_issues': len(decisions['user_decisions']),
            'decisions': decisions['user_decisions'],
            'summary': {
                'accept_to_gitignore': len([d for d in decisions['user_decisions'] if d['user_choice'] == 'A']),
                'add_to_gitupignore': len([d for d in decisions['user_decisions'] if d['user_choice'] == 'G']),
                'ignore_keep_flagging': len([d for d in decisions['user_decisions'] if d['user_choice'] == 'I']),
                'resolve_issue': len([d for d in decisions['user_decisions'] if d['user_choice'] == 'R'])
            }
        }
        
        # Save metadata
        with open(self.gitupignore_meta_path, 'w') as f:
            json.dump(existing_meta, f, indent=2)
    
    def show_audit_history(self):
        """Show audit history from .gitupignore.meta"""
        if not self.gitupignore_meta_path.exists():
            print("No audit history found.")
            return
        
        try:
            with open(self.gitupignore_meta_path, 'r') as f:
                metadata = json.load(f)
            
            print("=" * 60)
            print("📋 GITUP SECURITY AUDIT HISTORY")
            print("=" * 60)
            
            for session_id, session_data in metadata.items():
                print(f"\nSession: {session_id}")
                print(f"  Timestamp: {session_data['timestamp']}")
                print(f"  Total Issues: {session_data['total_issues']}")
                print(f"  Summary:")
                for action, count in session_data['summary'].items():
                    if count > 0:
                        print(f"    {action.replace('_', ' ').title()}: {count}")
                        
        except Exception as e:
            print(f"Error reading audit history: {e}")

def main():
    """Main CLI interface"""
    advisor = GitUpSecurityAdvisor()
    
    print("🔒 GitUp Security Advisor")
    print("=" * 40)
    print("1. Generate diff report")
    print("2. Interactive decision process")
    print("3. Show audit history")
    print("4. Exit")
    
    while True:
        choice = input("\nChoose option (1-4): ").strip()
        
        if choice == '1':
            print("\n" + advisor.generate_diff_report())
        elif choice == '2':
            decisions = advisor.prompt_user_decisions()
            advisor.apply_user_decisions(decisions)
        elif choice == '3':
            advisor.show_audit_history()
        elif choice == '4':
            print("Goodbye!")
            break
        else:
            print("Invalid choice. Please enter 1, 2, 3, or 4.")

if __name__ == "__main__":
    main()