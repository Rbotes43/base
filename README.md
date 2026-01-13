# 🇬🇧 ASA Compliance Checker

**UK Advertising Standards Authority Code Review Tool**

An intelligent web application that reviews advertising content and copy against the UK ASA (Advertising Standards Authority) Code for compliance. The tool identifies non-compliance risks, categorizes them by severity, and provides actionable suggestions for making content compliant.

---

## 📋 Features

### Core Functionality
- ✅ **Text Content Analysis** - Paste advertising copy for instant compliance checking
- ✅ **Visual Content Upload** - Upload images (PNG, JPG, GIF, etc.) for analysis
- ✅ **Risk Categorization** - Issues flagged as High, Medium, or Low risk
- ✅ **ASA Code References** - Each issue links to specific CAP Code requirements
- ✅ **Substantiation Alerts** - Identifies claims requiring evidence
- ✅ **Compliance Suggestions** - Get specific recommendations for each issue
- ✅ **Revised Content Generation** - Automatically suggests compliant versions

### What It Checks

The tool analyzes content against multiple ASA Code requirements:

#### High Risk Issues
- ❌ Medicinal claims without authorization
- ❌ Absolute guarantees without qualification
- ❌ Exaggerated efficacy claims ("miracle", "cure")
- ❌ Unsubstantiable absolute claims (100% effective/safe)
- ❌ Specific weight loss claims without evidence
- ❌ Misleading "free" claims
- ❌ Superiority claims without proof

#### Medium Risk Issues
- ⚠️ Claims requiring scientific substantiation
- ⚠️ Time-specific efficacy claims
- ⚠️ Environmental/natural claims
- ⚠️ Endorsements without evidence
- ⚠️ Professional/scientific claims
- ⚠️ Pricing and discount claims
- ⚠️ Comparative advertising

#### Low Risk Issues
- ℹ️ Ambiguous or unclear claims
- ℹ️ Subjective quality claims
- ℹ️ Claims requiring better qualification

### ASA Code Coverage

The tool checks compliance with:
- **CAP Code 3.1** - Misleading advertising
- **CAP Code 3.7** - Substantiation
- **CAP Code 3.9** - Clarity
- **CAP Code 3.10** - Qualification
- **CAP Code 3.17, 3.40** - Prices
- **CAP Code 3.33-3.35** - Comparisons
- **CAP Code 3.45-3.47** - Endorsements and testimonials
- **CAP Code 11.1-11.4** - Environmental claims
- **CAP Code 12.1** - Medicines and health-related products

---

## 🚀 Quick Start

### Prerequisites

- Python 3.8 or higher
- pip (Python package installer)

### Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd base
   ```

2. **Create a virtual environment** (recommended)
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Optional: Configure AI-powered image analysis**

   For advanced visual content analysis using Claude AI:
   ```bash
   cp .env.example .env
   # Edit .env and add your Anthropic API key
   ```

   Get an API key from: https://console.anthropic.com/

5. **Run the application**
   ```bash
   python app.py
   ```

6. **Open your browser**

   Navigate to: http://localhost:5000

---

## 💻 Usage

### Checking Text Content

1. Click the **"📝 Text Content"** tab
2. Paste your advertising copy into the text area
3. Click **"🔍 Check Compliance"**
4. Review the results:
   - Overall risk assessment
   - Detailed issues by risk level
   - ASA Code references
   - Specific suggestions
5. Click **"💡 View Suggested Changes"** for compliant alternatives

### Checking Visual Content

1. Click the **"🖼️ Visual Content"** tab
2. Upload an image by:
   - Clicking the upload area and selecting a file
   - Dragging and dropping an image
3. Click **"🔍 Check Compliance"**
4. Review the analysis results

**Note:** Visual content analysis works best with the optional Anthropic API key configured. Without it, basic validation is performed.

### Example Text to Test

Try this example advertising copy:

```
Lose 10kg in just 2 weeks with our miracle weight loss pill!
100% guaranteed results. Clinically proven formula that cures
obesity. Free trial - limited time only! Rated #1 by doctors.
```

This will trigger multiple high-risk compliance issues.

---

## 🏗️ Project Structure

```
base/
├── app.py                  # Flask backend application
├── asa_compliance.py       # Core compliance checking logic
├── requirements.txt        # Python dependencies
├── .env.example           # Environment variables template
├── .gitignore             # Git ignore rules
├── README.md              # This file
├── templates/
│   └── index.html         # Frontend interface
├── static/                # Static assets (auto-created)
└── uploads/               # Temporary file uploads
    └── .gitkeep
```

---

## 🔧 Configuration

### Environment Variables

Create a `.env` file (copy from `.env.example`):

```bash
# Optional: Anthropic API Key for AI-powered image analysis
ANTHROPIC_API_KEY=your_api_key_here
```

### Application Settings

Edit `app.py` to customize:
- `MAX_CONTENT_LENGTH` - Maximum upload file size (default: 16MB)
- `ALLOWED_EXTENSIONS` - Supported image formats
- Server host and port (default: `0.0.0.0:5000`)

---

## 🔍 API Endpoints

The application provides REST API endpoints:

### Check Text Content
```
POST /api/check-text
Content-Type: application/json

