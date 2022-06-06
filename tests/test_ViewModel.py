from todo_app.View_Class import ViewModel
from todo_app.data.task_class import Task


def test_View_Model_has_returned_only_Doing_Items():
    # Arrange
    items = [Task(id="123456", name="testcard 123", status="To Do"),
             Task(id="123457", name="testcard 456", status="Doing"),
             Task(id="123458", name="testcard 789", status="Done")]

    # Act
    item_view_model = ViewModel(items).doing_items

    # Assert
    assert len(item_view_model) == 1
    assert item_view_model[0][0].name == 'testcard 456'


def test_View_Model_has_returned_only_To_Do_Items():
    # Arrange
    items = [Task(id="123456", name="testcard 123", status="To Do"),
             Task(id="123457", name="testcard 456", status="Doing"),
             Task(id="123458", name="testcard 789", status="Done")]

    # Act
    item_view_model = ViewModel(items).toDo_items

    # Assert
    assert len(item_view_model) == 1
    assert item_view_model[0][0].name == 'testcard 123'


def test_View_Model_has_returned_only_Done_Items():
    # Arrange
    items = [Task(id="123456", name="testcard 123", status="To Do"),
             Task(id="123457", name="testcard 456", status="Doing"),
             Task(id="123458", name="testcard 789", status="Done")]

    # Act
    item_view_model = ViewModel(items).done_items

    # Assert
    assert len(item_view_model) == 1
    assert item_view_model[0][0].name == 'testcard 789'
