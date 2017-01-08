from cq import aggregates


class Todo(aggregates.Aggregate):
    __slots__ = ('name', 'done')


@aggregates.register_mutator(Todo, 'Todo.Added')
def mutate_added(todo, event, data):
    todo.name = data['name']
    todo.done = False


@aggregates.register_mutator(Todo, 'Todo.Finished')
def mutate_finished(todo, event, data):
    todo.done = True


@aggregates.register_mutator(Todo, 'Todo.Reopened')
def mutate_reopened(todo, event, data):
    todo.done = False
