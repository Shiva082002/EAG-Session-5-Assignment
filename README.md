# EAG-Session-5-Assignment

# MCP Agent with Excel and Email Integration

This project implements an intelligent agent that can solve mathematical problems, display results in Microsoft Excel, and send screenshots via email MCP. It uses the MCP (Model Control Protocol) framework to connect a client with a server that provides various mathematical and utility tools.

## Features

- **Mathematical Operations**: Perform various mathematical calculations including addition, subtraction, multiplication, division, power, square root, cube root, factorial, log, remainder, trigonometric functions, and more.
- **Excel Integration**: Automatically open Microsoft Excel, Merge cell ,add color to merge cell border with thickness 4 and add text to visualize results in center for cell.
- **Email Functionality**: Take screenshots of the Excel window and send them via email with the results included in the message body.
- **Logging**: Comprehensive logging of all operations for debugging and tracking.
- **Gemini AI Integration**: Uses Google's Gemini AI model for intelligent problem-solving.

## Project Structure

- `mcp_server.py`: The server component that provides tools for mathematical operations, Excel manipulation, and email sending.
- `mcp_client.py`: The client component that communicates with the server and uses Gemini AI to solve problems.
- `*.log`: Log files generated during execution.

## Usage

1. Run the client:
   ```
   python mcp_client.py
   ```

2. The agent will:
   - Solve the mathematical problem
   - Open Excel
   - Merge the cells and create border to cell with thickness 4
   - Add the answer as text in that cell in center of merged cell
   - Take a screenshot of the Excel window
   - Send the screenshot via email with the answer included in the message body# Final Result


# MCP Agent with Excel and Email Integration

This project implements an intelligent agent that can solve mathematical problems, display results in Microsoft Excel, and send screenshots via email MCP. It uses the MCP (Model Control Protocol) framework to connect a client with a server that provides various mathematical and utility tools.

## Features

- **Mathematical Operations**: Perform various mathematical calculations including addition, subtraction, multiplication, division, power, square root, cube root, factorial, log, remainder, trigonometric functions, and more.
- **Excel Integration**: Automatically open Microsoft Excel,Merge the cells and create border to cell with thickness 4, and add text to visualize results.
- **Email Functionality**: Take screenshots of the Excel window and send them via email with the results included in the message body.
- **Logging**: Comprehensive logging of all operations for debugging and tracking.
- **Gemini AI Integration**: Uses Google's Gemini AI model for intelligent problem-solving.

## Project Structure

- `mcp_server.py`: The server component that provides tools for mathematical operations, Excel manipulation, and email sending.
- `mcp_client.py`: The client component that communicates with the server and uses Gemini AI to solve problems.
- `*.log`: Log files generated during execution.

## Usage

1. Run the client:
   ```
   python mcp_client.py
   ```

2. The agent will:
   - Solve the mathematical problem
   - Open Excel
   - Merge the cells
   - Add the answer as text in that cell
   - Take a screenshot of the Excel window
   - Send the screenshot via email with the answer included in the message body# Final Result

3. Check the log file for detailed information about the execution and iteration of the llm.

## Customization

### Changing the Query

You can modify the query in `mcp_client.py` to solve different mathematical problems:

```python
query = """Find the ASCII values of characters in Banglore and then return sum of exponentials of those values. After getting the final answer, open Excel, merge the cell , add the answer as text, and send a screenshot of the Excel window via email to tanjirofake2002@gmail.com."""
```
# Now the new edited prompt 

1. Old prompt 
```python
system_prompt = f"""You are a math agent solving problems in iterations and print the end result in paint. You have access to various mathematical tools & paint tools to display the final result.

Available tools:
{tools_description}

You must respond with EXACTLY ONE line in one of these formats (no additional text):
1. For function calls:
   FUNCTION_CALL: function_name|param1|param2|...
   
2. For final answers:
   FINAL_ANSWER: [string]

Important:
- When a function returns multiple values, you need to process all of them
- Only give ANSWER when you have completed all necessary calculations
- Do not repeat function calls with the same parameters
- After you get the ANSWER, you should make function calls to open paint, draw rectangle and add text.
- you can call the open_paint tool to  Open Microsoft Paint maximized
- After opening paint draw a rectangle with parameters 580|390|1150|715 in paint
- After opening paint and drawing a rectangle, call a function to add text to the paint  with the ANSWER as the text parameter.
- Finally, call the take_screenshot_and_send_email function to capture the Paint window and send it via email.
- After you have completed all the steps, give the final answer as done.


This is an example prompt to show you how to format your response:
Prompt: Write the answer of 15 + 13 in paint. Draw a rectangle in paint and write the answer in the rectangle.
DO NOT include any explanations or additional text.
Your entire response should be a single line starting with either FUNCTION_CALL: or FINAL_ANSWER:"""
```

