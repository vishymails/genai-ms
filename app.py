from flask import Flask, request, jsonify
import cohere
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

try :
    COHERE_API_KEY = os.getenv("COHERE_API_KEY")

    if not COHERE_API_KEY:
        raise ValueError("Cohere API key not found in environment variables.")
    co = cohere.Client(COHERE_API_KEY)

    MODEL_NAME = "command-a-03-2025"
    print("Cohere client initialized successfully. {MODEL_NAME} model is set.")

except ValueError as ve:
    print(f"ValueError: {ve}")
    co = None
except Exception as e:
    print(f"An error occurred while initializing the Cohere client: {e}")
    co = None


@app.route('/chat', methods=['POST'])
def handle_chat_request() :
    if co is None:
        return jsonify({"error": "Cohere client is not initialized."}), 500

    
    try :
        data = request.get_json()
        user_message = data.get('message', '')

        if not user_message:
            return jsonify({"error": "No message provided."}), 400
    except  Exception as e:
        return jsonify({"error": f"Invalid request data: {e}"}), 400

    try :
        response = co.chat(
            model=MODEL_NAME,
            message = user_message
        )

        ai_response_text = response.text

        print(f"User Message: {user_message}")
        print(f"AI Response: {ai_response_text}")

        return jsonify({
            "query": user_message,
            "response": ai_response_text,
            "model_used": MODEL_NAME
        })

    except Exception as e:
        print(f"Error during Cohere API call: {e}")
        return jsonify({"error": f"Error during Cohere API call: {e}"}), 500

if __name__ == '__main__' :
    app.run(debug=True, port=5000)