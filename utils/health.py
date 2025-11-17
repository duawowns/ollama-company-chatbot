"""
헬스 체크 엔드포인트
시스템 상태 모니터링
"""

import logging
import requests
import os
from pathlib import Path

logger = logging.getLogger(__name__)

OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")


def check_ollama() -> tuple[bool, str]:
    """Ollama 서버 연결 확인

    Returns:
        (정상 여부, 메시지) 튜플
    """
    try:
        response = requests.get(
            f"{OLLAMA_BASE_URL}/api/tags",
            timeout=5
        )

        if response.status_code == 200:
            models = response.json().get("models", [])
            return True, f"Ollama OK ({len(models)} models)"
        else:
            return False, f"Ollama HTTP {response.status_code}"

    except requests.exceptions.Timeout:
        return False, "Ollama timeout"
    except requests.exceptions.ConnectionError:
        return False, "Ollama connection refused"
    except Exception as e:
        return False, f"Ollama error: {str(e)}"


def check_vectorstore() -> tuple[bool, str]:
    """벡터 스토어 존재 확인

    Returns:
        (정상 여부, 메시지) 튜플
    """
    try:
        vectorstore_path = Path("data/vectorstore")

        if not vectorstore_path.exists():
            return False, "Vectorstore not found"

        # chroma.sqlite3 파일 확인
        db_file = vectorstore_path / "chroma.sqlite3"
        if not db_file.exists():
            return False, "Vectorstore DB missing"

        # 파일 크기 확인
        size_mb = db_file.stat().st_size / (1024 * 1024)
        return True, f"Vectorstore OK ({size_mb:.1f}MB)"

    except Exception as e:
        return False, f"Vectorstore error: {str(e)}"


def get_health_status() -> dict:
    """전체 시스템 헬스 체크

    Returns:
        헬스 상태 딕셔너리
    """
    ollama_ok, ollama_msg = check_ollama()
    vectorstore_ok, vectorstore_msg = check_vectorstore()

    overall_status = "healthy" if (ollama_ok and vectorstore_ok) else "degraded"

    if not ollama_ok and not vectorstore_ok:
        overall_status = "unhealthy"

    return {
        "status": overall_status,
        "components": {
            "ollama": {
                "status": "healthy" if ollama_ok else "unhealthy",
                "message": ollama_msg
            },
            "vectorstore": {
                "status": "healthy" if vectorstore_ok else "unhealthy",
                "message": vectorstore_msg
            }
        },
        "version": "1.0.0"
    }
