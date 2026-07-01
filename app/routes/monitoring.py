from flask import Blueprint, jsonify
from app.models import db

monitoring_bp = Blueprint('monitoring', __name__)

@monitoring_bp.route('/health', methods=['GET'])
def health():
    """General health check endpoint."""
    return jsonify({"status": "healthy", "service": "AI Medical Assistant"}), 200

@monitoring_bp.route('/live', methods=['GET'])
def liveness():
    """Liveness probe for orchestrators like Docker/Kubernetes."""
    return jsonify({"status": "alive"}), 200

@monitoring_bp.route('/ready', methods=['GET'])
def readiness():
    """Readiness probe to ensure database is reachable."""
    try:
        # Execute a simple query to ensure DB is connected
        db.session.execute(db.text('SELECT 1'))
        return jsonify({"status": "ready", "database": "connected"}), 200
    except Exception as e:
        return jsonify({"status": "unready", "error": str(e)}), 503
