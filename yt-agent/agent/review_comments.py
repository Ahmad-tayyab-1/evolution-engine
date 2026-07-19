"""
Run: python -m agent.review_comments
Interactively approve/reject/edit AI-drafted comment replies before posting.
"""
from dotenv import load_dotenv
load_dotenv()

from agent.db import get_session, CommentQueue  # noqa: E402
from agent import youtube_client as yt  # noqa: E402


def main():
    session = get_session()
    pending = session.query(CommentQueue).filter_by(status="pending").all()
    if not pending:
        print("No pending replies.")
        return

    for row in pending:
        print("\n" + "=" * 60)
        print(f"Comment by {row.author}: {row.text}")
        print(f"Draft reply: {row.draft_reply}")
        choice = input("[a]pprove / [e]dit / [r]eject / [s]kip? ").strip().lower()

        if choice == "a":
            yt.post_reply(row.youtube_comment_id, row.draft_reply)
            row.status = "posted"
        elif choice == "e":
            new_text = input("New reply text: ").strip()
            yt.post_reply(row.youtube_comment_id, new_text)
            row.draft_reply = new_text
            row.status = "posted"
        elif choice == "r":
            row.status = "rejected"
        # 's' = leave as pending

        session.commit()
    session.close()


if __name__ == "__main__":
    main()
