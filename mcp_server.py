# basic import 
from mcp.server.fastmcp import FastMCP, Image
from mcp.server.fastmcp.prompts import base
from mcp.types import TextContent
from mcp import types
from PIL import Image as PILImage
import math
import sys
from pywinauto.application import Application
import win32gui
import win32con
import time
from win32api import GetSystemMetrics
import pyautogui
import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.image import MIMEImage
from dotenv import load_dotenv
import io
import win32com.client as win32

# instantiate an MCP server client
mcp = FastMCP("Calculator")

# Load environment variables
load_dotenv()

# DEFINE TOOLS

#addition tool
@mcp.tool()
def add(a: int, b: int) -> int:
    """Add two numbers"""
    print("CALLED: add(a: int, b: int) -> int:")
    return int(a + b)

@mcp.tool()
def add_list(l: list) -> int:
    """Add all numbers in a list"""
    print("CALLED: add(l: list) -> int:")
    return sum(l)

# subtraction tool
@mcp.tool()
def subtract(a: int, b: int) -> int:
    """Subtract two numbers"""
    print("CALLED: subtract(a: int, b: int) -> int:")
    return int(a - b)

# multiplication tool
@mcp.tool()
def multiply(a: int, b: int) -> int:
    """Multiply two numbers"""
    print("CALLED: multiply(a: int, b: int) -> int:")
    return int(a * b)

#  division tool
@mcp.tool() 
def divide(a: int, b: int) -> float:
    """Divide two numbers"""
    print("CALLED: divide(a: int, b: int) -> float:")
    return float(a / b)

# power tool
@mcp.tool()
def power(a: int, b: int) -> int:
    """Power of two numbers"""
    print("CALLED: power(a: int, b: int) -> int:")
    return int(a ** b)

# square root tool
@mcp.tool()
def sqrt(a: int) -> float:
    """Square root of a number"""
    print("CALLED: sqrt(a: int) -> float:")
    return float(a ** 0.5)

# cube root tool
@mcp.tool()
def cbrt(a: int) -> float:
    """Cube root of a number"""
    print("CALLED: cbrt(a: int) -> float:")
    return float(a ** (1/3))

# factorial tool
@mcp.tool()
def factorial(a: int) -> int:
    """factorial of a number"""
    print("CALLED: factorial(a: int) -> int:")
    return int(math.factorial(a))

# log tool
@mcp.tool()
def log(a: int) -> float:
    """log of a number"""
    print("CALLED: log(a: int) -> float:")
    return float(math.log(a))

# remainder tool
@mcp.tool()
def remainder(a: int, b: int) -> int:
    """remainder of two numbers divison"""
    print("CALLED: remainder(a: int, b: int) -> int:")
    return int(a % b)

# sin tool
@mcp.tool()
def sin(a: int) -> float:
    """sin of a number"""
    print("CALLED: sin(a: int) -> float:")
    return float(math.sin(a))

# cos tool
@mcp.tool()
def cos(a: int) -> float:
    """cos of a number"""
    print("CALLED: cos(a: int) -> float:")
    return float(math.cos(a))

# tan tool
@mcp.tool()
def tan(a: int) -> float:
    """tan of a number"""
    print("CALLED: tan(a: int) -> float:")
    return float(math.tan(a))

# mine tool
@mcp.tool()
def mine(a: int, b: int) -> int:
    """special mining tool"""
    print("CALLED: mine(a: int, b: int) -> int:")
    return int(a - b - b)

@mcp.tool()
def create_thumbnail(image_path: str) -> Image:
    """Create a thumbnail from an image"""
    print("CALLED: create_thumbnail(image_path: str) -> Image:")
    img = PILImage.open(image_path)
    img.thumbnail((100, 100))
    return Image(data=img.tobytes(), format="png")

@mcp.tool()
def strings_to_chars_to_int(string: str) -> list[int]:
    """Return the ASCII values of the characters in a word"""
    print("CALLED: strings_to_chars_to_int(string: str) -> list[int]:")
    return [int(ord(char)) for char in string]

