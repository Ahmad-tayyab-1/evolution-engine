"""
Run: python -m agent.genome_status
Shows the evolution history: control genome, any active candidate being
A/B tested, and retired genomes with their outcomes.
"""
from dotenv import load_dotenv
load_dotenv()

from agent.db import get_session, Genome  # noqa: E402


def main():
    session = get_session()
    genomes = session.query(Genome).order_by(Genome.version).all()

    for g in genomes:
        print("\n" + "=" * 70)
        print(f"v{g.version} [{g.status}] (parent: v{g.parent_version or '-'})")
        if g.mutation_rationale:
            print(f"  Rationale: {g.mutation_rationale}")
        print(f"  Videos produced: {g.videos_produced}")
        if g.avg_ctr is not None:
            print(f"  avg_ctr={g.avg_ctr:.4f}  avg_retention={g.avg_retention:.0f}s")
        print(f"  scenes: long={g.scene_count_long} shorts={g.scene_count_shorts}")
        print(f"  created={g.created_at}  promoted={g.promoted_at}  retired={g.retired_at}")

    session.close()


if __name__ == "__main__":
    main()
