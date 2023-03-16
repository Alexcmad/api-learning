import pyautogui as pg
import pprint
import requests
import json
title = "OWO"


def main():
    choice = pg.confirm(buttons=("Add", "View", "Exit"), text="View Todo list or Exit?", title=title)
    print(choice)
    data = view_todo_list()
    if choice == "View":
        for task in data:
            choice = pg.confirm(text=f"{task.get('description')}\n{task.get('completed')}",
                                buttons=("Complete", "Delete", "Next", "Back"), title=title)
            if choice == "Complete":
                id = task.get('id')
                op = requests.patch(f'http://127.0.0.1:8001/tasks/{id}')
                print(op.status_code)

            elif choice == "Delete":
                id = task.get('id')
                op = requests.delete(f'http://127.0.0.1:8001/tasks/{id}')
                print(op.status_code)

            elif choice == "Back":
                main()

        main()

    elif choice == "Add":
        task = pg.prompt(text="Enter the new Task", title=title)
        payload = {"description": task}
        op = requests.post("http://127.0.0.1:8001/tasks/", json=payload)
        print(op.status_code)
        pprint.pprint(op.json())

        main()

    elif choice == "Exit":
        exit()

def view_todo_list():
    data = requests.get('http://127.0.0.1:8001/tasks')
    data = data.json().get("data")
    # pprint.pprint(data)
    return data

main()