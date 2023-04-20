import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base, User, TodoList, Task

engine = create_engine('sqlite:///todo.db')
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()

current_user = None


def login(username):
    global current_user
    user = session.query(User).filter_by(username=username).first()
    if user:
        print(f'Welcome back {user.username}!')
        print("")
    else:
        user = User(username=username)
        session.add(user)
        session.commit()
        print(f'Welcome {user.username}!')
        print("")
    current_user = user


def get_user_by_id(id):
    global current_user
    user = session.query(User).filter_by(id=id).first()
    if user:
        current_user = user
        return current_user
    else:
        return None


def get_all_users():
    return session.query(User).all()


def create_todo_list(name, user_id):
    todo_list = TodoList(name=name, user_id=user_id)
    session.add(todo_list)
    session.commit()
    return todo_list


def get_todo_lists_for_user(user_id):
    print(f"Here are {current_user.username}'s ToDo-Lists")
    return session.query(TodoList).filter_by(user_id=user_id).all()



def delete_todo_list(todo_list_id):
    todo_list = session.query(TodoList).filter_by(id=todo_list_id).first()
    if todo_list:
        session.delete(todo_list)
        session.commit()
        print(f'Todo list {todo_list.name} deleted')
    else:
        print('Todo list not found')


def create_task(description, todo_list_id):
    todo_list = session.query(TodoList).filter_by(id=todo_list_id).first()
    if todo_list:
        task = Task(description=description, todo_list_id=todo_list_id)
        session.add(task)
        session.commit()
        print(f'Task "{task.description}" added to todo list "{todo_list.name}"')
    else:
        print('Todo list not found')

def get_tasks_for_user(user_id):
    if not current_user:
        print('No current user set')
        return
    todo_lists = get_todo_lists_for_user(user_id)
    if not todo_lists:
        print('No todo lists found')
        return
    for todo_list in todo_lists:
        print(f'Todo list: {todo_list.name}')
        tasks = session.query(Task).filter_by(todo_list_id=todo_list.id).all()
        if tasks:
            for task in tasks:
                print(f'{task.id} | {task.description}')
        else:
            print('No tasks found')
        print()




def run_todo_list_app():
    os.system('clear') 
    print('Todo List App')
    while True:
        if current_user:
            print(f'Logged in as {current_user.username}')
            print("")
            print('1. Get user by ID')
            print('2. Get all users')
            print('3. Create todo list')
            print('4. Get all todo lists for the current user')
            print('5. Delete todo list')
            print('6. Create task')
            print('0. Exit')
        else:
            print('1. Login')
            print('0. Exit')

        choice = input('Enter choice: ')

        if choice == '1':
            if not current_user:
                username = input('Enter username: ')
                print("")
                login(username)
            else:
                id = input('Enter user ID: ')
                user = get_user_by_id(id)
                if user:
                    print(f'User: {user.username}')
                else:
                    print('User not found')
                input('Press Enter to continue...')
        elif choice == '2':
            users = get_all_users()
            for user in users:
                print(f'{user.id} | {user.username}')
            input('Press Enter to continue...')
        elif choice == '3':
            name = input('Enter todo list name: ')
            user_id = current_user.id if current_user else input('Enter user ID: ')
            create_todo_list(name, user_id)
            print('Todo list created')
        elif choice == '4':
            if not current_user:
                print('No current user set')
            else:
                todo_lists = get_todo_lists_for_user(current_user.id)
                for todo_list in todo_lists:
                    print(f'{todo_list.id} | {todo_list.name}')
            input('Press Enter to continue...')
        elif choice == '5':
            if not current_user:
                print('No current user set')
            else:
                todo_lists = get_todo_lists_for_user(current_user.id)
                print('Todo lists:')
                for todo_list in todo_lists:
                    print(f'{todo_list.id} | {todo_list.name}')
                todo_list_id = input('Enter todo list ID to delete: ')
                delete_todo_list(todo_list_id)
            input('Press Enter to continue...')
        elif choice == '6':
            if not current_user:
                print('No current user set')
            else:
                todo_lists = get_todo_lists_for_user(current_user.id)
                if not todo_lists:
                    print('No Todo lists found')
                    run_todo_list_app()

                else:
                    for todo_list in todo_lists:
                        print(f'{todo_list.id} | {todo_list.name}')
                todo_list_id = input('Enter the ID of the Todo list to add the task to: ')

                todo_list = session.query(TodoList).filter_by(id=todo_list_id).first()
                if not todo_list:
                    print('Todo list not found')
                else:
                    description = input('Enter task description: ')
                    task = Task(description=description, todo_list_id=todo_list.id)
                    session.add(task)
                    session.commit()
                    print(f'Task "{description}" created and added to Todo list "{todo_list.name}"')

        
        elif choice == '0':
            break


        else:
            print('Invalid choice')
            input('Press Enter to continue...')


if __name__ == '__main__':
    run_todo_list_app()