@mcp.tool()
def int_list_to_exponential_sum(int_list: list) -> float:
    """Return sum of exponentials of numbers in a list"""
    print("CALLED: int_list_to_exponential_sum(int_list: list) -> float:")
    return sum(math.exp(i) for i in int_list)

@mcp.tool()
def fibonacci_numbers(n: int) -> list:
    """Return the first n Fibonacci Numbers"""
    print("CALLED: fibonacci_numbers(n: int) -> list:")
    if n <= 0:
        return []
    fib_sequence = [0, 1]
    for _ in range(2, n):
        fib_sequence.append(fib_sequence[-1] + fib_sequence[-2])
    return fib_sequence[:n]

        
@mcp.tool()
async def open_excel() -> dict:
    """Open Microsoft Excel"""
    global excel_app
    try:
        excel_app = Application().start(r'C:\Program Files\Microsoft Office\root\Office16\EXCEL.EXE')
        time.sleep(3)
        excel_app = win32.Dispatch("Excel.Application")
        excel_app.Visible = True
        excel_app.Workbooks.Add()  # Create a new blank workbook
        return {
            "content": [
                TextContent(
                    type="text",
                    text="Excel opened successfully."
                )
            ]
        }
    except Exception as e:
        return {
            "content": [
                TextContent(
                    type="text",
                    text=f"Error opening Excel: {str(e)}"
                )
            ]
        }

@mcp.tool()
async def merge_cells() -> dict:
    """Merge cells in a predefined range in Excel (A1:O27)"""
    global excel_app
    try:
        # Access the first worksheet
        worksheet = excel_app.ActiveSheet
        
        # Predefined range to merge (you can change this range as needed)
        range_to_merge = 'A1:W23'
        
        # Get the range of cells to merge
        cell_range = worksheet.Range(range_to_merge)
        
        # Merge the selected range
        cell_range.Merge()

        # Optionally, apply a red border and center text in the merged cells
        cell_range.Borders.Color = 255  # Red color
        cell_range.Borders.Weight = 4   # Apply border thickness
        cell_range.HorizontalAlignment = -4108  # Center align horizontally
        cell_range.VerticalAlignment = -4108    # Center align vertically
        cell_range.Value = "Merged Cells"  # You can customize the text

        return {
            "content": [
                TextContent(
                    type="text",
                    text=f"Cells {range_to_merge} merged successfully with red border and centered text."
                )
            ]
        }
    except Exception as e:
        return {
            "content": [
                TextContent(
                    type="text",
                    text=f"Error merging cells: {str(e)}"
                )
            ]
        }

@mcp.tool()
async def enter_text_centered(text: str) -> dict:
    """Enter text in Excel and center it"""
    global excel_app
    try:
        worksheet = excel_app.ActiveSheet
        cell_range = worksheet.Range('A1')
        cell_range.Value = text  # Set the text

        # Center the text
        cell_range.HorizontalAlignment = -4108  # Horizontal center
        cell_range.VerticalAlignment = -4108    # Vertical center
        cell_range.Font.Size = 100  # Set font size to 72
        worksheet.Rows("1:1").RowHeight = 100  # Set row height to 72

        return {
            "content": [
                TextContent(
                    type="text",
                    text=f"Text '{text}' entered and centered in cell A1."
                )
            ]
        }

    except Exception as e:
        return {
            "content": [
                TextContent(
                    type="text",
                    text=f"Error entering text: {str(e)}"
                )
            ]
        }



