import logging
import uuid
from flask import Blueprint, render_template, request, session
from app.services.chat_service import get_chat_response
from app.services.memory_service import get_session_history

main_bp = Blueprint('main', __name__)
logger = logging.getLogger(__name__)

import os
from werkzeug.utils import secure_filename
from flask import jsonify

from flask_login import login_required, current_user
from flask import redirect, url_for

ALLOWED_EXTENSIONS = {'pdf', 'png', 'jpg', 'jpeg'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@main_bp.route('/upload_report', methods=['POST'])
@login_required
def upload_report():
    if 'file' not in request.files:
        return jsonify({"error": "No file part"}), 400
        
    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400
        
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        upload_folder = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'data', 'uploads')
        os.makedirs(upload_folder, exist_ok=True)
        filepath = os.path.join(upload_folder, filename)
        file.save(filepath)
        
        try:
            from app.services.ocr_service import extract_text_from_file
            from app.services.memory_service import add_report_to_memory
            from app.services.medical_analyzer import analyze_report
            from app.services.risk_classifier import get_risk_color, get_value_color

            # 1. OCR Extraction
            extracted_text = extract_text_from_file(filepath)
            
            session_id = request.form.get('session_id')
            if session_id:
                str_session_id = f"user_{current_user.id}_chat_{session_id}"
                add_report_to_memory(str_session_id, extracted_text)
            
            # 3. Structural Analysis
            analysis = analyze_report(extracted_text)
            
            # Save to Database
            from app.models import MedicalReport, db
            import json
            report = MedicalReport(
                user_id=current_user.id,
                filename=filename,
                extracted_text=extracted_text,
                analysis_json=json.dumps(analysis),
                urgency_level=analysis.get('urgency_level', 'NORMAL')
            )
            db.session.add(report)
            db.session.commit()
            
            # Add UI formatting metadata
            analysis['risk_color'] = get_risk_color(analysis.get('urgency_level', 'Normal'))
            for abnormal in analysis.get('abnormal_values', []):
                if isinstance(abnormal, dict):
                    abnormal['color'] = get_value_color(abnormal.get('status', 'Normal'))
            
            # Clean up the file
            os.remove(filepath)
            
            return jsonify(analysis)
        except Exception as e:
            logger.error(f"Error processing upload: {e}")
            return jsonify({"error": str(e)}), 500
    
    return jsonify({"error": "File type not allowed. Please upload PDF, JPG, or PNG."}), 400


@main_bp.route('/', methods=['GET'])
def index():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard.index'))
    return render_template('auth/landing.html')

@main_bp.route('/health', methods=['GET'])
def health_check():
    return jsonify({"status": "ok"}), 200

@main_bp.route('/chat/<int:session_id>', methods=['GET'])
@login_required
def chat_view(session_id):
    from app.models import ChatSession
    # Ensure this session belongs to the current user
    chat_session = ChatSession.query.filter_by(id=session_id, user_id=current_user.id).first_or_404()
    
    # We still use the file-based memory_service for LangChain, but keyed by the string ID
    str_session_id = f"user_{current_user.id}_chat_{session_id}"
    history_obj = get_session_history(str_session_id)
    
    return render_template('index.html', history=history_obj.messages, current_chat=chat_session)

@main_bp.route('/chat_stream', methods=['GET'])
@login_required
def chat_stream():
    from flask import Response, stream_with_context
    from app.services.chat_service import stream_chat_response
    
    user_input = request.args.get('user_input', '')
    session_id = request.args.get('session_id')
    
    if not user_input.strip() or not session_id:
        return jsonify({"error": "Empty input or missing session"}), 400
        
    # verify ownership
    from app.models import ChatSession
    chat_session = ChatSession.query.filter_by(id=session_id, user_id=current_user.id).first()
    if not chat_session:
        return jsonify({"error": "Unauthorized"}), 403
        
    # Pass the unique string ID to LangChain
    str_session_id = f"user_{current_user.id}_chat_{session_id}"
    logger.info(f"Streaming response for session {str_session_id}")
    return Response(stream_with_context(stream_chat_response(str_session_id, user_input)), mimetype='text/event-stream')

@main_bp.route('/generate_tts', methods=['POST'])
def generate_tts():
    from app.services.tts_service import generate_audio
    data = request.json
    text = data.get('text', '')
    lang = data.get('lang', 'en')
    
    if not text:
        return jsonify({"error": "No text provided"}), 400
        
    # generate_audio returns just the filename (e.g. hash.mp3)
    filename = generate_audio(text, lang)
    if filename:
        return jsonify({"audio_url": f"/audio/{filename}"})
    return jsonify({"error": "TTS failed"}), 500

@main_bp.route('/audio/<filename>')
def serve_audio(filename):
    from flask import send_from_directory
    from app.services.tts_service import AUDIO_DIR
    return send_from_directory(AUDIO_DIR, filename)

@main_bp.app_errorhandler(404)
def page_not_found(e):
    return render_template('index.html', error="Page not found. Please try again."), 404

@main_bp.app_errorhandler(500)
def internal_server_error(e):
    logger.error(f"Internal server error: {e}")
    return render_template('index.html', error="Internal server error. Please try again later."), 500
