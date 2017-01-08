from cq import entities


class Todo(entities.Entity):
    __slots__ = ('name', 'done')


@entities.register_mutator(Todo, 'Todo.Added')
def mutate_added(todo, event, data):
    todo.name = data['name']
    todo.done = False


@entities.register_mutator(Todo, 'Todo.Finished')
def mutate_finished(todo, event, data):
    todo.done = True


@entities.register_mutator(Todo, 'Todo.Reopened')
def mutate_reopened(todo, event, data):
    todo.done = False