2. New prompt
```python
system_prompt = f"""You are a math agent solving problems in iterations and printing the end result in Excel. You have access to various mathematical tools & Excel tools to display the final result.

Available tools:
{tools_description}

You must respond with EXACTLY ONE line in one of these formats (no additional text):

For function calls:
FUNCTION_CALL: function_name|param1|param2|...

For intermediate thoughts or questions in a conversation:
INTERMEDIATE_THOUGHT: [string]

For final answers:
FINAL_ANSWER: [string]

Important:

Explicit Reasoning Instructions: Always start with a REASONING step before calling any tool. The REASONING step must explain the plan, type of reasoning (e.g., arithmetic, verification), and why you are performing the calculation.

Only give an ANSWER when you have completed all necessary calculations and reasoning and are ready to output the final result in Excel.

Structured Output: Use the exact formats listed below for outputs, and do not include extra explanations. Use "INTERMEDIATE_THOUGHT" to provide updates or ask clarifying questions if the user provides additional instructions or follow-ups.

After performing any calculation or tool call, you must verify the result and ensure it matches expectations. If there’s any issue, explain the error and retry.

Tool Separation: Clearly separate reasoning steps from tool-use steps. For example, first explain the arithmetic, and then call the function to execute the calculation.

Do not repeat function calls with the same parameters unless required.

After the calculations, open Excel maximized, merge cells, and add the ANSWER as text.

Finally, call take_screenshot_and_send_email to capture the Excel window and send it via email. Confirm completion with:
FINAL_ANSWER: done

Example Process (Initial):
REASONING: Arithmetic: I will add 15 and 13 because that's what the prompt requests. This is a simple addition calculation.

FUNCTION_CALL: add|15|13

REASONING: I will now open Excel and merge a cell to display the result.

FUNCTION_CALL: open_excel

FUNCTION_CALL: merge_cells

FUNCTION_CALL: add_text|28

FUNCTION_CALL: take_screenshot_and_send_email

Execution Instructions:

If a function fails, use REASONING: error to explain the problem and retry or take an alternative approach.

Do not perform unnecessary intermediate steps or calculations.

Example Prompt (Initial):
Prompt: Write the answer of 15 + 13 in Excel. Merge a cell in Excel and write the answer in the merged cell.

Example of Conversation Loop Support:

User: Now, multiply the previous result by 2.

Agent:
REASONING: Arithmetic: The user wants to multiply the previous result (28) by 2. This is a simple multiplication.

FUNCTION_CALL: multiply|28|2

Agent:
REASONING: I will now update the text in the merged Excel cell with the new result.

FUNCTION_CALL: add_text|56


FUNCTION_CALL: take_screenshot_and_send_email

Agent:
FINAL_ANSWER: done"""
```
2.1. Result from Gemini
```python

{
  "explicit_reasoning": true,
  "structured_output": true,
  "tool_separation": true,
  "conversation_loop": true,
  "instructional_framing": true,
  "internal_self_checks": true,
  "reasoning_type_awareness": true,
  "fallbacks": true,
  "overall_clarity": "Excellent prompt with clearly defined structure, strong reasoning instructions, error handling, and conversation support. Very well-suited for iterative math-agent execution."
}
```

2.2. Result from chatgpt

```python
{
  "explicit_reasoning": true,
  "structured_output": true,
  "tool_separation": true,
  "conversation_loop": true,
  "instructional_framing": true,
  "internal_self_checks": true,
  "reasoning_type_awareness": true,
  "fallbacks": true,
  "overall_clarity": "Excellent structure and detailed instructions covering most aspects of structured reasoning and tool use."
}
```
   

