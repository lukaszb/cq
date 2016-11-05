from ses import entities


class Todo(entities.Entity):
    __slots__ = ('name', 'done')


@entities.register_mutator(Todo, 'Todo.Added')
def mutate_added(todo, data):
    todo.name = data['name']
    todo.done = False


@entities.register_mutator(Todo, 'Todo.Finished')
def mutate_finished(todo, data):
    todo.done = True


@entities.register_mutator(Todo, 'Todo.Reopened')
def mutate_reopened(todo, data):
    todo.done = False
