# Job Executor Application

The Job Executor Application is a powerful tool that allows you to manage and execute various types of jobs efficiently. Whether it's running scripts, processing data, or handling event-based tasks, this application provides a reliable and scalable solution.

## Table of Contents

- [Job Executor Application](#job-executor-application)
  - [Table of Contents](#table-of-contents)
  - [Features](#features)
  - [Database Diagram](#database-diagram)
  - [API Documentation](#api-documentation)
  - [Installation](#installation)
  - [Usage](#usage)

## Features

- Job Execution: Execute different types of jobs based on their configuration and execution requirements.
- Script Execution: Run custom scripts or shell commands as jobs, allowing for flexible job execution.
- Data Processing: Perform data processing tasks specific to each job, such as reading data from files, processing it, and updating job statuses accordingly.
- Event-Based Jobs: Trigger jobs based on specific events, such as receiving notifications or signals, providing seamless integration with event-driven systems.
- Job Scheduling: Schedule jobs to run at specific times or intervals, allowing for automated and recurring job execution.
- Job Monitoring: Track and monitor the status of jobs, including their execution progress, completion status, and any potential errors or failures.
- User-Friendly Interface: Provide an intuitive and user-friendly interface for managing jobs, configuring job parameters, and monitoring job execution.

## Database Diagram

![Job Excutor Application](https://github.com/anshitmishraa/Job-Executors/assets/54078251/e2a520de-1a55-4e42-8ea5-361ed85bea15)

## API Documentation

The API documentation for this project can be found [here](https://job-executors-production.up.railway.app/docs).

## Installation

To install and run the Job Executor Application, follow these steps:

- Clone the repository: `https://github.com/anshitmishraa/Job-Executors.git`
- Navigate to the project directory: cd job-executor
- Set up a virtual environment (optional but recommended) by running the following command:
  - `python -m venv venv`
- Activate the virtual environment:
  - On Windows:
    - `venv\Scripts\activate`
  - On macOS/Linux:
    - `source venv/bin/activate`
- Install the required dependencies: pip install -r requirements.txt
- Configure the application settings, such as database connection details and API credentials, in the config.py file.
- Run the application: `uvicorn main:app --reload`
- Make sure to have Python and the necessary dependencies installed before running the application.

## Usage

- Access the Job Executor Application through the provided URL or local server address.
- Use the intuitive interface to create new jobs, configure their parameters, and set execution schedules.
- Monitor the status of running jobs, view execution logs, and handle any potential errors or failures.
- Optionally, configure event-based jobs to automatically trigger based on specific events or notifications.
