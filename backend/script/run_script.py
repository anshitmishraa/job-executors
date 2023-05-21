import os
import subprocess
import sh

from backend.models.job import JobType
from backend.helper import log


logger = log.setup_logging()


def run_script(result_job_type: JobType):
    # Specify the script content as a string
    script = result_job_type['script']

    # Get the current directory
    current_directory = os.getcwd()

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

    os.chmod(script_path, 0o755)

    try:
        # Execute the Bash script
        output = sh.bash(script_path)

        logger.info("Shell script output %s", str(output))

        return True
    except Exception as e:
        # Handle any exceptions or errors
        log.error("Error occurred:", str(e))
        return False
