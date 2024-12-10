from models.base import get_db_session
from models.progress_model import Progress

def test_progress_entries():
    with get_db_session() as session:
        all_progress = session.query(Progress).all()
        if not all_progress:
            print("Нет записей о прогрессе.")
        else:
            for progress in all_progress:
                print(f"User ID: {progress.user_id}, Weight: {progress.weight}, Date: {progress.date}")

if __name__ == "__main__":
    test_progress_entries()
