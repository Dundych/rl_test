from subprocess import Popen, PIPE, STDOUT

def run_cmd(cmd):
    """
    Execute linux bash script. Wait for it complete and get result of execution (output, return code, error message)

    Args:
        cmd (str): shell command for execute

    Returns:
        tuple(iterator, int, string): 
            output - stdout has been converted to iterator (str)
            return_value - error code (0, 1, 2)
            error_message - (str or None)
    """
    p = Popen(cmd, shell=True, stdin=PIPE, stdout=PIPE, stderr=STDOUT, close_fds=True)
    lines = iter(p.stdout.readline, b'')
    lines = (line.decode('utf-8') for line in lines if line)
    retval = p.wait()
    return lines, retval, p.stderr

def run_cmd_with_interaction(cmd, user_input):
    """
    Execute linux bash script. Input answer

    Args:
        cmd (str): shell command for execute
        user_input (str): user type 

    Returns:
        tuple(string, int, string): 
            output - stdout
            error_message - (str or None)
    """
    p = Popen(cmd, shell=True, stdin=PIPE, stdout=PIPE, stderr=STDOUT, close_fds=True)
    output, error_message = p.communicate(input = user_input.encode()) 
    return output, error_message
