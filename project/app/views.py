from django.shortcuts import render

# ==========================
# 임시 in-memory "테이블"
# ==========================

USERS = [
    {
        "id": 1,
        "username": "username1",
        "profile_image": "",
        "bio": "Hi, I'm username1",
    },
    {
        "id": 2,
        "username": "username2",
        "profile_image": "",
        "bio": "Hi, I'm username2",
    },
]

CHALLENGES = [
    {
        "id": 1,
        "title": "Morning Workout",
        "content": "매일 아침 7시에 20분 운동하기",
        "max_participants": 7,      # 방 정원
        "current_participants": 2,  # 현재 인원
        "is_group": True,           # 여러 명 가능한 그룹 챌린지
        "is_full": False,           # 꽉 찼는지 여부(개념상 컬럼)
        "master_id": 1,             # User.id 참조
        "created_at": "2025-11-18",
    },
    {
        "id": 2,
        "title": "No Sugar Week",
        "content": "일주일 동안 설탕 간식 끊기",
        "max_participants": 1,      # 1인 챌린지
        "current_participants": 1,  # 항상 1명
        "is_group": False,          # 혼자 하는 챌린지
        "is_full": True,            # 이미 혼자 꽉 찬 상태
        "master_id": 2,
        "created_at": "2025-11-19",
    },
]

# 중간 테이블: "어떤 유저가 어떤 챌린지에 참여 중인가"만 표현
CHALLENGE_PARTICIPANTS = [
    {"id": 1, "challenge_id": 1, "user_id": 1},
    {"id": 2, "challenge_id": 1, "user_id": 2},
    {"id": 3, "challenge_id": 2, "user_id": 2},
]

VERIFICATIONS = [
    {"id": 1, "image": "run_1.png", "date": "2025-11-18", "user_id": 1, "challenge_id": 1},
    {"id": 2, "image": "run_2.png", "date": "2025-11-18", "user_id": 2, "challenge_id": 1},
]


def get_current_user():
    """지금은 첫 번째 User를 '로그인 유저'라고 가정."""
    return USERS[0]


def get_participating_challenges(user_id: int):
    # 내가 참여한 challenge_id 목록
    joined_ids = {
        row["challenge_id"]
        for row in CHALLENGE_PARTICIPANTS
        if row["user_id"] == user_id
    }

    result = []
    for ch in CHALLENGES:
        if ch["id"] in joined_ids:
            # 정원 / 현재 인원 계산
            if ch["is_group"]:
                capacity = ch["max_participants"]
                participants_count = ch["current_participants"]
            else:
                # 1인 챌린지: 방장 혼자
                capacity = 1
                participants_count = 1

            # 꽉 찼는지 여부
            is_full = participants_count >= capacity

            # progress: "방이 얼마나 찼는지" 퍼센트
            if capacity > 0:
                progress = int(participants_count / capacity * 100)
                if progress > 100:
                    progress = 100
            else:
                progress = 0

            result.append(
                {
                    **ch,  # id, title, content, max_participants, current_participants, is_group, is_full, master_id, created_at
                    "participants_count": participants_count,
                    "capacity": capacity,
                    "progress": progress,
                    "is_full": is_full, 
                }
            )
    return result


# ==========================
# 뷰 함수
# ==========================

def mypage(request):
    user = get_current_user()
    participating_challenges = get_participating_challenges(user["id"])

    # User 테이블 구조 + participating_count
    profile = {
        "id": user["id"],
        "username": user["username"],
        "profile_image": user["profile_image"],
        "bio": user["bio"],
        "participating_count": len(participating_challenges),
    }

    menu_items = [
        {"name": "My Challenges", "url_name": "my_challenges"},
        {"name": "Upload History", "url_name": "upload_history"},
        {"name": "Edit Profile", "url_name": "edit_profile"},
        {"name": "Settings", "url_name": "#"},  
        {"name": "Log Out", "url_name": "#"},   
    ]

    context = {
        "profile": profile,
        "menu_items": menu_items,
    }
    return render(request, "mypage.html", context)


def my_challenges(request):
    user = get_current_user()
    challenges = get_participating_challenges(user["id"])

    context = {"challenges": challenges}
    return render(request, "my_challenges.html", context)


def edit_profile(request):
    return render(request, "edit_profile.html")


def upload_history(request):
    return render(request, "upload_history.html")
