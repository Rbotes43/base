"""
ASA Compliance Checker
Checks advertising content against UK ASA Code principles
"""

import re
from typing import Dict, List, Tuple
from dataclasses import dataclass, field


@dataclass
class ComplianceIssue:
    """Represents a compliance issue found in advertising content"""
    risk_level: str  # 'high', 'medium', 'low'
    category: str
    description: str
    asa_rule: str
    location: str = ""
    suggestion: str = ""


class ASAComplianceChecker:
    """
    Checks advertising content against UK ASA Code principles
    """

    def __init__(self):
        self.issues: List[ComplianceIssue] = []

        # Patterns that indicate potential compliance issues
        self.high_risk_patterns = {
            r'\b(cure|cures|cured|curing)\b': 'Medicinal claims without authorization',
            r'\b(guaranteed|guarantee)\b(?!\s+available|\s+included|\s+provided)': 'Absolute guarantees without qualification',
            r'\b(miracle|miraculous)\b': 'Exaggerated efficacy claims',
            r'\b100%\s*(effective|safe|natural|guaranteed)': 'Unsubstantiable absolute claims',
            r'\b(lose|loss)\s+\d+\s*(kg|pounds|lbs|stone)\s+in\s+\d+\s*(days|weeks)': 'Specific weight loss claims requiring substantiation',
            r'\bfree\b(?!\s+(?:from|of|delivery|shipping|returns))': 'Free claims without clear conditions',
            r'\b(number\s+one|#1|best|leading)\b(?!\s+seller)': 'Superiority claims requiring evidence',
        }

        self.medium_risk_patterns = {
            r'\b(proven|clinically proven)\b': 'Claims requiring scientific substantiation',
            r'\b(results?|works?)\s+in\s+\d+\s*(hours?|days?|weeks?)': 'Time-specific efficacy claims',
            r'\b(may|could|might)\s+(help|reduce|improve|increase)': 'Ambiguous hedged claims',
            r'\b(up to|upto)\s+\d+': 'Maximum claims that may be unrepresentative',
            r'\b(natural|organic|eco-friendly)\b': 'Environmental/natural claims requiring substantiation',
            r'\b(recommended by|endorsed by)\b': 'Endorsement claims requiring evidence',
            r'\b(doctor|clinically|medically|scientifically)\b': 'Professional/scientific claims requiring proof',
        }

        self.low_risk_patterns = {
            r'\b(help|helps|may help)\b': 'Hedged claims requiring clarity',
            r'\b(new|improved)\b': 'Comparative claims requiring basis',
            r'\b(quality|premium|luxury)\b': 'Subjective quality claims',
        }

        # Prohibited words for specific sectors
        self.prohibited_health_claims = [
            'cancer', 'arthritis', 'diabetes', 'heart disease',
            'blood pressure', 'cholesterol'
        ]

        # Common misleading phrases
        self.misleading_phrases = {
            'as seen on tv': 'Misleading if not actually featured',
            'limited time offer': 'Must specify actual time limit',
            'while stocks last': 'Must be genuine stock limitation',
            'exclusive': 'Must be genuinely exclusive',
        }

    def check_content(self, content: str, content_type: str = 'text') -> Dict:
        """
        Main method to check advertising content for ASA compliance

        Args:
            content: The advertising content to check
            content_type: 'text' or 'visual_description'

        Returns:
            Dictionary containing compliance analysis
        """
        self.issues = []
        content_lower = content.lower()

        # Run all compliance checks
        self._check_high_risk_patterns(content, content_lower)
        self._check_medium_risk_patterns(content, content_lower)
        self._check_low_risk_patterns(content, content_lower)
        self._check_prohibited_health_claims(content_lower)
        self._check_misleading_phrases(content_lower)
        self._check_pricing_claims(content, content_lower)
        self._check_comparative_claims(content_lower)
        self._check_testimonials(content_lower)
        self._check_environmental_claims(content_lower)
        self._check_clarity_and_ambiguity(content)

        # Categorize issues by risk level
        high_risk = [i for i in self.issues if i.risk_level == 'high']
        medium_risk = [i for i in self.issues if i.risk_level == 'medium']
        low_risk = [i for i in self.issues if i.risk_level == 'low']

        # Generate overall risk assessment
        overall_risk = self._calculate_overall_risk(high_risk, medium_risk, low_risk)

        return {
            'overall_risk': overall_risk,
            'high_risk_issues': [self._issue_to_dict(i) for i in high_risk],
            'medium_risk_issues': [self._issue_to_dict(i) for i in medium_risk],
            'low_risk_issues': [self._issue_to_dict(i) for i in low_risk],
            'total_issues': len(self.issues),
            'summary': self._generate_summary(high_risk, medium_risk, low_risk),
            'suggestions': self._generate_suggestions(content)
        }

    def _check_high_risk_patterns(self, content: str, content_lower: str):
        """Check for high-risk compliance issues"""
        for pattern, description in self.high_risk_patterns.items():
            matches = re.finditer(pattern, content_lower, re.IGNORECASE)
            for match in matches:
                suggestion = self._get_suggestion_for_pattern(pattern, match.group())
                self.issues.append(ComplianceIssue(
                    risk_level='high',
                    category='Unsubstantiated Claims',
                    description=description,
                    asa_rule='CAP Code 3.1, 3.7 (Misleading advertising, Substantiation)',
                    location=f'"{match.group()}" at position {match.start()}',
                    suggestion=suggestion
                ))

    def _check_medium_risk_patterns(self, content: str, content_lower: str):
        """Check for medium-risk compliance issues"""
        for pattern, description in self.medium_risk_patterns.items():
            matches = re.finditer(pattern, content_lower, re.IGNORECASE)
            for match in matches:
                suggestion = self._get_suggestion_for_pattern(pattern, match.group())
                self.issues.append(ComplianceIssue(
                    risk_level='medium',
                    category='Substantiation Required',
                    description=description,
                    asa_rule='CAP Code 3.7 (Substantiation)',
                    location=f'"{match.group()}" at position {match.start()}',
                    suggestion=suggestion
                ))

    def _check_low_risk_patterns(self, content: str, content_lower: str):
        """Check for low-risk compliance issues"""
        for pattern, description in self.low_risk_patterns.items():
            matches = re.finditer(pattern, content_lower, re.IGNORECASE)
            for match in matches:
                suggestion = self._get_suggestion_for_pattern(pattern, match.group())
                self.issues.append(ComplianceIssue(
                    risk_level='low',
                    category='Clarity Required',
                    description=description,
                    asa_rule='CAP Code 3.9 (Clarity)',
                    location=f'"{match.group()}" at position {match.start()}',
                    suggestion=suggestion
                ))

    def _check_prohibited_health_claims(self, content_lower: str):
        """Check for prohibited health claims"""
        for condition in self.prohibited_health_claims:
            if re.search(r'\b' + condition + r'\b', content_lower):
                if re.search(r'\b(cure|treat|prevent|reverse)\b.*\b' + condition + r'\b|' +
                           condition + r'.*\b(cure|treat|prevent|reverse)\b', content_lower):
                    self.issues.append(ComplianceIssue(
                        risk_level='high',
                        category='Prohibited Health Claims',
                        description=f'Prohibited medicinal claim regarding {condition}',
                        asa_rule='CAP Code 12.1 (Medicines, medical devices, health-related products and beauty products)',
                        location=f'Reference to "{condition}"',
                        suggestion=f'Remove claims to treat, cure, or prevent {condition}. Only licensed medicines can make such claims.'
                    ))

    def _check_misleading_phrases(self, content_lower: str):
        """Check for potentially misleading phrases"""
        for phrase, description in self.misleading_phrases.items():
            if phrase in content_lower:
                self.issues.append(ComplianceIssue(
                    risk_level='medium',
                    category='Potentially Misleading',
                    description=description,
                    asa_rule='CAP Code 3.1 (Misleading advertising)',
                    location=f'"{phrase}"',
                    suggestion=f'Ensure "{phrase}" is accurate and provide specific details/evidence.'
                ))

    def _check_pricing_claims(self, content: str, content_lower: str):
        """Check pricing and promotional claims"""
        # Check for percentage discounts
        discount_pattern = r'(\d+)%\s*off'
        matches = re.finditer(discount_pattern, content_lower)
        for match in matches:
            self.issues.append(ComplianceIssue(
                risk_level='medium',
                category='Pricing Claims',
                description='Discount claims must be genuine and substantiated',
                asa_rule='CAP Code 3.17, 3.40 (Prices)',
                location=f'"{match.group()}"',
                suggestion='Ensure discount is calculated from genuine previous price (not inflated). State time period of previous price.'
            ))

        # Check for "RRP" or "was" pricing
        if re.search(r'\b(rrp|was|were)\b.*£\d+', content_lower):
            self.issues.append(ComplianceIssue(
                risk_level='medium',
                category='Comparative Pricing',
                description='Comparative price claims must be verifiable',
                asa_rule='CAP Code 3.40 (Prices)',
                location='Comparative pricing found',
                suggestion='Ensure previous prices were genuine and offered for meaningful period (typically 28 days in preceding 6 months).'
            ))

    def _check_comparative_claims(self, content_lower: str):
        """Check comparative advertising claims"""
        comparative_terms = [
            'better than', 'more effective than', 'faster than',
            'stronger than', 'superior to', 'outperforms'
        ]

        for term in comparative_terms:
            if term in content_lower:
                self.issues.append(ComplianceIssue(
                    risk_level='high',
                    category='Comparative Claims',
                    description='Comparative claims must be objective and substantiated',
                    asa_rule='CAP Code 3.33-3.35 (Comparisons)',
                    location=f'"{term}"',
                    suggestion='Provide objective evidence for comparison. Clearly identify competitor or comparison basis.'
                ))

    def _check_testimonials(self, content_lower: str):
        """Check testimonial and endorsement usage"""
        testimonial_indicators = [
            'testimonial', 'review', 'customer said', 'user said',
            '"', "'", 'rated', 'stars'
        ]

        has_testimonial = any(indicator in content_lower for indicator in testimonial_indicators)

        if has_testimonial and re.search(r'["\'].*["\']', content_lower):
            self.issues.append(ComplianceIssue(
                risk_level='medium',
                category='Testimonials',
                description='Testimonials must be genuine and representative',
                asa_rule='CAP Code 3.45-3.47 (Endorsements and testimonials)',
                location='Testimonial/review content detected',
                suggestion='Ensure testimonials are genuine, verifiable, and representative of typical results. Include disclaimer if results are atypical.'
            ))

    def _check_environmental_claims(self, content_lower: str):
        """Check environmental and sustainability claims"""
        env_terms = ['eco-friendly', 'sustainable', 'green', 'carbon neutral',
                     'environmentally friendly', 'biodegradable', 'recyclable']

        for term in env_terms:
            if term in content_lower:
                self.issues.append(ComplianceIssue(
                    risk_level='medium',
                    category='Environmental Claims',
                    description=f'Environmental claim "{term}" requires clear substantiation',
                    asa_rule='CAP Code 11.1-11.4 (Environmental claims)',
                    location=f'"{term}"',
                    suggestion='Provide specific evidence for environmental claim. Avoid vague or unqualified claims. Specify which aspect is environmentally friendly.'
                ))

    def _check_clarity_and_ambiguity(self, content: str):
        """Check for unclear or ambiguous content"""
        # Check for overly complex sentences
        sentences = re.split(r'[.!?]+', content)
        for sentence in sentences:
            words = sentence.split()
            if len(words) > 40:
                self.issues.append(ComplianceIssue(
                    risk_level='low',
                    category='Clarity',
                    description='Overly complex sentence may be unclear',
                    asa_rule='CAP Code 3.9 (Clarity)',
                    location=f'Long sentence: "{sentence[:50]}..."',
                    suggestion='Break into shorter, clearer sentences to ensure message is easily understood.'
                ))

        # Check for missing key information indicators
        if re.search(r'\*|\†|‡|§', content):
            self.issues.append(ComplianceIssue(
                risk_level='medium',
                category='Clarity - Qualifications',
                description='Asterisks/footnotes detected - ensure qualifications are clear and prominent',
                asa_rule='CAP Code 3.9, 3.10 (Qualification)',
                location='Footnote markers found',
                suggestion='Ensure all important qualifications are sufficiently prominent, not just in footnotes. Material information should be clear upfront.'
            ))

    def _get_suggestion_for_pattern(self, pattern: str, matched_text: str) -> str:
        """Generate specific suggestions for pattern matches"""
        suggestions = {
            r'\b(cure|cures|cured|curing)\b': 'Replace with softer language like "may help manage" or remove claim entirely unless product is licensed medicine.',
            r'\b(guaranteed|guarantee)\b': 'Remove absolute guarantee or add clear qualifications (e.g., "money-back guarantee" with terms).',
            r'\b(miracle|miraculous)\b': 'Remove exaggerated language. Use objective, substantiated claims instead.',
            r'\b100%\s*(effective|safe|natural|guaranteed)': 'Remove absolute claim or replace with qualified statement supported by evidence.',
            r'\b(lose|loss)\s+\d+\s*(kg|pounds|lbs|stone)\s+in\s+\d+\s*(days|weeks)': 'Remove specific timeframe or add "up to" and disclaimer about typical results.',
            r'\bfree\b': 'Clarify "free" with conditions (e.g., "free with purchase", "free delivery on orders over £X").',
            r'\b(number\s+one|#1|best|leading)\b': 'Provide objective basis and evidence, or use qualified claim (e.g., "one of the leading...").',
            r'\b(proven|clinically proven)\b': 'Ensure robust clinical evidence exists and is available. Specify the proven aspect.',
            r'\b(results?|works?)\s+in\s+\d+\s*(hours?|days?|weeks?)': 'Add "up to" or "may see results" and clarify these are possible, not guaranteed outcomes.',
            r'\b(may|could|might)\s+(help|reduce|improve|increase)': 'Clarify the conditions under which this may occur. Be more specific.',
            r'\b(up to|upto)\s+\d+': 'Clarify that this is maximum result, not typical. Consider stating typical/average results.',
            r'\b(natural|organic|eco-friendly)\b': 'Specify which ingredients/aspects are natural. Provide certification or evidence.',
            r'\b(recommended by|endorsed by)\b': 'Provide specific details of who recommends and basis for recommendation.',
            r'\b(doctor|clinically|medically|scientifically)\b': 'Ensure scientific/medical claims are supported by appropriate evidence.',
            r'\b(help|helps|may help)\b': 'Specify what aspect it helps with and under what conditions.',
            r'\b(new|improved)\b': 'Specify what is new or improved compared to what.',
            r'\b(quality|premium|luxury)\b': 'Support with objective features or evidence of quality.',
        }

        for pat, suggestion in suggestions.items():
            if re.search(pat, pattern, re.IGNORECASE):
                return suggestion

        return 'Review and substantiate this claim with appropriate evidence.'

    def _calculate_overall_risk(self, high_risk: List, medium_risk: List, low_risk: List) -> str:
        """Calculate overall compliance risk level"""
        if len(high_risk) >= 3:
            return 'HIGH'
        elif len(high_risk) >= 1:
            return 'HIGH'
        elif len(medium_risk) >= 5:
            return 'HIGH'
        elif len(medium_risk) >= 2:
            return 'MEDIUM'
        elif len(low_risk) >= 5:
            return 'MEDIUM'
        elif len(low_risk) >= 1:
            return 'LOW'
        else:
            return 'COMPLIANT'

    def _generate_summary(self, high_risk: List, medium_risk: List, low_risk: List) -> str:
        """Generate a human-readable summary"""
        if not self.issues:
            return "No compliance issues detected. Content appears to meet basic ASA Code requirements."

        summary = f"Found {len(self.issues)} potential compliance issue(s): "
        parts = []

        if high_risk:
            parts.append(f"{len(high_risk)} high-risk")
        if medium_risk:
            parts.append(f"{len(medium_risk)} medium-risk")
        if low_risk:
            parts.append(f"{len(low_risk)} low-risk")

        summary += ", ".join(parts) + "."

        if high_risk:
            summary += " HIGH RISK issues require immediate attention and substantiation."

        return summary

    def _generate_suggestions(self, content: str) -> Dict[str, str]:
        """Generate overall suggestions for making content compliant"""
        suggestions = {
            'general': [],
            'substantiation_needed': [],
            'clarity_improvements': [],
            'revised_content': ''
        }

        # Collect substantiation requirements
        substantiation_issues = [i for i in self.issues if 'substantiat' in i.description.lower() or 'evidence' in i.description.lower()]
        if substantiation_issues:
            suggestions['substantiation_needed'] = [
                "Maintain documentary evidence for all claims",
                "Ensure scientific/clinical claims are supported by robust studies",
                "Keep evidence available for ASA review if challenged"
            ]

        # General improvements
        if self.issues:
            suggestions['general'] = [
                "Review all claims against CAP Code requirements",
                "Ensure all material information is clear and prominent",
                "Avoid absolute or exaggerated claims",
                "Qualify claims appropriately where needed",
                "Make sure pricing comparisons are genuine and substantiated"
            ]

        # Clarity improvements
        clarity_issues = [i for i in self.issues if i.category in ['Clarity', 'Clarity Required', 'Clarity - Qualifications']]
        if clarity_issues:
            suggestions['clarity_improvements'] = [
                "Use clear, simple language",
                "Avoid ambiguous or hedged statements",
                "Place important qualifications prominently, not just in small print",
                "Ensure consumers can easily understand the key message"
            ]

        # Generate revised content suggestion
        revised = content
        for issue in sorted(self.issues, key=lambda x: ['high', 'medium', 'low'].index(x.risk_level)):
            if issue.suggestion and issue.location:
                # This is simplified - in a real app, you'd do more sophisticated text replacement
                pass

        suggestions['revised_content'] = self._generate_compliant_version(content)

        return suggestions

    def _generate_compliant_version(self, content: str) -> str:
        """Generate a suggested compliant version of the content"""
        revised = content

        # Apply basic substitutions for common issues
        substitutions = {
            r'\bcure(s|d|ing)?\b': 'help manage',
            r'\bguaranteed?\b(?!\s+available|\s+included)': 'designed to',
            r'\bmiracle\b': 'innovative',
            r'\b100%\s*effective\b': 'shown to be effective',
            r'\b100%\s*safe\b': 'considered safe',
            r'\b100%\s*natural\b': 'made with natural ingredients',
        }

        for pattern, replacement in substitutions.items():
            revised = re.sub(pattern, replacement, revised, flags=re.IGNORECASE)

        # Add disclaimer if needed
        if len([i for i in self.issues if i.risk_level in ['high', 'medium']]) > 0:
            revised += "\n\n[Note: Individual results may vary. Claims should be supported by appropriate evidence.]"

        return revised

    def _issue_to_dict(self, issue: ComplianceIssue) -> Dict:
        """Convert ComplianceIssue to dictionary"""
        return {
            'risk_level': issue.risk_level,
            'category': issue.category,
            'description': issue.description,
            'asa_rule': issue.asa_rule,
            'location': issue.location,
            'suggestion': issue.suggestion
        }