{
  "content": "Your advertising text here"
}
```

**Response:**
```json
{
  "overall_risk": "HIGH|MEDIUM|LOW|COMPLIANT",
  "high_risk_issues": [...],
  "medium_risk_issues": [...],
  "low_risk_issues": [...],
  "total_issues": 5,
  "summary": "Found 5 potential compliance issue(s)...",
  "suggestions": {
    "general": [...],
    "substantiation_needed": [...],
    "clarity_improvements": [...],
    "revised_content": "..."
  }
}
```

### Check Visual Content
```
POST /api/check-visual
Content-Type: multipart/form-data

file: [image file]
```

### Health Check
```
GET /health

Response: {
  "status": "healthy",
  "service": "ASA Compliance Tool",
  "ai_enabled": true|false
}
```

---

## 📚 Understanding Compliance Results

### Risk Levels

| Level | Meaning | Action Required |
|-------|---------|-----------------|
| **HIGH** | Likely breaches ASA Code | Immediate attention required. Must substantiate or remove claims. |
| **MEDIUM** | Requires substantiation | Ensure evidence exists and is available for ASA review. |
| **LOW** | Best practice improvements | Consider revising for clarity and consumer understanding. |
| **COMPLIANT** | No issues detected | Content appears to meet basic ASA requirements. |

### Common Issues and How to Fix Them

#### 1. Absolute Claims ("100% effective", "guaranteed")
- **Problem:** Cannot be substantiated absolutely
- **Fix:** Use qualified language like "designed to", "may help", "shown to be effective"

#### 2. Medicinal Claims ("cure", "treat")
- **Problem:** Only licensed medicines can make these claims
- **Fix:** Remove or replace with "help manage", "support"

#### 3. Superiority Claims ("best", "#1")
- **Problem:** Requires objective evidence
- **Fix:** Provide basis ("best-selling in category") or use "one of the leading"

#### 4. Time-Specific Claims ("results in 7 days")
- **Problem:** Must be typical, not exceptional
- **Fix:** Add "up to" or "may see results" with disclaimer

#### 5. "Free" Claims
- **Problem:** Must be genuinely free
- **Fix:** Clarify conditions ("free with purchase over £X")

---

## ⚖️ Legal Disclaimer

**This tool is for guidance only and does not constitute legal advice.**

- The tool provides automated analysis based on common ASA Code requirements
- It may not catch all compliance issues
- It does not replace professional legal or compliance review
- Always seek advice from qualified advertising compliance professionals
- The ASA may assess advertising differently based on context
- You are responsible for ensuring your advertising complies with all applicable laws and codes

For official guidance, visit:
- UK ASA: https://www.asa.org.uk/
- CAP Code: https://www.asa.org.uk/codes-and-rulings/advertising-codes.html

---

## 🛠️ Development

### Running in Development Mode

```bash
python app.py
```

The server runs with Flask's debug mode enabled for development.

### Testing

Test the compliance checker directly:

```python
from asa_compliance import ASAComplianceChecker

checker = ASAComplianceChecker()
results = checker.check_content("Your advertising text here")
print(results)
```

### Adding New Compliance Rules

Edit `asa_compliance.py` and add patterns to:
- `high_risk_patterns` - For serious violations
- `medium_risk_patterns` - For claims requiring substantiation
- `low_risk_patterns` - For clarity issues

---

## 📝 Dependencies

- **Flask 3.0.0** - Web framework
- **Werkzeug 3.0.1** - WSGI utilities
- **Pillow 10.1.0** - Image processing
- **anthropic 0.39.0** - Claude AI API (optional)
- **python-dotenv 1.0.0** - Environment variable management

---

## 🤝 Contributing

Contributions are welcome! Areas for improvement:

1. **Additional ASA Code Rules** - Expand pattern matching
2. **Industry-Specific Checks** - Add sector-specific rules (finance, alcohol, etc.)
3. **Better Visual Analysis** - Enhance image content detection
4. **Multi-language Support** - Support for other languages
5. **Export Functionality** - PDF reports of compliance analysis
6. **Batch Processing** - Check multiple pieces of content at once

---

## 📄 License

This project is provided as-is for educational and compliance assistance purposes.

---

## 🆘 Support

For issues, questions, or suggestions:
1. Check existing documentation
2. Review ASA guidance at https://www.asa.org.uk/
3. Open an issue in the repository

---

## 🎯 Roadmap

Future enhancements planned:
- [ ] Batch content checking
- [ ] Export reports to PDF
- [ ] Historical tracking of checks
- [ ] Industry-specific rule sets
- [ ] Integration with CMS platforms
- [ ] API rate limiting and authentication
- [ ] Multi-user support with team features

---

## 📊 Examples

### High-Risk Example

**Input:**
```
Miracle cure for diabetes! 100% guaranteed to reverse your
condition in 30 days. Clinically proven. Free bottle today!
```

**Issues Found:**
- High Risk: Medicinal claim "cure for diabetes"
- High Risk: Absolute guarantee without qualification
- High Risk: Exaggerated claim "miracle"
- High Risk: Unsubstantiable "100% guaranteed"
- High Risk: Misleading "free" claim
- Medium Risk: "Clinically proven" requires robust evidence

### Compliant Example

**Input:**
```
Our weight management supplement is designed to support your
health goals when used as part of a balanced diet and exercise
program. Results may vary. Contains natural ingredients.
Money-back guarantee available - see terms and conditions.
```

**Issues Found:**
- Low Risk: "may vary" statement could be more specific
- Low Risk: "natural" claim requires clarification

---

**Built for UK advertising compliance | Last updated: January 2026**
