import os
import subprocess
from models.job import JobType
from helper import log


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
        # Make the script file executable
        subprocess.run(['chmod', '+x', script_path], check=True)
    except subprocess.CalledProcessError as e:
        logger.error(
            "Error occurred while making the script file executable: %s", str(e))
        return False

    # Execute the shell script
    try:
        subprocess.run(['bash', script_path], check=True)
        logger.info("Shell script executed successfully.")

        return True
    except subprocess.CalledProcessError as e:
        logger.error("Error executing the shell script: %s", str(e))

        return False
