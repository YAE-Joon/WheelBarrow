from enum import Enum

class WorkStatus(str,Enum):
    TODO = "예정"
    IN_PROGRESS = "진행중"
    UNDER_REVIEW = "검토중"
    REJECTED = "반려"
    DONE = "완료"
    CANCELLED = "취소"
    

