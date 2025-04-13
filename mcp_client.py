import os
from dotenv import load_dotenv
from mcp import ClientSession, StdioServerParameters, types
from mcp.client.stdio import stdio_client
import asyncio
from google import genai
from concurrent.futures import TimeoutError
from functools import partial
import logging
import datetime

# Load environment variables from .env file
load_dotenv()

# Set up logging
log_filename = f"mcp_agent_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.log"
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(log_filename),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# Access your API key and initialize Gemini client correctly
api_key = os.getenv("GEMINI_API_KEY")
client = genai.Client(api_key=api_key)

max_iterations = 10
last_response = None
iteration = 0
iteration_response = []

async def generate_with_timeout(client, prompt, timeout=10):
    """Generate content with a timeout"""
    logger.info("Starting LLM generation...")
    try:
        # Convert the synchronous generate_content call to run in a thread
        loop = asyncio.get_event_loop()
        response = await asyncio.wait_for(
            loop.run_in_executor(
                None, 
                lambda: client.models.generate_content(
                    model="gemini-2.0-flash",
                    contents=prompt
                )
            ),
            timeout=timeout
        )
        logger.info("LLM generation completed")
        return response
    except TimeoutError:
        logger.error("LLM generation timed out!")
        raise
    except Exception as e:
        logger.error(f"Error in LLM generation: {e}")
        raise

def reset_state():
    """Reset all global variables to their initial state"""
    global last_response, iteration, iteration_response
    last_response = None
    iteration = 0
    iteration_response = []
    logger.info("State reset")

