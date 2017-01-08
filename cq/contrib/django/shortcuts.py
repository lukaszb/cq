from django.http import Http404


def get_aggregate_or_404(repo, aggregate_id):
    try:
        return repo.get_aggregate(aggregate_id)
    except repo.DoesNotExist:
        raise Http404
