# Hippocratic AI Bedtime Story Generator

This Python script generates bedtime stories for children ages 5–10.  
It uses an LLM storyteller + an LLM judge to generate the stories based off given requirements.

## Instructions to Run
Create a `.env` file with:

OPENAI_API_KEY=your-key-here

Run main.py

### Features

- Takes a child's story idea as input and turns it into a bedtime story
- Requirements listed in the prompt:
  - Simple child-friendly language
  - Emotionally wholesome tone
  - 3-act story structure (Setup → Rising Action → Resolution)
  - Character motivations and emotional depth
  - No fear, violence, or stressful content
  - Relevant emoji use in the output to keep the story lively
- LLM judge evaluates each story (1–10) before showing to user
- Automatically improves story if score < 8
- User can request ANY type of revisions (“add a dragon”, “make it sillier”)


#### Components
Story Generator (GPT-3.5-Turbo) | Creates story from structured prompt 
Story Judge (GPT-3.5-Turbo) | Scores story 1–10 w/ targeted rubric & feedback 
Refinement Loop | Auto-refines based on judge or user feedback 
CLI | Displays story and interacts with user 

#### Flow Diagram
Please see the attached file diagram.jpg to view the flow diagram of this script.
