import unittest
from unittest.mock import patch

from sqlmodel_crud.main import create_engine, create_task, delete_task, read_task, update_task, Task, Session


class TestMain(unittest.TestCase):

    @patch.object(Session, "exec")
    def test_read_task(self, mock_exec):
        # Mock the session.exec call
        mock_exec.return_value.all.return_value = [Task(id=1, content="Test task")]

        # Call the read_task function
        tasks = read_task()

        # Assert the expected task is returned
        self.assertEqual(tasks, [Task(id=1, content="Test task")])

    @patch.object(Session, "add")
    @patch.object(Session, "commit")
    @patch.object(Session, "refresh")
    def test_create_task(self, mock_refresh, mock_commit, mock_add):
        # Create a test task
        task = Task(content="New task")

        # Call the create_task function
        created_task = create_task(task)

        # Assert the session methods were called with the expected arguments
        mock_add.assert_called_once_with(task)
        mock_commit.assert_called_once()
        mock_refresh.assert_called_once_with(task)

        # Assert the returned task matches the created task
        self.assertEqual(created_task, task)

    @patch.object(Session, "exec")
    @patch.object(Session, "delete")
    @patch.object(Session, "commit")
    def test_delete_task(self, mock_commit, mock_delete, mock_exec):
        # Mock the session.exec call to return a task
        mock_exec.return_value.one.return_value = Task(id=1, content="Task to delete")

        # Call the delete_task function
        response = delete_task(Task(id=1))

        # Assert the session methods were called with the expected arguments
        mock_delete.assert_called_once()
        mock_commit.assert_called_once()

        # Assert the expected response is returned
        self.assertEqual(response, "Task deleted ...!")

    @patch.object(Session, "exec")
    @patch.object(Session, "add")
    @patch.object(Session, "commit")
    @patch.object(Session, "refresh")
    def test_update_task(self, mock_refresh, mock_commit, mock_add, mock_exec):
        # Mock the session.exec call to return a task
        mock_exec.return_value.one.return_value = Task(id=1, content="Old content")

        # Create an updated task
        updated_task = Task(id=1, content="Updated content")

        # Call the update_task function
        returned_task = update_task(updated_task)

        # Assert the session methods were called with the expected arguments
        mock_add.assert_called_once()
        mock_commit.assert_called_once()
        mock_refresh.assert_called_once_with(returned_task)

        # Assert the returned task content is updated
        self.assertEqual(returned_task.content, updated_task.content)


if __name__ == "__main__":
    unittest.main()