"""Google Search Agent definition for ADK Bidi-streaming demo."""

import os

from google.adk.agents import Agent
from google.adk.tools import google_search
from dotenv import load_dotenv

load_dotenv()

# Default models for Live API with native audio support:
# - Gemini Live API: gemini-2.5-flash-native-audio-preview-12-2025
# - Vertex AI Live API: gemini-live-2.5-flash-native-audio
root_agent = Agent(
    name="google_search_agent",
    model="gemini-2.5-pro",
    tools=Maintenance_Plan,
    instruction="You are a helpful assistant that can search the web.",
)