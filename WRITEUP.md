# 2025-08-26

Ok starting the writeup here. So the general idea behind this app is to use an LLM server as a tool calling agent, and use it to drive UI automation PURELY through our voice.

The motivation of this app is that I have a friend who has been going through some wrist pains and consequently typing on his computer has been difficult. I want to create a way for him to easily use his computer entirely by voice. 

The general flow is as follows:

	1. Speech to text on the main thread
	2. Package the command in a prompt to the LLM (containing tool descriptions)
	3. send the LLM an initial screenshot along with the initial prompt and user command
	4. The LLM calls a tool or series of tools in order to accomplish a task
	5. The tool call is executed via pyautogui
	6. a new screenshot is sent to the LLM along with the conversation history (including the original prompt, the original command, and all previous (state, action) pairs
	7. 
