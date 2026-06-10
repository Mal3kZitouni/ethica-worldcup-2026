import pandas as pd
from collections import defaultdict
from services.match_service import load_matches


def get_group_tables():

    matches = load_matches()

    # -----------------------------------
    # 1. Extract all teams per group
    # -----------------------------------
    group_teams = defaultdict(set)

    for m in matches:
        group_teams[m.group_name].add(m.home_team)
        group_teams[m.group_name].add(m.away_team)

    # If no data
    if not group_teams:
        return {}

    # -----------------------------------
    # 2. Initialize standings
    # -----------------------------------
    tables = {}

    for group, teams in group_teams.items():
        tables[group] = {
            team: {
                "Team": team,
                "Played": 0,
                "Won": 0,
                "Drawn": 0,
                "Lost": 0,
                "Goals For": 0,
                "Goals Against": 0,
                "Goal Difference": 0,
                "Points": 0
            }
            for team in teams
        }

    # -----------------------------------
    # 3. Apply played matches
    # -----------------------------------
    for m in matches:
        if not getattr(m, "played", False):
            continue

        group = m.group_name
        home = m.home_team
        away = m.away_team
        hg = m.home_score
        ag = m.away_score

        ht = tables[group][home]
        at = tables[group][away]

        ht["Played"] += 1
        at["Played"] += 1

        ht["Goals For"] += hg
        ht["Goals Against"] += ag

        at["Goals For"] += ag
        at["Goals Against"] += hg

        if hg > ag:
            ht["Won"] += 1
            at["Lost"] += 1
            ht["Points"] += 3
        elif hg < ag:
            at["Won"] += 1
            ht["Lost"] += 1
            at["Points"] += 3
        else:
            ht["Drawn"] += 1
            at["Drawn"] += 1
            ht["Points"] += 1
            at["Points"] += 1

    # -----------------------------------
    # 4. Final dataframe
    # -----------------------------------
    final_tables = {}

    for group, teams in tables.items():
        rows = []

        for team, stats in teams.items():
            stats["Goal Difference"] = stats["Goals For"] - stats["Goals Against"]
            rows.append(stats)

        df = pd.DataFrame(rows)

        df = df.sort_values(
            by=["Points", "Goal Difference", "Goals For"],
            ascending=[False, False, False]
        )

        final_tables[group] = df

    return final_tables