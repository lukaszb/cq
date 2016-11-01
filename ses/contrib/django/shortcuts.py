from django.http import Http404


def get_entity_or_404(repo, entity_id):
    try:
        return repo.get_entity(entity_id)
    except repo.DoesNotExist:
        raise Http404