async def main():
    reset_state()  # Reset at the start of main
    logger.info("Starting main execution...")
    try:
        # Create a single MCP server connection
        logger.info("Establishing connection to MCP server...")
        server_params = StdioServerParameters(
            command="python",
            args=["mcp_server.py"]
        )

        async with stdio_client(server_params) as (read, write):
            logger.info("Connection established, creating session...")
            async with ClientSession(read, write) as session:
                logger.info("Session created, initializing...")
                await session.initialize()
                
                # Get available tools
                logger.info("Requesting tool list...")
                tools_result = await session.list_tools()
                tools = tools_result.tools
                logger.info(f"Successfully retrieved {len(tools)} tools")

                # Create system prompt with available tools
                logger.info("Creating system prompt...")
                logger.info(f"Number of tools: {len(tools)}")
                
                try:
                    # First, let's inspect what a tool object looks like
                    # if tools:
                    #     print(f"First tool properties: {dir(tools[0])}")
                    #     print(f"First tool example: {tools[0]}")
                    
                    tools_description = []
                    for i, tool in enumerate(tools):
                        try:
                            # Get tool properties
                            params = tool.inputSchema
                            desc = getattr(tool, 'description', 'No description available')
                            name = getattr(tool, 'name', f'tool_{i}')
                            
                            # Format the input schema in a more readable way
                            if 'properties' in params:
                                param_details = []
                                for param_name, param_info in params['properties'].items():
                                    param_type = param_info.get('type', 'unknown')
                                    param_details.append(f"{param_name}: {param_type}")
                                params_str = ', '.join(param_details)
                            else:
                                params_str = 'no parameters'

                            tool_desc = f"{i+1}. {name}({params_str}) - {desc}"
                            tools_description.append(tool_desc)
                            logger.debug(f"Added description for tool: {tool_desc}")
                        except Exception as e:
                            logger.error(f"Error processing tool {i}: {e}")
                            tools_description.append(f"{i+1}. Error processing tool")
                    
                    tools_description = "\n".join(tools_description)
                    logger.info("Successfully created tools description")
                except Exception as e:
                    logger.error(f"Error creating tools description: {e}")
                    tools_description = "Error loading tools"
                
                logger.info("Created system prompt...")
                
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

                query = """Find the ASCII values of characters in Banglore and then return sum of exponentials of those values. After getting the final answer, open Excel, merge the cell , add the answer as text, and send a screenshot of the Excel window via email to tanjirofake2002@gmail.com."""
                logger.info(f"Query: {query}")
                logger.info("Starting iteration loop...")
                
                # Use global iteration variables
                global iteration, last_response
                
                while iteration < max_iterations:
                    logger.info(f"\n--- Iteration {iteration + 1} ---")
                    if last_response is None:
                        current_query = query
                    else:
                        current_query = current_query + "\n\n" + " ".join(iteration_response)
                        current_query = current_query + "  What should I do next?"

                    # Get model's response with timeout
                    logger.info("Preparing to generate LLM response...")
                    prompt = f"{system_prompt}\n\nQuery: {current_query}"
                    try:
                        response = await generate_with_timeout(client, prompt)
                        response_text = response.text.strip()
                        logger.info(f"LLM Response: {response_text}")
                        
                        # Find the FUNCTION_CALL line in the response
                        for line in response_text.split('\n'):
                            line = line.strip()
                            if line.startswith("FUNCTION_CALL:"):
                                response_text = line
                                break
                        
                    except Exception as e:
                        logger.error(f"Failed to get LLM response: {e}")
                        break


                    if response_text.startswith("FUNCTION_CALL:"):
                        _, function_info = response_text.split(":", 1)
                        parts = [p.strip() for p in function_info.split("|")]
                        func_name, params = parts[0], parts[1:]
                        
                        logger.debug(f"Raw function info: {function_info}")
                        logger.debug(f"Split parts: {parts}")
                        logger.debug(f"Function name: {func_name}")
                        logger.debug(f"Raw parameters: {params}")
                        
                        try:
                            # Find the matching tool to get its input schema
                            tool = next((t for t in tools if t.name == func_name), None)
                            if not tool:
                                logger.error(f"Available tools: {[t.name for t in tools]}")
                                raise ValueError(f"Unknown tool: {func_name}")

                            logger.debug(f"Found tool: {tool.name}")
                            logger.debug(f"Tool schema: {tool.inputSchema}")

                            # Prepare arguments according to the tool's input schema
                            arguments = {}
                            schema_properties = tool.inputSchema.get('properties', {})
                            logger.debug(f"Schema properties: {schema_properties}")

                            for param_name, param_info in schema_properties.items():
                                if not params:  # Check if we have enough parameters
                                    raise ValueError(f"Not enough parameters provided for {func_name}")
                                    
                                value = params.pop(0)  # Get and remove the first parameter
                                param_type = param_info.get('type', 'string')
                                
                                logger.debug(f"Converting parameter {param_name} with value {value} to type {param_type}")
                                
                                # Convert the value to the correct type based on the schema
                                if param_type == 'integer':
                                    arguments[param_name] = int(value)
                                elif param_type == 'number':
                                    arguments[param_name] = float(value)
                                elif param_type == 'array':
                                    # Handle array input
                                    if isinstance(value, str):
                                        value = value.strip('[]').split(',')
                                    arguments[param_name] = [int(x.strip()) for x in value]
                                else:
                                    arguments[param_name] = str(value)

                            logger.debug(f"Final arguments: {arguments}")
                            logger.info(f"Calling tool {func_name}")
                            
                            result = await session.call_tool(func_name, arguments=arguments)
                            logger.debug(f"Raw result: {result}")
                            
                            # Get the full result content
                            if hasattr(result, 'content'):
                                logger.debug("Result has content attribute")
                                # Handle multiple content items
                                if isinstance(result.content, list):
                                    iteration_result = [
                                        item.text if hasattr(item, 'text') else str(item)
                                        for item in result.content
                                    ]
                                else:
                                    iteration_result = str(result.content)
                            else:
                                logger.debug("Result has no content attribute")
                                iteration_result = str(result)
                                
                            logger.debug(f"Final iteration result: {iteration_result}")
                            
                            # Format the response based on result type
                            if isinstance(iteration_result, list):
                                result_str = f"[{', '.join(iteration_result)}]"
                            else:
                                result_str = str(iteration_result)
                            
                            iteration_response.append(
                                f"In the {iteration + 1} iteration you called {func_name} with {arguments} parameters, "
                                f"and the function returned {result_str}."
                            )
                            last_response = iteration_result
                            logger.info(f"Tool {func_name} executed successfully with result: {result_str}")

                        except Exception as e:
                            logger.error(f"Error details: {str(e)}")
                            logger.error(f"Error type: {type(e)}")
                            import traceback
                            logger.error(traceback.format_exc())
                            iteration_response.append(f"Error in iteration {iteration + 1}: {str(e)}")
                            break

                    elif response_text.startswith("FINAL_ANSWER:"):
                        logger.info("\n=== Agent Execution Complete ===")
                        logger.info(f"Final answer: {response_text}")
                        # The agent will handle Paint operations itself, so we don't need to do anything here
                        # Just break out of the loop
                        break

                    iteration += 1

    except Exception as e:
        logger.error(f"Error in main execution: {e}")
        import traceback
        logger.error(traceback.format_exc())
    finally:
        reset_state()  # Reset at the end of main
        logger.info(f"Execution completed. Log file: {log_filename}")

if __name__ == "__main__":
    asyncio.run(main())
    
    
