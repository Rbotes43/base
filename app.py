"""
ASA Compliance Tool - Flask Backend
UK Advertising Standards Authority compliance checker
"""

from flask import Flask, render_template, request, jsonify
from werkzeug.utils import secure_filename
import os
from PIL import Image
import base64
from io import BytesIO
from asa_compliance import ASAComplianceChecker, analyze_visual_content_description
from anthropic import Anthropic
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['ALLOWED_EXTENSIONS'] = {'png', 'jpg', 'jpeg', 'gif', 'bmp', 'webp'}

# Create uploads directory if it doesn't exist
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# Initialize Anthropic client (optional, for advanced image analysis)
anthropic_client = None
if os.getenv('ANTHROPIC_API_KEY'):
    try:
        anthropic_client = Anthropic(api_key=os.getenv('ANTHROPIC_API_KEY'))
    except Exception:
        pass


def allowed_file(filename):
    """Check if file extension is allowed"""
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']


def image_to_base64(image_path):
    """Convert image to base64 for API calls"""
    with open(image_path, 'rb') as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')


def analyze_image_with_ai(image_path):
    """
    Analyze image content using Claude AI for advertising compliance
    This provides advanced visual content analysis
    """
    if not anthropic_client:
        return None

    try:
        # Get image format
        image_format = image_path.rsplit('.', 1)[1].lower()
        if image_format == 'jpg':
            image_format = 'jpeg'

        # Read and encode image
        image_data = image_to_base64(image_path)

        # Create message with image
        message = anthropic_client.messages.create(
            model="claude-3-5-sonnet-20241022",
            max_tokens=2000,
            messages=[
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "image",
                            "source": {
                                "type": "base64",
                                "media_type": f"image/{image_format}",
                                "data": image_data,
                            },
                        },
                        {
                            "type": "text",
                            "text": """Analyze this advertising image for UK ASA Code compliance. Identify:

1. All text visible in the image (transcribe exactly)
2. Any claims made (explicit or implied)
3. Visual representations that might be misleading
4. Before/after imagery or testimonials
5. Price comparisons or promotional offers
6. Small print or disclaimers
7. Health, beauty, or efficacy claims
8. Comparative or superiority claims
9. Any other advertising elements

Provide a detailed description of the advertising content and any compliance concerns."""
                        }
                    ],
                }
            ],
        )

        return message.content[0].text

    except Exception as e:
        print(f"Error analyzing image with AI: {e}")
        return None


@app.route('/')
def index():
    """Render main page"""
    return render_template('index.html')


@app.route('/api/check-text', methods=['POST'])
def check_text():
    """Check text content for ASA compliance"""
    try:
        data = request.get_json()
        content = data.get('content', '')

        if not content or not content.strip():
            return jsonify({'error': 'No content provided'}), 400

        # Run compliance check
        checker = ASAComplianceChecker()
        results = checker.check_content(content)

        return jsonify(results)

    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/check-visual', methods=['POST'])
def check_visual():
    """Check visual content for ASA compliance"""
    try:
        if 'file' not in request.files:
            return jsonify({'error': 'No file provided'}), 400

        file = request.files['file']

        if file.filename == '':
            return jsonify({'error': 'No file selected'}), 400

        if not allowed_file(file.filename):
            return jsonify({'error': 'Invalid file type. Allowed: PNG, JPG, JPEG, GIF, BMP, WEBP'}), 400

        # Save file
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)

        # Try AI-powered analysis first
        visual_description = None
        if anthropic_client:
            visual_description = analyze_image_with_ai(filepath)

        # If AI analysis available, use it; otherwise use basic analysis
        if visual_description:
            checker = ASAComplianceChecker()
            results = checker.check_content(visual_description, 'visual_description')
            results['visual_analysis'] = visual_description
        else:
            # Basic analysis without AI
            results = {
                'overall_risk': 'UNKNOWN',
                'high_risk_issues': [],
                'medium_risk_issues': [{
                    'risk_level': 'medium',
                    'category': 'Visual Content Analysis',
                    'description': 'Visual content requires manual review. AI analysis not available.',
                    'asa_rule': 'CAP Code 3.1 (Misleading advertising)',
                    'location': 'Entire image',
                    'suggestion': 'Manually review image for: misleading visuals, before/after claims, small print visibility, price claims, testimonials, and any implied claims.'
                }],
                'low_risk_issues': [],
                'total_issues': 1,
                'summary': 'Visual content uploaded. Manual review recommended as AI analysis is not configured.',
                'suggestions': {
                    'general': [
                        'Ensure visual content is not misleading',
                        'Check all text in image is legible and prominent',
                        'Verify before/after images are representative',
                        'Ensure price comparisons are accurate'
                    ],
                    'substantiation_needed': [],
                    'clarity_improvements': [],
                    'revised_content': ''
                }
            }

        # Clean up uploaded file
        try:
            os.remove(filepath)
        except Exception:
            pass

        return jsonify(results)

    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/get-suggestions', methods=['POST'])
def get_suggestions():
    """Get detailed suggestions for making content compliant"""
    try:
        data = request.get_json()
        content = data.get('content', '')
        issues = data.get('issues', [])

        if not content:
            return jsonify({'error': 'No content provided'}), 400

        checker = ASAComplianceChecker()
        results = checker.check_content(content)

        return jsonify({
            'suggestions': results['suggestions'],
            'revised_content': results['suggestions']['revised_content']
        })

    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/health')
def health():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'service': 'ASA Compliance Tool',
        'ai_enabled': anthropic_client is not None
    })


if __name__ == '__main__':
    print("=" * 60)
    print("ASA COMPLIANCE TOOL - Starting Server")
    print("=" * 60)
    print("🏴󐁧󐁢󐁥󐁮󐁧󐁿  UK Advertising Standards Authority Compliance Checker")
    print("\nFeatures:")
    print("  ✓ Text content analysis")
    print("  ✓ Visual content upload")
    print("  ✓ Risk categorization (High/Medium/Low)")
    print("  ✓ Compliance suggestions")
    print("  ✓ ASA Code references")

    if anthropic_client:
        print("  ✓ AI-powered image analysis (ENABLED)")
    else:
        print("  ⚠ AI-powered image analysis (DISABLED - set ANTHROPIC_API_KEY)")

    print("\n" + "=" * 60)
    print("Server running at: http://localhost:5000")
    print("=" * 60 + "\n")

    app.run(debug=True, host='0.0.0.0', port=5000)
