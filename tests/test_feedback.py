import pytest
from datetime import datetime
from models.feedback import Feedback
from storage.feedback_storage import FeedbackStorage
from repository.feedback_repo import FeedbackRepository
from config import SQL_DATA


@pytest.fixture
def feedback_storage(db):
    return FeedbackStorage(db, SQL_DATA)


@pytest.fixture
def feedback_repo(feedback_storage):
    return FeedbackRepository(feedback_storage)


def test_feedback_operations(feedback_repo, sample_user):
    # Создание отзыва
    feedback = feedback_repo.create(
        user_id=sample_user.id,
        text="Отличный сервис!",
        order_id=None
    )

    assert feedback.id > 0
    assert feedback.text == "Отличный сервис!"
    assert feedback.created_at is not None  # Проверяем что дата установлена
    assert isinstance(feedback.created_at, datetime)  # Проверяем тип