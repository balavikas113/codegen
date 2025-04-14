import os
import requests
import gradio as gr

# Step 1: Setup function with Google Gemini configuration
def setup_gemini_client():
    # Set up the Gemini API with the provided API key
    api_key = "AIzaSyByIVaDRoc3g8u_hY1_BCegEyfJ-ZkmkX4"
    return api_key

# Step 2: Code generation function with optimized prompt
def generate_code(problem_statement):
    try:
        # Get the API key
        api_key = setup_gemini_client()
        
        # Create the system prompt for code generation
        system_prompt = (
            "You are a **Code Generator**, an expert at creating clean, efficient, and well-documented code "
            "based on problem statements. Your task is to generate high-quality code that solves the given problem. "
            "Structure your response as follows:\n\n"
            
            "### **1. PROBLEM UNDERSTANDING**\n"
            "- Briefly summarize your understanding of the problem.\n\n"
            
            "### **2. SOLUTION APPROACH**\n"
            "- Explain the approach you're taking to solve the problem.\n"
            "- Mention any algorithms, data structures, or design patterns you're using.\n\n"
            
            "### **3. CODE SOLUTION**\n"
            "\n"
            "# Include your complete code solution here\n"
            "# Add clear comments to explain complex parts\n"
            "\n\n"
            
            "### **4. USAGE EXAMPLE**\n"
            "- Show an example of how to use the code.\n\n"
            
            "### **5. COMPLEXITY ANALYSIS**\n"
            "- Briefly analyze the time and space complexity of your solution.\n\n"
            
            "**Note:** Ensure the code is correct, efficient, and follows best practices for the language used."
        )
        
        # Create the full prompt
        full_prompt = f"{system_prompt}\n\nPROBLEM STATEMENT:\n\n{problem_statement}"
        
        # Set up the API request
        url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent"
        headers = {
            "Content-Type": "application/json"
        }
        
        # Prepare the request data
        data = {
            "contents": [
                {
                    "parts": [
                        {
                            "text": full_prompt
                        }
                    ]
                }
            ]
        }
        
        # Send the request
        response = requests.post(
            f"{url}?key={api_key}",
            headers=headers,
            json=data
        )
        
        # Parse the response
        response_json = response.json()
        
        # Extract the generated text
        if "candidates" in response_json and len(response_json["candidates"]) > 0:
            return response_json["candidates"][0]["content"]["parts"][0]["text"]
        else:
            return "Error: Unable to generate response. " + str(response_json)

    except Exception as e:
        return f"Error: {str(e)}"

# Get the absolute path to the CSS file
css_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "style.css")

# Create a simple interface
def create_interface():
    # Using the simple interface approach to avoid JavaScript integration issues
    interface = gr.Interface(
        fn=generate_code,
        inputs=gr.Textbox(label="Problem Statement", lines=5, placeholder="Describe the problem you want to solve..."),   
        outputs=gr.Textbox(label="Generated Code", lines=20),
        title="💻 Code Generator AI",
        description="Describe a problem, and I'll generate code to solve it.",
        examples=[
            ["Create a function to find the nth Fibonacci number using dynamic programming."],
            ["Write a Python script to download and extract text from a webpage."],
            ["Create a simple REST API with Flask that stores and retrieves user data."],
        ],
        allow_flagging="never",
        css=style.css
        
    )
    
    return interface

# Run the application
if __name__ == "__main__":
    interface = create_interface()
    interface.launch()
