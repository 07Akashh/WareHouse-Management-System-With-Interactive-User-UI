# AI Over Data Layer: Text-to-SQL Integration

This document outlines the research and proposed architecture for integrating a text-to-SQL solution into the WMS, fulfilling Part 4 of the assignment. The goal is to allow non-technical users to query the WMS database using natural language.

## 1. Research on Text-to-SQL Tools

I researched several tools that provide text-to-SQL capabilities. The two most promising options are Lumina AI (as mentioned in the assignment) and Vanna AI.

### a) Lumina AI

*   **Description:** Lumina AI appears to be a broader data platform that includes AI-powered analytics. The reference video suggests it can connect to a data source and provide a chat-like interface for asking questions, generating charts, and adding calculated fields.
*   **Pros:**
    *   Seems to be a complete, all-in-one solution.
    *   User-friendly interface designed for business users.
    *   Can likely handle complex queries and generate visualizations directly.
*   **Cons:**
    *   As a commercial product, it might be less flexible for deep integration.
    *   Pricing and specific API capabilities are not publicly available, requiring a demo or sales contact.
    *   It's a "black box," meaning less control over the text-to-SQL models.

### b) Vanna AI

*   **Description:** Vanna is an open-source Python library for text-to-SQL. It works by "training" on your database schema, which involves generating and storing metadata about your tables, columns, and relationships. It can then use this metadata to generate accurate SQL queries from natural language questions.
*   **Pros:**
    *   **Open-source and highly customizable:** You can choose the underlying LLM (e.g., GPT-4, Llama) and the vector database for storing the metadata.
    *   **High accuracy:** The "training" process makes it very accurate for a specific database schema.
    *   **Integrates directly into a Python application:** It's a library, not an external service, giving you full control.
*   **Cons:**
    *   Requires more development effort to set up and integrate.
    *   You are responsible for hosting the LLM and the vector database (though free options are available).

### Conclusion

For this project, **Vanna AI** is the recommended choice. Its open-source nature and direct Python integration make it a perfect fit for our existing Flask application. It provides more control and is more transparent than a closed-box solution like Lumina AI, while still being incredibly powerful.

## 2. Proposed Architecture with Vanna AI

The following diagram illustrates how Vanna AI would be integrated into our WMS:

```
+-----------------+      +-------------------+      +----------------+
|   User (Web UI) |----->|   Flask Backend   |----->|   Vanna AI     |
+-----------------+      |     (app.py)      |      | (Python Lib)   |
                         +-------------------+      +----------------+
                                   ^                       |
                                   | SQL Query             | Generates SQL
                                   v                       v
                         +-------------------+      +----------------+
                         |  Teable.io DB     |<-----|   LLM (OpenAI) |
                         +-------------------+      +----------------+
```

**Data Flow:**

1.  **User Input:** The user types a natural language question into a new text box on the web UI (e.g., "What were the total sales for cste-pen last week?").
2.  **API Call:** The frontend sends this question to a new endpoint on our Flask backend (e.g., `/api/query`).
3.  **Vanna AI Processing:**
    *   The Flask endpoint passes the question to the Vanna AI library.
    *   Vanna AI uses the pre-generated "training" data about our Teable.io schema to construct a prompt for an LLM.
    *   It sends this prompt to the LLM (e.g., GPT-4 via the OpenAI API).
4.  **SQL Generation:** The LLM returns a SQL query to Vanna AI.
5.  **Database Query:** Vanna AI executes the generated SQL query against our Teable.io database.
6.  **Return Result:** The query result (e.g., a pandas DataFrame) is returned to the Flask endpoint.
7.  **Display Result:** The Flask endpoint formats the result (e.g., as JSON or a rendered table) and sends it back to the user's web UI to be displayed.

## 3. Hypothetical Code Snippet (in app.py)

This code snippet shows how a new `/api/query` endpoint might look using Vanna AI.

```python
# --- Vanna AI Setup (would be in a separate config file) ---
# import vanna as vn
#
# vn.set_api_key("YOUR_VANNA_API_KEY")
# vn.set_model("your-chosen-llm")
# vn.connect_to_teable(api_key="YOUR_TEABLE_API_KEY", base_id="YOUR_TEABLE_BASE_ID")
# # In a real app, you would run vn.train(...) once to train on your schema.

# --- New API Endpoint in app.py ---
# @app.route('/api/query', methods=['POST'])
# def api_query():
#     """Handles natural language queries using Vanna AI."""
#     question = request.json.get('question')
#     if not question:
#         return jsonify({"error": "No question provided"}), 400
#
#     try:
#         # Ask the question and get a pandas DataFrame as the result
#         df = vn.ask(question)
#         result = df.to_json(orient='records')
#         return jsonify({"result": result})
#
#     except Exception as e:
#         return jsonify({"error": str(e)}), 500

```

This architecture provides a powerful and flexible way to add natural language querying to the WMS, empowering non-technical users to explore the data themselves.
