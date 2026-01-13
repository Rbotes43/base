#!/usr/bin/env python
"""
ASA Compliance Checker - Command Line Version
Usage: python cli_checker.py
"""

from asa_compliance import ASAComplianceChecker
import sys


def print_separator(char="=", length=70):
    print(char * length)


def print_results(results):
    """Display compliance check results"""
    print_separator()
    print(f"OVERALL RISK: {results['overall_risk']}")
    print_separator()
    print(f"\nTotal Issues: {results['total_issues']}")
    print(f"  • High Risk: {len(results['high_risk_issues'])}")
    print(f"  • Medium Risk: {len(results['medium_risk_issues'])}")
    print(f"  • Low Risk: {len(results['low_risk_issues'])}")
    print(f"\n{results['summary']}\n")

    # High Risk Issues
    if results['high_risk_issues']:
        print_separator("-")
        print("⚠️  HIGH RISK ISSUES")
        print_separator("-")
        for i, issue in enumerate(results['high_risk_issues'], 1):
            print(f"\n{i}. {issue['category']}")
            print(f"   Description: {issue['description']}")
            print(f"   ASA Rule: {issue['asa_rule']}")
            if issue['location']:
                print(f"   Location: {issue['location']}")
            if issue['suggestion']:
                print(f"   💡 Suggestion: {issue['suggestion']}")

    # Medium Risk Issues
    if results['medium_risk_issues']:
        print_separator("-")
        print("⚡ MEDIUM RISK ISSUES")
        print_separator("-")
        for i, issue in enumerate(results['medium_risk_issues'], 1):
            print(f"\n{i}. {issue['category']}")
            print(f"   Description: {issue['description']}")
            print(f"   ASA Rule: {issue['asa_rule']}")
            if issue['location']:
                print(f"   Location: {issue['location']}")
            if issue['suggestion']:
                print(f"   💡 Suggestion: {issue['suggestion']}")

    # Low Risk Issues
    if results['low_risk_issues']:
        print_separator("-")
        print("ℹ️  LOW RISK ISSUES")
        print_separator("-")
        for i, issue in enumerate(results['low_risk_issues'], 1):
            print(f"\n{i}. {issue['category']}")
            print(f"   Description: {issue['description']}")
            print(f"   ASA Rule: {issue['asa_rule']}")
            if issue['location']:
                print(f"   Location: {issue['location']}")
            if issue['suggestion']:
                print(f"   💡 Suggestion: {issue['suggestion']}")

    # Suggestions
    if results['suggestions']['revised_content']:
        print_separator("-")
        print("📝 SUGGESTED COMPLIANT VERSION")
        print_separator("-")
        print(results['suggestions']['revised_content'])

    print_separator()


def main():
    print_separator("=")
    print("🇬🇧  ASA COMPLIANCE CHECKER - COMMAND LINE TOOL")
    print_separator("=")
    print("\nThis tool checks advertising content against UK ASA Code requirements.")
    print("It identifies compliance issues and provides suggestions.\n")

    checker = ASAComplianceChecker()

    while True:
        print_separator("-")
        print("OPTIONS:")
        print("  1. Check text content")
        print("  2. View example")
        print("  3. Exit")
        print_separator("-")

        choice = input("\nEnter your choice (1-3): ").strip()

        if choice == "1":
            print("\nEnter your advertising content (press Enter twice when done):")
            lines = []
            while True:
                line = input()
                if line == "" and (not lines or lines[-1] == ""):
                    break
                lines.append(line)

            content = "\n".join(lines).strip()

            if not content:
                print("\n⚠️  No content provided. Please try again.\n")
                continue

            print("\n🔍 Analyzing content...\n")
            results = checker.check_content(content)
            print_results(results)

        elif choice == "2":
            print("\n📋 Example High-Risk Content:\n")
            example = """Lose 10kg in just 2 weeks with our miracle weight loss pill!
100% guaranteed results. Clinically proven formula that cures obesity.
Free trial - limited time only! Rated #1 by doctors."""

            print(example)
            print("\n🔍 Analyzing example...\n")
            results = checker.check_content(example)
            print_results(results)

        elif choice == "3":
            print("\n👋 Thank you for using ASA Compliance Checker!\n")
            sys.exit(0)

        else:
            print("\n⚠️  Invalid choice. Please enter 1, 2, or 3.\n")

        input("\nPress Enter to continue...")
        print("\n" * 2)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n👋 Goodbye!\n")
        sys.exit(0)
