"""
Run: python -m agent.niche_status
Shows discovery phase progress and per-niche performance so far.
"""
from dotenv import load_dotenv
load_dotenv()

from agent.db import get_session, StrategyState, NicheScore  # noqa: E402


def main():
    session = get_session()
    state = session.query(StrategyState).first()

    if not state:
        print("No strategy state yet - agent hasn't run a cycle.")
        return

    print(f"Phase: {state.phase}")
    if state.phase == "niche_discovery":
        print(f"Discovery started: {state.discovery_started_at}")
        print(f"Discovery ends:    {state.discovery_ends_at}")
    else:
        print(f"Locked niche: {state.locked_niche}")
    if state.notes:
        print(f"Notes: {state.notes}")

    print("\nPer-niche results so far:")
    scores = session.query(NicheScore).order_by(NicheScore.avg_ctr.desc()).all()
    for s in scores:
        print(
            f"  {s.niche:<25} opportunity={s.opportunity_score:.2f}  "
            f"avg_ctr={s.avg_ctr:.4f}  avg_retention={s.avg_retention:.0f}s  "
            f"n={s.videos_count}"
        )

    session.close()


if __name__ == "__main__":
    main()
