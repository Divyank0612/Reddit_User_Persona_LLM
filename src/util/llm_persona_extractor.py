import ollama
from datetime import datetime


def extract_persona_llm(cleaned_posts, cleaned_comments,username,profile):
    text_data = ""

    for idx, post in enumerate(cleaned_posts):
        text_data += f"[Post #{idx+1}]\nText: {post['cleaned']}\nURL: {post['url']}\n\n"

    for idx, comment in enumerate(cleaned_comments):
        text_data += f"[Comment #{idx+1}]\nText: {comment['cleaned']}\nURL: {comment['url']}\n\n"


    if len(text_data.strip()) == 0:
        print("Error: No input data found for persona extraction.")
        return "No data to process"

    print("Input text length:", len(text_data))
    print("Sample input:", text_data[:500])

    system_prompt = """
You are an expert in user persona extraction.

You will receive a collection of Reddit posts and comments, all written by the **same individual user**.
Your task is to extract their personal details to create a **comprehensive user persona**.

Please extract the following aspects:

- Name/Nickname
- Age/Stage of Life
- Location
- Occupation/Education
- Interests & Hobbies
- Values/Beliefs
- Pain Points / Challenges
- Motivations
- Personality Traits
    - Classify also among these: (Introvert or Extrovert), (Intuition or Sensing), (Feeling or Thinking), (Perceiving or Judging)
- Content Tone

---

### **IMPORTANT: Citations Handling (MANDATORY)**

For **each trait**, include:

- **Trait Name**: Value  
- **Evidence**: Provide:
    - **Text Snippet:** Quote from the post/comment  
    - **URL:** Link to the source (use the URL provided in input)

---

#### **Example Format (Use Exactly This Style):**

**Location: New York, USA**  
- **Evidence**: "As someone living in NYC, I see this all the time."  
- **URL**: https://reddit.com/r/nyc/comments/xyz123

---

### **Unknown Traits Handling:**

If you cannot find direct information, infer from context. Output:

Also explain **why you suggested this** in the evidence field.

---

### **User Metadata **

You will also receive Reddit metadata for this user:

For account data refer
- **Link Karma**: {link_karma}
- **Comment Karma**: {comment_karma}
- **Account Creation Date (Cake Day)**: {cake_day}

Use this metadata to enrich the persona where relevant. For example:

- High **comment karma**: Likely enjoys discussions, may be witty or social.
- Low **link karma** but high **comment karma**: Prefers participation over content creation.
- Old account: Indicates tech-savviness, familiarity with online communities.

Weave these insights into personality traits or motivations if relevant.

Keep the language **professional, concise, and human-readable**.
"""



    link_karma = profile["karma"]["link_karma"]
    comment_karma = profile["karma"]["comment_karma"]
    cake_day_readable = datetime.utcfromtimestamp(float(profile["cake_day"])).strftime('%Y-%m-%d')

    system_prompt = system_prompt.format(
    username=username,
    link_karma=link_karma,
    comment_karma=comment_karma,
    cake_day=cake_day_readable
)

    try:
        response = ollama.chat(
            model='llama3:latest',   
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": text_data[:3000]}
            ]
        )

        # Print raw response for debugging
        print("Raw Ollama response:", response)

        if 'message' in response:
            output = response['message']['content']
        elif 'content' in response:
            output = response['content']
        else:
            output = str(response)

        print("\n--- Persona Extracted ---\n")
        print(output)

        filename = f"output_txt_file/{username}_persona.txt"

        with open(filename, "w", encoding="utf-8") as f:
            f.write(output)

        return output

    except Exception as e:
        print("LLM call failed:", e)
        return "LLM error"
