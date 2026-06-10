from datetime import datetime, timezone
from services.match_service import load_matches


STAGES = [
    "Group Stage",
    "Round of 32",
    "Round of 16",
    "Quarter Finals",
    "Semi Finals",
    "Final"
]


def get_active_prediction_stage():

    matches = load_matches()

    now = datetime.now(timezone.utc)

    for stage in STAGES:

        stage_matches = [
            m for m in matches
            if m.stage == stage
        ]

        if not stage_matches:
            continue

        start_date = min(
            m.match_date
            for m in stage_matches
        )

        end_date = max(
            m.match_date
            for m in stage_matches
        )

        if start_date <= now <= end_date:
            return stage

    return "Group Stage"