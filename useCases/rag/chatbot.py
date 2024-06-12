from flask import Flask, request, jsonify
import os
from puppy.llm.openAI import open_ai_chat


app = Flask(__name__)

prompt=[
    {
      "role": "system",
      "content": "You will be provided with a message, and your task is to respond as an AI assistant."
    },
    {
      "role": "user",
      "content": "How are you?"
    }
]


def generate_response(input_text):
    response = open_ai_chat(prompt=prompt, printing=True, stream=True, temperature=0.9)
    return response


@app.route('/get_response', methods=['POST'])
def get_response():
    input_text = request.json['input']
    response = generate_response(input_text)

    return jsonify({'response': response})


import gradio as gr


def interface(input_text):
    response = generate_response(input_text)
    return response


#iface = gr.Interface(fn=interface, inputs="text", outputs="text")
#iface.launch()

if __name__ == "__main__":
    app.run(debug=True, port=int(os.environ.get('PORT', 5000)))