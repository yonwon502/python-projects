from main import TodoApp
import os
import json

def test_todo_app():
    # Setup: ensure tasks.json is clean
    if os.path.exists("tasks.json"):
        os.remove("tasks.json")
    
    # Initialize app (without mainloop)
    app = TodoApp()
    
    # Test Add
    app.task_entry.insert(0, "Test Task")
    app.add_task()
    assert len(app.tasks) == 1
    assert app.tasks[0]["text"] == "Test Task"
    assert app.tasks[0]["completed"] == False
    
    # Test Toggle
    app.toggle_task(0)
    assert app.tasks[0]["completed"] == True
    
    # Test Delete
    app.delete_task(0)
    assert len(app.tasks) == 0
    
    # Test Persistence
    app.task_entry.insert(0, "Persistent Task")
    app.add_task()
    
    # Create a new instance to check loading
    app2 = TodoApp()
    assert len(app2.tasks) == 1
    assert app2.tasks[0]["text"] == "Persistent Task"
    
    print("All tests passed!")

if __name__ == "__main__":
    test_todo_app()