@mcp.tool()
async def take_screenshot_and_send_email(recipient_email: str, subject: str, message: str) -> dict:
    """Take a screenshot of the Excel window and send it via email."""
    global excel_app
    try:
        if not excel_app:
            return {
                "content": [
                    TextContent(
                        type="text",
                        text="Excel is not open. Please call open_excel first."
                    )
                ]
            }
        
        excel_win = Application(backend='uia').connect(path='EXCEL.EXE').top_window()
        excel_win.set_focus()
        time.sleep(1)

        hwnd = excel_win.handle
        rect = win32gui.GetWindowRect(hwnd)
        x, y, width, height = rect[0], rect[1], rect[2] - rect[0], rect[3] - rect[1]

        screenshot = pyautogui.screenshot(region=(x, y, width, height))
        temp_file = "excel_screenshot.png"
        screenshot.save(temp_file)
        
        # Enhance the message with a custom answer (you can adjust this as needed)
        enhanced_message = f"""
{message}

Please see the attached screenshot for the visual representation of the Excel sheet.
"""
        
        # Send email with the screenshot
        success = send_email_with_attachment(recipient_email, subject, enhanced_message, temp_file)
        
        # Clean up the temporary file
        if os.path.exists(temp_file):
            os.remove(temp_file)
        
        if success:
            return {
                "content": [
                    TextContent(
                        type="text",
                        text=f"Screenshot taken and email sent successfully to {recipient_email}"
                    )
                ]
            }
        else:
            return {
                "content": [
                    TextContent(
                        type="text",
                        text=f"Screenshot taken but failed to send email to {recipient_email}"
                    )
                ]
            }
    except Exception as e:
        return {
            "content": [
                TextContent(
                    type="text",
                    text=f"Error taking screenshot and sending email: {str(e)}"
                )
            ]
        }

def send_email_with_attachment(recipient_email: str, subject: str, message: str, attachment_path: str) -> bool:
    """Send email with attachment using SMTP."""
    try:
        # Create message
        msg = MIMEMultipart()
        msg["From"] = os.getenv("SENDER_EMAIL")
        msg["To"] = recipient_email
        msg["Subject"] = subject

        # Create email body
        body = f"""
        {message}

        Best regards,
        Your Name.
        """

        msg.attach(MIMEText(body, "plain"))

        # Attach the screenshot
        with open(attachment_path, "rb") as attachment:
            part = MIMEImage(attachment.read())
            part.add_header(
                "Content-Disposition",
                f"attachment; filename= {os.path.basename(attachment_path)}",
            )
            msg.attach(part)

        # Create SMTP session
        smtp_server = os.getenv("SMTP_SERVER")
        smtp_port = int(os.getenv("SMTP_PORT"))
        sender_email = os.getenv("SENDER_EMAIL")
        sender_password = os.getenv("SENDER_PASSWORD")
        
        print(f"Connecting to SMTP server: {smtp_server}:{smtp_port}")
        server = smtplib.SMTP(smtp_server, smtp_port)
        
        print("Starting TLS...")
        server.starttls()
        
        print(f"Logging in as {sender_email}...")
        server.login(sender_email, sender_password)

        # Send email
        print("Sending email...")
        server.send_message(msg)
        server.quit()
        print("Email sent successfully!")
        return True
    except smtplib.SMTPAuthenticationError as e:
        print(f"SMTP Authentication Error: {str(e)}")
        return False
    except Exception as e:
        print(f"Error sending email: {str(e)}")
        return False

# DEFINE RESOURCES

# Add a dynamic greeting resource
@mcp.resource("greeting://{name}")
def get_greeting(name: str) -> str:
    """Get a personalized greeting"""
    print("CALLED: get_greeting(name: str) -> str:")
    return f"Hello, {name}!"


# DEFINE AVAILABLE PROMPTS
@mcp.prompt()
def review_code(code: str) -> str:
    return f"Please review this code:\n\n{code}"
    print("CALLED: review_code(code: str) -> str:")


@mcp.prompt()
def debug_error(error: str) -> list[base.Message]:
    return [
        base.UserMessage("I'm seeing this error:"),
        base.UserMessage(error),
        base.AssistantMessage("I'll help debug that. What have you tried so far?"),
    ]

if __name__ == "__main__":
    # Check if running with mcp dev command
    print("STARTING")
    if len(sys.argv) > 1 and sys.argv[1] == "dev":
        mcp.run()  # Run without transport for dev server
    else:
        mcp.run(transport="stdio")  # Run with stdio for direct execution