"""
Rate Limiting 구현
사용자별 질의 횟수 제한
"""

import time
import logging
from collections import defaultdict
from typing import Dict, List
import os

logger = logging.getLogger(__name__)


class RateLimiter:
    """간단한 Rate Limiter (토큰 버킷 알고리즘)"""

    def __init__(
        self,
        requests_per_minute: int = 30,
        requests_per_hour: int = 100
    ):
        """
        Args:
            requests_per_minute: 분당 요청 제한
            requests_per_hour: 시간당 요청 제한
        """
        self.rpm = requests_per_minute
        self.rph = requests_per_hour

        # 사용자별 요청 기록
        self.requests: Dict[str, List[float]] = defaultdict(list)

    def _cleanup_old_requests(self, user_id: str, current_time: float):
        """1시간 이전 요청 기록 삭제

        Args:
            user_id: 사용자 ID
            current_time: 현재 시간
        """
        self.requests[user_id] = [
            req_time for req_time in self.requests[user_id]
            if current_time - req_time < 3600  # 1시간
        ]

    def is_allowed(self, user_id: str) -> tuple[bool, str]:
        """요청 허용 여부 확인

        Args:
            user_id: 사용자 ID

        Returns:
            (허용 여부, 에러 메시지) 튜플
        """
        current_time = time.time()

        # 오래된 요청 기록 정리
        self._cleanup_old_requests(user_id, current_time)

        # 분당 제한 확인
        recent_minute = [
            req_time for req_time in self.requests[user_id]
            if current_time - req_time < 60  # 1분
        ]

        if len(recent_minute) >= self.rpm:
            return False, f"분당 {self.rpm}회 제한을 초과했습니다. 잠시 후 다시 시도해주세요."

        # 시간당 제한 확인
        if len(self.requests[user_id]) >= self.rph:
            return False, f"시간당 {self.rph}회 제한을 초과했습니다. 나중에 다시 시도해주세요."

        # 요청 기록 추가
        self.requests[user_id].append(current_time)
        logger.info(f"Rate limit check passed for {user_id}: {len(recent_minute)+1}/{self.rpm} per minute")

        return True, ""

    def get_usage_stats(self, user_id: str) -> Dict[str, int]:
        """사용자의 사용량 통계 반환

        Args:
            user_id: 사용자 ID

        Returns:
            사용량 통계 딕셔너리
        """
        current_time = time.time()
        self._cleanup_old_requests(user_id, current_time)

        recent_minute = [
            req_time for req_time in self.requests[user_id]
            if current_time - req_time < 60
        ]

        return {
            "requests_last_minute": len(recent_minute),
            "requests_last_hour": len(self.requests[user_id]),
            "limit_per_minute": self.rpm,
            "limit_per_hour": self.rph,
            "remaining_minute": max(0, self.rpm - len(recent_minute)),
            "remaining_hour": max(0, self.rph - len(self.requests[user_id]))
        }


# 전역 Rate Limiter 인스턴스
_rate_limiter = None


def get_rate_limiter() -> RateLimiter:
    """Rate Limiter 싱글톤 인스턴스 반환

    Returns:
        RateLimiter 인스턴스
    """
    global _rate_limiter

    if _rate_limiter is None:
        rpm = int(os.getenv("RATE_LIMIT_PER_MINUTE", "30"))
        rph = int(os.getenv("RATE_LIMIT_PER_HOUR", "100"))
        _rate_limiter = RateLimiter(
            requests_per_minute=rpm,
            requests_per_hour=rph
        )
        logger.info(f"Rate Limiter initialized: {rpm}/min, {rph}/hour")

    return _rate_limiter
