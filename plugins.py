import yaml
import tools
import time

def execute_plugins(user_input, plugins, delay=0.2):
    
    user_input = user_input.lower().replace(" ", "")

    for pattern, commands in plugins.items():
        
        pattern = pattern.lower().replace(" ", "")
        if user_input.startswith(pattern):
            for command in commands:
                tool_name, *args = command.split(" ")
                tool = getattr(tools, tool_name)
                tool(*args)
                time.sleep(delay)
            return True
    return False
