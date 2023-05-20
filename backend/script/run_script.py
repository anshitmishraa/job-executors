import os
import subprocess

from backend.models.job import JobType
from backend.helper import log


logger = log.setup_logging()


def run_script(result_job_type: JobType):
    # Specify the script content as a string
    script = result_job_type['script']

    # Get the current directory
    current_directory = os.getcwd() + '\script'

    # Specify the script file name
    script_filename = 'script.sh'

    # Create the script file path
    script_path = os.path.join(current_directory, script_filename)

    try:
        # Save the script content to the file
        with open(script_path, 'w') as file:
            file.write(script)
    except Exception as e:
        logger.error(
            "Error occurred while writing the script file: %s", str(e))
        return False

    logger.info("Shell script has been created on path %s", str(script_path))

    try:
        # Execute the shell script
        subprocess.run(['venv\Scripts\python', script_path],
                       check=True, shell=True)

    except subprocess.CalledProcessError as e:
        logger.error(
            "Error occurred while executing the script file executable: %s", str(e))
        return False
