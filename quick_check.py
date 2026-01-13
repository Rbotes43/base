#!/usr/bin/env python
"""
Quick ASA Compliance Check
Usage: python quick_check.py "Your advertising text here"
"""

import sys
from asa_compliance import ASAComplianceChecker


def print_separator(char="=", length=70):
    print(char * length)


def main():
    if len(sys.argv) < 2:
        print("Usage: python quick_check.py \"Your advertising text here\"")
        print("\nOr run without arguments to use default example:")

        content = """Get glowing skin in 24 hours! Our miracle cream is 100% effective.
Guaranteed results or your money back. Clinically proven by doctors.
Free trial - limited offer!"""

        print("\nUsing example content:")
        print("-" * 70)
        print(content)
        print("-" * 70)
    else:
        content = " ".join(sys.argv[1:])
        print_separator()
        print("🇬🇧  ASA COMPLIANCE CHECK")
        print_separator()
        print("\nContent to check:")
        print("-" * 70)
        print(content)
        print("-" * 70)

    print("\n🔍 Analyzing...\n")

    checker = ASAComplianceChecker()
    results = checker.check_content(content)

    print_separator()
    print(f"OVERALL RISK: {results['overall_risk']}")
    print_separator()
    print(f"\nTotal Issues: {results['total_issues']}")
    print(f"  • High Risk: {len(results['high_risk_issues'])}")
    print(f"  • Medium Risk: {len(results['medium_risk_issues'])}")
    print(f"  • Low Risk: {len(results['low_risk_issues'])}")

    if results['high_risk_issues']:
        print("\n" + "-" * 70)
        print("⚠️  HIGH RISK ISSUES:")
        print("-" * 70)
        for i, issue in enumerate(results['high_risk_issues'], 1):
            print(f"\n{i}. {issue['category']}")
            print(f"   {issue['description']}")
            print(f"   💡 {issue['suggestion']}")

    if results['medium_risk_issues']:
        print("\n" + "-" * 70)
        print("⚡ MEDIUM RISK ISSUES:")
        print("-" * 70)
        for i, issue in enumerate(results['medium_risk_issues'], 1):
            print(f"\n{i}. {issue['category']}")
            print(f"   {issue['description']}")

    if results['low_risk_issues']:
        print("\n" + "-" * 70)
        print("ℹ️  LOW RISK ISSUES:")
        print("-" * 70)
        for i, issue in enumerate(results['low_risk_issues'], 1):
            print(f"\n{i}. {issue['category']}")
            print(f"   {issue['description']}")

    print("\n" + "=" * 70)
    print("✅ Analysis complete!")
    print("=" * 70)
    print()


if __name__ == "__main__":
    main()
