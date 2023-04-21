# ToDo_list_v2
# To-Do List App

The To-Do List App is a command-line application that allows users to manage their to-do lists and tasks. Each user can have many to-do lists, and each to-do list can have many tasks. All of the to-do lists and tasks are specific to the user.

# Installation
To use the To-Do List App, you will need to install pipenv. Once pipenv is installed, you can clone the repository and install the dependencies by running the following commands:

cd to-do-list-app

pipenv install

pipenv shell



# Overview
Once you have installed the dependencies and activated the virtual environment, you can use the To-Do List App to manage your to-do lists and tasks. Here is an overview of the available commands:

Get user by ID: Retrieve a user by their ID.

Get all users: Retrieve a list of all users.

Create to-do list: Create a new to-do list for the current user.

Get all to-do lists: Retrieve a list of all to-do lists for the current user.

Delete to-do list: Delete a to-do list for the current user.

Create task: Create a new task for a to-do list.

Get tasks: Retrieve a list of all tasks for the current user.

Exit: Exit the application.

# Detailed Explanation of Commands


## 1. Get user by ID
This command retrieves a user by their ID. You will be prompted to enter the ID of the user you wish to retrieve. If the user exists, their information will be displayed.

## 2. Get all users
This command retrieves a list of all users. If there are no users, a message will be displayed indicating that there are no users.

## 3. Create to-do list
This command creates a new to-do list for the current user. You will be prompted to enter the name of the to-do list. If the to-do list is successfully created, a message will be displayed indicating that the to-do list has been created.

## 4. Get all to-do lists
This command retrieves a list of all to-do lists for the current user. If there are no to-do lists, a message will be displayed indicating that there are no to-do lists.

## 5. Delete to-do list
This command deletes a to-do list for the current user. You will be prompted to enter the ID of the to-do list you wish to delete. If the to-do list is successfully deleted, a message will be displayed indicating that the to-do list has been deleted.

## 6. Create task
This command creates a new task for a to-do list. You will be prompted to enter the name of the task, the ID of the to-do list you wish to add the task to, and the due date of the task. If the task is successfully created, a message will be displayed indicating that the task has been created.

## 7. Get tasks
This command retrieves a list of all tasks for the current user. If there are no tasks, a message will be displayed indicating that there are no tasks.

## 0. Exit
This command exits the application.