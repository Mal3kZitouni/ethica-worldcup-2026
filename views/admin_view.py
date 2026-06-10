import streamlit as st
from datetime import datetime, timezone

from services.match_service import load_matches
from services.result_service import save_match_result
from services.admin_service import create_match
from services.translations import tr


ALL_STAGES = [
    "Group Stage",
    "Round of 32",
    "Round of 16",
    "Quarter Finals",
    "Semi Finals",
    "3rd Place Match",
    "Final"
]


def show():

    if st.session_state.get("role") != "admin":
        st.error(tr("Access denied"))
        return

    st.title(f"⚙️ {tr('Admin Panel')}")

    tab1, tab2 = st.tabs(
        [
            f"🏆 {tr('Results')}",
            f"➕ {tr('Add Match')}"
        ]
    )

    # ==================================================
    # RESULTS TAB
    # ==================================================
    with tab1:

        st.subheader(
            f"🏆 {tr('Enter Match Results')}"
        )

        all_matches = load_matches()

        now = datetime.now(timezone.utc)

        pending_matches = []
        completed_matches = []

        for match in all_matches:

            match_date = match.match_date

            if match_date.tzinfo is None:
                match_date = match_date.replace(
                    tzinfo=timezone.utc
                )

            if (
                match.home_score is not None
                and match.away_score is not None
            ):
                completed_matches.append(match)
                continue

            if match_date <= now:
                pending_matches.append(match)

        # ----------------------------------------
        # MATCHES WAITING FOR RESULTS
        # ----------------------------------------
        if not pending_matches:

            st.info(
                tr(
                    "No finished matches are waiting for results."
                )
            )

        else:

            st.success(
                f"{len(pending_matches)} "
                f"{tr('finished matches awaiting results')}"
            )

            for match in pending_matches:

                st.markdown("---")

                st.markdown(
                    f"### {match.home_team} vs {match.away_team}"
                )

                st.caption(
                    f"🏆 {tr(match.stage)}"
                )

                st.caption(
                    f"📅 {match.match_date}"
                )

                st.caption(
                    f"🏟 {match.stadium} - {match.city}"
                )

                col1, col2 = st.columns(2)

                home_score = col1.number_input(
                    tr("Home Score"),
                    min_value=0,
                    max_value=20,
                    value=0,
                    key=f"home_{match.id}"
                )

                away_score = col2.number_input(
                    tr("Away Score"),
                    min_value=0,
                    max_value=20,
                    value=0,
                    key=f"away_{match.id}"
                )

                if st.button(
                    f"💾 {tr('Save Result')}",
                    key=f"save_{match.id}"
                ):

                    save_match_result(
                        match.id,
                        home_score,
                        away_score
                    )

                    st.success(
                        f"✅ {tr('Result saved')}: "
                        f"{match.home_team} "
                        f"{home_score}-{away_score} "
                        f"{match.away_team}"
                    )

                    st.rerun()

        # ----------------------------------------
        # COMPLETED MATCHES
        # ----------------------------------------
        with st.expander(
            f"✅ {tr('Completed Matches')} ({len(completed_matches)})"
        ):

            if not completed_matches:

                st.info(
                    tr("No completed matches yet.")
                )

            else:

                for match in completed_matches:

                    st.write(
                        f"{match.home_team} "
                        f"{match.home_score} - "
                        f"{match.away_score} "
                        f"{match.away_team}"
                    )

    # ==================================================
    # ADD MATCH TAB
    # ==================================================
    with tab2:

        st.subheader(
            f"➕ {tr('Create Match')}"
        )

        stage = st.selectbox(
            tr("Stage"),
            [tr(s) for s in ALL_STAGES]
        )

        stage_mapping = {
            tr(s): s
            for s in ALL_STAGES
        }

        home_team = st.text_input(
            tr("Home Team")
        )

        away_team = st.text_input(
            tr("Away Team")
        )

        match_date = st.date_input(
            tr("Date")
        )

        match_time = st.time_input(
            tr("Time")
        )

        stadium = st.text_input(
            tr("Stadium")
        )

        city = st.text_input(
            tr("City")
        )

        if st.button(
            f"➕ {tr('Create Match')}"
        ):

            if not home_team or not away_team:

                st.error(
                    tr(
                        "Home team and Away team are required."
                    )
                )

            elif home_team == away_team:

                st.error(
                    tr(
                        "Teams cannot be the same."
                    )
                )

            else:

                kickoff = datetime.combine(
                    match_date,
                    match_time
                )

                create_match(
                    stage=stage_mapping[stage],
                    home_team=home_team,
                    away_team=away_team,
                    match_date=kickoff,
                    stadium=stadium,
                    city=city
                )

                st.success(
                    f"✅ {tr('Match created successfully')}: "
                    f"{home_team} vs {away_team}"
                )

                st.rerun()