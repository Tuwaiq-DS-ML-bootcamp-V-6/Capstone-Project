import json
import chainlit as cl
from weaviate import Client

# Initialize Weaviate client with the API key in headers
weaviate_client = Client(
    url="http://localhost:8080",
    additional_headers={
        "X-Openai-Api-Key": ""
    }
)

# Temporary global state to store user input
global_user_input = ""

@cl.on_message
async def handle_message(message: cl.Message):
    global global_user_input
    user_input = message.content.strip()
    global_user_input = user_input

    # Send initial message with buttons
    actions = [
        cl.Action(name=" منصة سطر", value="sadr", description="Sadr Academy"),
        cl.Action(name="أكاديمية طويق", value="tuwaiq", description="Tuwaiq Academy")
    ]

    await cl.Message(content="يرجى اختيار الأكاديمية التي ترغب في استعراض دوراتها التدريبية", actions=actions).send()

@cl.action_callback(" منصة سطر")
async def on_tuwaiq(action):
    global global_user_input
    user_input = global_user_input

    # Query Weaviate for Sadr Academy courses with additional fields
    response = (
        weaviate_client.query
        .get("Courses", ["course_name", "content", "job_titles"])
        .with_near_text({"concepts": [user_input]})
        .with_limit(3)
        .do()
    )

    # Process the response
    courses = response.get('data', {}).get('Get', {}).get('Courses', [])
    if not courses:
        formatted_response = "No results found for Sadr Academy."
    else:
        formatted_courses = "\n\n".join([
            f"Course Name: {course['course_name']}\n"
            f"Tools and Languages: {course.get('content', 'N/A')}\n"
            f"Job Titles: {(course.get('job_titles', []))}\n"
            for course in courses
        ])
        formatted_response = f":إليك أبرز الدورات المتاحة في أكاديمية سطر\n\n{formatted_courses}"

    msg = cl.Message(content=" ")
    for token in formatted_response:
        await msg.stream_token(token)
    await msg.send()

    await action.remove()

@cl.action_callback("أكاديمية طويق")
async def on_sadr(action):
    global global_user_input
    user_input = global_user_input

    # Query Weaviate for Tuwaiq Academy courses with additional fields
    response = (
        weaviate_client.query
        .get("TQSkills", ["content", "job_titles", "tools_and_languages"])
        .with_near_text({"concepts": [user_input]})
        .with_limit(3)
        .do()
    )

    # Process the response
    courses = response.get('data', {}).get('Get', {}).get('TQSkills', [])
    if not courses:
        formatted_response = "No results found for Tuwaiq Academy."
    else:
        formatted_courses = "\n\n".join([
            f"Course Name: {course['content']}\n"
            f"Job Titles: {(course.get('job_titles', []))}\n"
            f"Tools and Languages: {(course.get('tools_and_languages', []))}\n"
            for course in courses
        ])
        formatted_response = f":إليك أبرز الدورات المتاحة في أكاديمية طويق\n\n{formatted_courses}"

    msg = cl.Message(content=" ")
    for token in formatted_response:
        await msg.stream_token(token)
    await msg.send()

    await action.remove()

# Run the Chainlit application
if __name__ == "__main__":
    cl.run()




