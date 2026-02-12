import os
from google import genai
from google.genai import types

# 1. Define the actual Python function (the "tool")
@tools.tool
def Maintenance_Plan(equipment_id: str) -> dict:
    """
    Creates a maintenance plan for a specific equipment ID.
    Args:
        equipment_id: The unique identifier for the machinery or equipment.
    """
    # In a real scenario, this would query a database or ERP system.
    # For now, we return mock data.
    print(f"\n[System] Generating plan for ID: {equipment_id}...")
    
    return {
        "equipment_id": equipment_id,
        "plan_status": "Scheduled",
        "tasks": [
            "Lubricate joints",
            "Replace air filter",
            "Calibration check"
        ],
        "next_service_date": "2026-03-15",
        "technician_assigned": "Sarah Miller"
    }

# 2. Configure the Gemini Client
# Ensure your API key is set in your environment variables
client = genai.Client(api_key="YOUR_API_KEY") 

# 3. Initialize the model with the tool
# Note: Gemini 2.5 Pro is the latest reasoning model in the 2.5 series
model_id = "gemini-2.5-pro"

# We pass the function directly to the tools list
# The SDK automatically handles the JSON schema generation

# Load the agent using your YAML file
# The ADK will now find 'Maintenance_Plan' because it's registered above
agent = agents.Agent.from_yaml('/home/devstar3414/adkui/My_agent/root_agent.yaml')

response = agent.run("Generate a maintenance plan for SN-992")
print(response.text)

config = types.GenerateContentConfig(
    tools=[Maintenance_Plan],
    temperature=0  # Lower temperature is better for tool calling accuracy
)

# 4. Execute the request
prompt = "I need a maintenance plan for the industrial pump with ID PUMP-99."

response = client.models.generate_content(
    model=model_id,
    contents=prompt,
    config=config
)

# 5. Handle the Tool Call
# The model will return a 'function_call' part if it wants to use the tool
for part in response.candidates[0].content.parts:
    if part.function_call:
        # Extract function name and arguments
        fn_name = part.function_call.name
        args = part.function_call.args
        
        # Execute the local function
        if fn_name == "Maintenance_Plan":
            result = Maintenance_Plan(**args)
            
            # 6. Send the tool output back to Gemini to get a final natural language response
            final_response = client.models.generate_content(
                model=model_id,
                contents=[
                    types.Content(role="user", parts=[types.Part.from_text(prompt)]),
                    response.candidates[0].content, # The model's call
                    types.Content(role="tool", parts=[
                        types.Part.from_function_response(
                            name=fn_name,
                            response={"result": result}
                        )
                    ])
                ]
            )
            print("\nGemini's Response:")
            print(final_response.text)