def analyze_visual_content_description(description: str) -> Dict:
    """
    Analyze visual content based on description
    For actual image analysis, this would integrate with computer vision
    """
    checker = ASAComplianceChecker()

    # Add specific visual content checks
    visual_issues = []

    description_lower = description.lower()

    # Check for misleading visual representations
    if any(term in description_lower for term in ['before and after', 'before/after']):
        visual_issues.append({
            'risk_level': 'high',
            'category': 'Visual Claims',
            'description': 'Before/after images must be genuine, representative, and not misleading',
            'asa_rule': 'CAP Code 3.45 (Endorsements and testimonials)',
            'suggestion': 'Ensure images are genuine, taken under same conditions, and represent typical results. Include disclaimer if atypical.'
        })

    # Check for small print in visuals
    if any(term in description_lower for term in ['small text', 'small print', 'fine print', 'asterisk']):
        visual_issues.append({
            'risk_level': 'medium',
            'category': 'Visual Clarity',
            'description': 'Important information must be sufficiently prominent',
            'asa_rule': 'CAP Code 3.9 (Clarity)',
            'suggestion': 'Ensure all key terms and conditions are clearly visible and readable.'
        })

    # Standard text compliance check
    result = checker.check_content(description, 'visual_description')

    # Add visual-specific issues
    if visual_issues:
        for issue in visual_issues:
            if issue['risk_level'] == 'high':
                result['high_risk_issues'].append(issue)
            elif issue['risk_level'] == 'medium':
                result['medium_risk_issues'].append(issue)
        result['total_issues'] += len(visual_issues)

    return result
