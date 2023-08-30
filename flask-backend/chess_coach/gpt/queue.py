import os
import time
from datetime import datetime
from uuid import uuid4

task_count = 0

def clear_old_tasks():
    task_folder = "tasks"
    now = time.mktime(datetime.now().timetuple())
    twenty_minutes_ago = now - (20 * 60)  # 20 minutes ago

    for task_file in os.listdir(task_folder):
        task_file_path = os.path.join(task_folder, task_file)
        file_time = os.path.getmtime(task_file_path)

        if file_time < twenty_minutes_ago:
            os.remove(task_file_path)
            print(f"Removed old task file: {task_file}")

def new_task():
    task_id = str(uuid4())
    timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
    file_name = f"{task_id}_{timestamp}"

    with open(f"tasks/{file_name}", "w") as f:
        # create empty file
        pass

    task_count += 1
    if task_count % 20 == 0:
        clear_old_tasks()

    return file_name
