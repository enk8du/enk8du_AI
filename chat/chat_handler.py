def chat_with_ai(messages):

    try:
        response = client.chat.completions.create(
            model="llama3-8b-8192",
            messages=messages
        )

        return response.choices[0].message.content

    except Exception as e:
        return f"ERROR: {str(e)}"