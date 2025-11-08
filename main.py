import os
from dotenv import load_dotenv
import openai
import json

# Load environment variables
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

"""
Before submitting the assignment, describe here in a few sentences what you would have built next if you spent 2 more hours on this project:

If I had more time, I would add a simple UI so the kid can pick from a randomized set of themes
(e.g. adventure, funny, animals, robots, etc.)

I would find a way to make the judge feedback more strict, and test it. GPT does a good job a following my initial requirements, so it seems to always give a high score to the first story.

Lastly, I would implement a more interactive way to ask if the users wants to refine the story,
Perhaps with randomized messages such as: "Getting sleepy yet? Do you want another story?" or "Want me to change the story a bit, or is it time for bed?"
"""

# ------------------ LLM CALL WRAPPER ------------------
def call_model(prompt: str, max_tokens=700, temperature=0.5) -> str:
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",  # required by instructions
        messages=[{"role": "user", "content": prompt}],
        max_tokens=max_tokens,
        temperature=temperature
    )
    return response.choices[0].message["content"]

# ------------------ PROMPTS ------------------
def story_prompt(user_request: str) -> str:
    return f"""
Write a gentle bedtime story for children ages 5–10 based on this idea:

"{user_request}"

Requirements:
- Simple language a child can understand
- Focus on a calming tone, a simple plot, and relatable, gentle characters that can help relax a child before sleep
- Create charactrers with depth. The child should understand why the character is making specific choices and driving the story forward
- Maintain Momentum: Each scene should build upon the last, raising the stakes or offering new information that drives the story forward
- Follow this story arc structure: 
Act I (Setup): Introduce characters, setting, and the initial status quo. The inciting incident disrupts this balance and presents the main problem or challenge.
Act II (Confrontation/Rising Action): The bulk of the story. Create scenes where the protagonist attempts to solve the problem, facing obstacles, conflicts, and increasing stakes. This builds tension toward a climax.
Act III (Resolution): The climax occurs—the point of highest tension where the protagonist faces their greatest challenge. Afterward, the falling action resolves loose ends and the story concludes with the new normal.
- Include emojis when appropriate to keep the story fun and lively
"""

def refine_story_prompt(current_story: str, feedback: str) -> str:
    return f"""
Rewrite the following children's story based on the user's feedback.

Original story:
\"\"\"{current_story}\"\"\"

Feedback:
\"\"\"{feedback}\"\"\"

Make the new story warm, child-friendly, imaginative, and easy to understand. 
Keep a clear moral at the end and maintain a gentle bedtime tone.
"""

def judge_prompt(story: str) -> str:
    return f"""
You are a strict literary critic for children's bedtime stories (ages 5–10).
You NEVER give high scores unless all conditions are met perfectly.


Story:
\"\"\"{story}\"\"\"

Rate the story from 1–10 based ONLY on these criteria:

1. **Simple language** a 5–10 year old can understand
2. **Calming tone** suitable for bedtime
3. **Relatable, gentle characters** who make emotionally clear choices
4. **Character depth** — a child should understand *why* characters act the way they do
5. **Strong plot momentum** — each scene builds on the last, adding gentle tension or curiosity
6. **Story arc quality**:
   - Act I: Clear introduction & inciting incident
   - Act II: Rising action & gentle challenge/problem solving
   - Act III: Satisfying climax and resolution, establishing a “new normal”
7. **Includes emojis appropriately** to make the story fun and child-friendly
8. **No scary or violent content**
9. **Has a wholesome lesson or emotional takeaway**

Strict scoring rules:
- 9–10: Masterful bedtime story; meets ALL criteria
- 7–8: Good but noticeable weaknesses (you MUST list them)
- 4–6: Major issues in plot, tone, clarity, or emotional arc
- 0–3: Inappropriate, confusing, or violates bedtime tone requirements

Return ONLY valid JSON in this exact format:

{{
 "score": <number>,
 "feedback": "<1 sentence: tell the writer what to improve>"
}}
"""

# ------------------ STORY FLOW ------------------
def generate_story(user_request: str) -> str:
    return call_model(story_prompt(user_request))

def revise_story(story: str, feedback: str) -> str:
    return call_model(refine_story_prompt(story, feedback))

def maybe_improve(story: str) -> str:
    review = call_model(judge_prompt(story), temperature=0.2)

    try:
        result = json.loads(review)
        score = result["score"]
        feedback = result["feedback"]
    except:
        print("Judge failed to parse response.")
        return story

    print(f"\n Judge Score: {score}")
    print(f"Judge Feedback: {feedback}")

    if score < 8:
        print("Judge requests improvement — refining story...")
        story = revise_story(story, feedback)
    else:
        print("Judge approved story — no auto refinement needed.")

    return story


# ------------------ MAIN INTERACTION LOOP ------------------
def main():
    user_input = input("🌙 What kind of bedtime story would you like? ")

    story = generate_story(user_input)

    story = maybe_improve(story)

    print("\n⭐ Your bedtime story:\n")
    print(story)

    while True:
        choice = input("\nWould you like to change anything in the story? (yes/no) ").strip().lower()
        if choice not in ["yes", "y"]:
            break

        print("\nTell me what you'd like to change (e.g., 'add a dragon', 'make it funnier'):")
        feedback = input("> ")
        story = revise_story(story, feedback)

        print("\n✨ Updated story:\n")
        print(story)

    print("\n🌜 Goodnight and sweet dreams! ✨")

if __name__ == "__main__":
    main()
