"""
Chainlit 인증 시스템
간단하지만 안전한 인증 구현
"""

import os
import hashlib
import secrets
from typing import Optional
import chainlit as cl


def hash_password(password: str, salt: Optional[str] = None) -> tuple[str, str]:
    """비밀번호 해싱 (SHA-256 + salt)

    Args:
        password: 평문 비밀번호
        salt: 솔트 (없으면 자동 생성)

    Returns:
        (해시값, 솔트) 튜플
    """
    if salt is None:
        salt = secrets.token_hex(16)

    hash_value = hashlib.sha256(f"{password}{salt}".encode()).hexdigest()
    return hash_value, salt


def verify_password(password: str, hash_value: str, salt: str) -> bool:
    """비밀번호 검증

    Args:
        password: 입력된 비밀번호
        hash_value: 저장된 해시값
        salt: 솔트

    Returns:
        비밀번호 일치 여부
    """
    computed_hash, _ = hash_password(password, salt)
    return computed_hash == hash_value


# 환경변수에서 인증 정보 로드
AUTH_ENABLED = os.getenv("AUTH_ENABLED", "false").lower() == "true"
AUTH_USERNAME = os.getenv("AUTH_USERNAME", "admin")
AUTH_PASSWORD = os.getenv("AUTH_PASSWORD", "futuresystem2025")
AUTH_SALT = os.getenv("AUTH_SALT", secrets.token_hex(16))

# 비밀번호 해싱
AUTH_PASSWORD_HASH, AUTH_SALT = hash_password(AUTH_PASSWORD, AUTH_SALT)


@cl.password_auth_callback
def auth_callback(username: str, password: str) -> Optional[cl.User]:
    """Chainlit 인증 콜백

    Args:
        username: 사용자명
        password: 비밀번호

    Returns:
        인증 성공 시 User 객체, 실패 시 None
    """
    if not AUTH_ENABLED:
        # 인증 비활성화 시 모든 사용자 허용
        return cl.User(identifier=username, metadata={"role": "user"})

    # 사용자명 확인
    if username != AUTH_USERNAME:
        return None

    # 비밀번호 확인
    if not verify_password(password, AUTH_PASSWORD_HASH, AUTH_SALT):
        return None

    # 인증 성공
    return cl.User(
        identifier=username,
        metadata={
            "role": "admin",
            "provider": "credentials"
        }
    )


def get_current_user() -> Optional[cl.User]:
    """현재 로그인한 사용자 정보 반환

    Returns:
        User 객체 또는 None
    """
    return cl.user_session.get("user")
