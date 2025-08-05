# Warehouse Management System (WMS) MVP

This project is a Minimum Viable Product (MVP) for a Warehouse Management System (WMS). It provides a web interface to upload sales data from different marketplaces, standardizes the data, maps Stock Keeping Units (SKUs) to Master SKUs (MSKUs), and loads the data into a relational database.

## Features

*   **File Upload:** Upload sales data in CSV format from different marketplaces (Amazon, Flipkart, Meesho).
*   **Data Standardization:** Automatically detects the marketplace format and standardizes the data into a common structure.
*   **SKU Mapping:** Maps marketplace-specific SKUs to a master SKU (MSKU). This supports "combo products" where multiple SKUs can map to the same MSKU.
*   **SKU Management GUI:** A web interface to add, delete, and view SKU-to-MSKU mappings.
*   **Database Integration:** Includes scripts to create a database schema and load data into a relational database like Teable.io.
*   **AI-Powered Querying (Design):** A detailed design for integrating a text-to-SQL solution to allow natural language querying of the database.

## Tech Stack

*   **Backend:** Python, Flask
*   **Frontend:** HTML, simple.css
*   **Data Processing:** pandas
*   **Database:** Teable.io (or other Airtable alternatives)
*   **AI Querying (Proposed):** Vanna AI

## How to Set Up and Run

1.  **Clone the repository.**
2.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```
3.  **Configure Teable.io (Optional):**
    *   If you want to use the database integration, sign up for a free account at [Teable.io](https://teable.io/).
    *   Create a new base and get your API token and base ID.
    *   Set the following environment variables:
        ```bash
        export TEABLE_API_TOKEN="YOUR_TEABLE_API_TOKEN"
        export TEABLE_BASE_ID="YOUR_TEABLE_BASE_ID"
        ```
    *   Run the schema creation script:
        ```bash
        python create_schema.py
        ```
4.  **Run the application:**
    ```bash
    flask run
    ```
5.  **Access the application:**
    *   Open your browser to `http://127.0.0.1:5000` to access the main file upload page.
    *   Open `http://127.0.0.1:5000/mappings` to manage SKU mappings.

## How to Use

1.  **Manage Mappings:** Go to the `/mappings` page to add or delete SKU-to-MSKU mappings.
2.  **Upload Sales Data:** On the home page, select a CSV sales file from your computer and click "Upload".
3.  **Process and Download:** The application will process the file, map the SKUs, and provide a link to download the processed file.
4.  **Load to Database:** If you configured the Teable.io integration, the processed data will be automatically loaded into your base.

## AI Tool Usage

This project was developed with the assistance of an AI coding assistant. The AI was used for the following tasks:

*   **Code Generation:** Generating boilerplate code for the Flask application, file I/O, and data processing logic.
*   **Code Refactoring:** Improving the structure and readability of the code.
*   **Research and Documentation:** Researching database alternatives and text-to-SQL solutions, and generating the documentation for them.
*   **Debugging:** Identifying and fixing errors in the code.

## Relational DB Alternatives Research

The assignment required researching alternatives to Airtable for a user-friendly, editable database frontend. Here is a comparison of three popular choices:

| Feature           | Teable.io                                       | Baserow                                           | NocoDB                                            |
| ----------------- | ----------------------------------------------- | ------------------------------------------------- | ------------------------------------------------- |
| **Data Model**    | Relational, spreadsheet-like interface.         | Relational, with a focus on being a database first. | Can connect to existing SQL databases.            |
| **User Interface**| Clean, modern, and very similar to Airtable.    | More developer-focused, but still user-friendly.  | Aims to be a no-code platform on top of databases. |
| **API**           | Provides a REST API for programmatic access.    | Provides a REST API.                              | Provides a REST API and a GraphQL API.            |
| **Self-Hosting**  | Available.                                      | Available and open-source.                        | Available and open-source.                        |
| **Pricing**       | Offers a free tier and paid plans.              | Offers a free tier and paid plans.                | Open-source and free.                             |
| **Conclusion**    | A great choice for a direct Airtable replacement with a focus on ease of use. | A powerful and flexible option, especially for developers who want more control. | The best choice if you already have an existing SQL database that you want to expose through a user-friendly interface. |

For this project, **Teable.io** was chosen as the target database due to its similarity to Airtable and its user-friendly interface, which aligns well with the goal of providing a tool for non-technical users.
