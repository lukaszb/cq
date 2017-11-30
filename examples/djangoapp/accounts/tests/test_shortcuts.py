from accounts.cqrs import app
from cq.contrib.django import shortcuts
from django.http import Http404
import pytest


@pytest.mark.django_db
def test_get_aggregate_or_404():
    with pytest.raises(Http404):
        shortcuts.get_aggregate_or_404(app.users, 'wrong_id')
