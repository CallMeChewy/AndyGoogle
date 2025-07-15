#!/usr/bin/env python3
"""Test script to demonstrate the GitUp Security Advisor"""

from gitup_security_advisor import GitUpSecurityAdvisor

def main():
    advisor = GitUpSecurityAdvisor()
    
    print("🔒 GitUp Security Advisor - Diff Report")
    print("=" * 80)
    
    # Generate and display the diff report
    diff_report = advisor.generate_diff_report()
    print(diff_report)
    
    print("\n" + "=" * 80)
    print("📋 CURRENT GITIGNORE VS PROPOSED GITUPIGNORE")
    print("=" * 80)
    
    # Show analysis details
    analysis = advisor.analyze_gitignore_coverage()
    
    print(f"\nCurrent .gitignore patterns: {len(analysis['gitignore_patterns'])}")
    print(f"Current .gitupignore patterns: {len(analysis['gitupignore_patterns'])}")
    print(f"Security issues found: {len(analysis['current_issues'])}")
    print(f"Recommendations generated: {len(analysis['recommendations'])}")
    
    print("\n📊 BREAKDOWN BY RECOMMENDATION:")
    action_counts = {}
    for rec in analysis['recommendations']:
        action = rec['recommended_action']
        action_counts[action] = action_counts.get(action, 0) + 1
    
    for action, count in action_counts.items():
        print(f"  {action.replace('_', ' ').title()}: {count}")
    
    print("\n📋 DETAILED ISSUE ANALYSIS:")
    for i, rec in enumerate(analysis['recommendations'], 1):
        print(f"\n[{i}] {rec['severity']} - {rec['file_path']}")
        print(f"    Description: {rec['description']}")
        print(f"    .gitignore covers: {'✅' if rec['is_gitignore_covered'] else '❌'}")
        print(f"    .gitupignore covers: {'✅' if rec['is_gitupignore_covered'] else '❌'}")
        print(f"    Recommended: {rec['recommended_action'].replace('_', ' ').title()}")
        print(f"    Proposed pattern: {rec['proposed_pattern']}")

if __name__ == "__main__":
    main()