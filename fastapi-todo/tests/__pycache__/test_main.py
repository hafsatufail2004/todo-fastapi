import unittest
from unittest.mock import patch

from main import create_engine, create_todo_api,delete_todo_api, read_todo, update_todo_api, Session
from models import Todo

class TestMain(unittest.TestCase):

    @patch.object(Session, "exec")
    def test_read_todo(self, mock_exec):
        # Mock the session.exec call
        mock_exec.return_value.all.return_value = [Todo(id=1, content="Test todo")]

        # Call the read_todo function
        todo = read_todo()

        # Assert the expected todo is returned
        self.assertEqual(todo, [Todo(id=1, content="Test todo")])

    @patch.object(Session, "add")
    @patch.object(Session, "commit")
    @patch.object(Session, "refresh")
    def test_create_todo(self, mock_refresh, mock_commit, mock_add):
        # Create a test todo
        todo = Todo(content="New todo")

        # Call the create_todo function
        created_todo = create_todo_api(todo)

        # Assert the session methods were called with the expected arguments
        mock_add.assert_called_once_with(todo)
        mock_commit.assert_called_once()
        mock_refresh.assert_called_once_with(todo)

        # Assert the returned todo matches the created todo
        self.assertEqual(created_todo, todo)

    @patch.object(Session, "exec")
    @patch.object(Session, "delete")
    @patch.object(Session, "commit")
    def test_delete_todo(self, mock_commit, mock_delete, mock_exec):
        # Mock the session.exec call to return a todo
        mock_exec.return_value.one.return_value = Todo(id=1, content="todo to delete")

        # Call the delete_todo function
        response = delete_todo_api(Todo(id=1))

        # Assert the session methods were called with the expected arguments
        mock_delete.assert_called_once()
        mock_commit.assert_called_once()

        # Assert the expected response is returned
        self.assertEqual(response, "todo deleted ...!")

    @patch.object(Session, "exec")
    @patch.object(Session, "add")
    @patch.object(Session, "commit")
    @patch.object(Session, "refresh")
    def test_update_todo(self, mock_refresh, mock_commit, mock_add, mock_exec):
        # Mock the session.exec call to return a todo
        mock_exec.return_value.one.return_value = Todo(id=1, content="Old content")

        # Create an updated todo
        updated_todo = Todo(id=1, content="Updated content")

        # Call the update_todo function
        returned_todo = update_todo_api(updated_todo)

        # Assert the session methods were called with the expected arguments
        mock_add.assert_called_once()
        mock_commit.assert_called_once()
        mock_refresh.assert_called_once_with(returned_todo)

        # Assert the returned todo content is updated
        self.assertEqual(returned_todo.content, updated_todo.content)


if __name__ == "__main__":
    unittest.main()