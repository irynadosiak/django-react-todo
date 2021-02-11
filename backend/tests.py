from django.test import TestCase
from accounts.models import User
from backend.models import Todo


class TodoTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='test', email='test@example.com',
                                             password='12test21')

    def test_create_todo(self):
        Todo.objects.create(text='test', completed=False, owner=self.user)
        todo = Todo.objects.get(text='test')
        self.assertEqual(Todo.objects.count(), 1)
        # compare owner's email with provided
        self.assertEqual(todo.owner.email, 'test@example.com')
