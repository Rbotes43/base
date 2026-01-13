"""
Simple test script to verify ASA compliance checker functionality
"""

from asa_compliance import ASAComplianceChecker

def test_high_risk_content():
    """Test high-risk advertising content"""
    print("=" * 60)
    print("TEST 1: High-Risk Advertising Content")
    print("=" * 60)

    content = """
    Miracle cure for diabetes! 100% guaranteed to reverse your
    condition in 30 days. Clinically proven. Free bottle today!
    Rated #1 by doctors. Lose 10kg in 2 weeks guaranteed!
    """

    checker = ASAComplianceChecker()
    results = checker.check_content(content)

    print(f"\nContent: {content.strip()}\n")
    print(f"Overall Risk: {results['overall_risk']}")
    print(f"Total Issues: {results['total_issues']}")
    print(f"High Risk: {len(results['high_risk_issues'])}")
    print(f"Medium Risk: {len(results['medium_risk_issues'])}")
    print(f"Low Risk: {len(results['low_risk_issues'])}")
    print(f"\nSummary: {results['summary']}")

    if results['high_risk_issues']:
        print("\nHigh Risk Issues:")
        for issue in results['high_risk_issues']:
            print(f"  - {issue['description']}")
            print(f"    Rule: {issue['asa_rule']}")
            print(f"    Suggestion: {issue['suggestion']}\n")

def test_compliant_content():
    """Test compliant advertising content"""
    print("\n" + "=" * 60)
    print("TEST 2: Compliant Advertising Content")
    print("=" * 60)

    content = """
    Our weight management supplement is designed to support your
    health goals when used as part of a balanced diet and exercise
    program. Results may vary. Contains natural ingredients.
    Money-back guarantee available - see terms and conditions.
    """

    checker = ASAComplianceChecker()
    results = checker.check_content(content)

    print(f"\nContent: {content.strip()}\n")
    print(f"Overall Risk: {results['overall_risk']}")
    print(f"Total Issues: {results['total_issues']}")
    print(f"High Risk: {len(results['high_risk_issues'])}")
    print(f"Medium Risk: {len(results['medium_risk_issues'])}")
    print(f"Low Risk: {len(results['low_risk_issues'])}")
    print(f"\nSummary: {results['summary']}")

def test_medium_risk_content():
    """Test medium-risk advertising content"""
    print("\n" + "=" * 60)
    print("TEST 3: Medium-Risk Advertising Content")
    print("=" * 60)

    content = """
    Our eco-friendly product is clinically proven to work in 7 days.
    Recommended by doctors. Natural and organic formula.
    50% off - was £100, now £50!
    """

    checker = ASAComplianceChecker()
    results = checker.check_content(content)

    print(f"\nContent: {content.strip()}\n")
    print(f"Overall Risk: {results['overall_risk']}")
    print(f"Total Issues: {results['total_issues']}")
    print(f"High Risk: {len(results['high_risk_issues'])}")
    print(f"Medium Risk: {len(results['medium_risk_issues'])}")
    print(f"Low Risk: {len(results['low_risk_issues'])}")
    print(f"\nSummary: {results['summary']}")

    if results['medium_risk_issues']:
        print("\nMedium Risk Issues:")
        for issue in results['medium_risk_issues']:
            print(f"  - {issue['description']}")

if __name__ == '__main__':
    print("\n🇬🇧 ASA COMPLIANCE CHECKER - TEST SUITE\n")

    try:
        test_high_risk_content()
        test_compliant_content()
        test_medium_risk_content()

        print("\n" + "=" * 60)
        print("✅ ALL TESTS COMPLETED SUCCESSFULLY")
        print("=" * 60 + "\n")

    except Exception as e:
        print(f"\n❌ TEST FAILED: {e}\n")
        raise
