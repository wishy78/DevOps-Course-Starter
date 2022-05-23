from asyncio import tasks
from unicodedata import name
from todo_app.View_Class import ViewModel
from todo_app.data.task_class import Task

def test_View_Model_has_returned_only_Doing_Items():

    # Arrange
    items = []
    items.append(Task(id="123456",name="testcard 123",status="To do"))
    items.append(Task(id="123457",name="testcard 456",status="Doing"))
    items.append(Task(id="123458",name="testcard 789",status="Done"))
    

    # Act
    item_view_model = ViewModel(items).doing_items

    # Assert
    assert item_view_model.count == 1
    assert 'Test card 456' in item_view_model

def test_View_Model_has_returned_only_To_Do_Items():

    # Arrange
    items = []
    items.append(Task(id="123456",name="testcard 123",status="To do"))
    items.append(Task(id="123457",name="testcard 456",status="Doing"))
    items.append(Task(id="123458",name="testcard 789",status="Done"))
    

    # Act
    item_view_model = ViewModel(items).toDo_items

    # Assert
    assert item_view_model.count == 1
    assert 'Test card 123' in item_view_model

def test_View_Model_has_returned_only_Done_Items():

    # Arrange
    items = []
    items.append(Task(id="123456",name="testcard 123",status="To do"))
    items.append(Task(id="123457",name="testcard 456",status="Doing"))
    items.append(Task(id="123458",name="testcard 789",status="Done"))
    

    # Act
    item_view_model = ViewModel(items).done_items

    # Assert
    assert item_view_model.count == 1
    assert 'Test card 789' in item_view_model