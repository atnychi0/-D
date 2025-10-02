import base64
import hashlib
import os
import threading
import webbrowser

import numpy as np
import pandas as pd
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad
from flask import Flask, render_template_string, request


# --- START OF FILE HELPER FUNCTIONS & CLASSES ---

def generate_secure_key(user_input: str) -> str:
    """Generate a secure key using user input as seed material."""
    base_key = hashlib.sha256(user_input.encode()).digest()
    salt = os.urandom(16)
    derived_key = hashlib.pbkdf2_hmac("sha256", base_key, salt, 100000, dklen=32)
    data_to_encrypt = os.urandom(32)
    cipher = AES.new(derived_key, AES.MODE_CBC)
    ct_bytes = cipher.encrypt(pad(data_to_encrypt, AES.block_size))
    encrypted_blob = base64.b64encode(salt + cipher.iv + ct_bytes).decode("utf-8")
    return encrypted_blob


def recursive_harmonic_lock(phi: float = 1.6180339887, iterations: int = 144) -> np.ndarray:
    """Generate a harmonic lock spiral inspired by the golden ratio."""
    signal = []
    theta = np.pi / phi  # golden phase
    for i in range(iterations):
        radius = phi ** (i / 12)  # harmonic scale base-12
        x_val = radius * np.cos(i * theta)
        y_val = radius * np.sin(i * theta)
        signal.append((x_val, y_val))
    return np.array(signal)


# --- END OF FILE HELPER FUNCTIONS & CLASSES ---


# --- STRIPE_SECRET_KEY & PUBLISHABLE_KEY EXAMPLE - FOR DEMONSTRATION ONLY ---
stripe_secret_key = "sk_test_your_secret_key"
stripe_publishable_key = "pk_test_your_publishable_key"
# PLEASE REPLACE WITH YOUR ACTUAL STRIPE KEYS


# --- forgekey_full_app.py (FLASK APP) ---
app = Flask(__name__)
HTML_TEMPLATE = """
<!doctype html>
<title>ForgeKey Generator</title>
<h2>ForgeKey: Generate Secure Keys</h2>
<form method=post>
  <input type=text name=input placeholder="Enter your secret input" size="40">
  <input type=submit value=Generate>
</form>
{% if key %}
<h3>Generated Key:</h3>
<p><textarea rows="4" cols="80">{{ key }}</textarea></p>
{% endif %}
"""


@app.route("/", methods=["GET", "POST"])
def index():
    key = None
    if request.method == "POST":
        user_input = request.form["input"]
        key = generate_secure_key(user_input)
    return render_template_string(HTML_TEMPLATE, key=key)


def run_flask_app():
    """Launch the Flask app and open it in a browser when executed directly."""
    if __name__ == "__main__":
        threading.Timer(1.25, lambda: webbrowser.open("http://localhost:5000")).start()
        app.run(debug=False)


# --- Load and print input CSV data ---
def load_and_print_csv(filepath: str = "input.csv"):
    """Load a CSV file, print a quick summary, and return the dataframe."""
    try:
        df = pd.read_csv(filepath)
        print("CSV File Content (head):\n", df.head())
        print("\nCSV File Info:\n", df.info())
        return df
    except FileNotFoundError:
        print(f"Error: The file '{filepath}' was not found.")
        return None
    except Exception as exc:  # pylint: disable=broad-except
        print(f"An error occurred while loading the CSV file: {exc}")
        return None


def search_copyscript(df, copyscript_content, verbose: bool = True):
    """Search the copyscript for math fields listed in the dataframe."""
    if df is None or copyscript_content is None:
        print(
            "Warning: search_copyscript was called but dataframe or copy script was none. "
            "Returning an empty list."
        )
        return []

    matched_fields = []
    for field in df["Field"]:
        if isinstance(field, str) and field.lower() in copyscript_content.lower():
            matched_fields.append(field)
    if verbose:
        print("\nMatched fields in Copyscript:\n", matched_fields)
    return matched_fields


def analyze_files():
    """Driver routine to execute the CSV and copyscript analysis."""
    csv_df = load_and_print_csv("Full_Set_of_112__Real_Math_Domains__Expanded_.csv")
    if csv_df is not None:
        try:
            with open("FINAL_CROWN_DARPA_COPYSCRIPT.txt", "r", encoding="utf-8") as file:
                copyscript_content = file.read()
        except FileNotFoundError:
            print("Error: The file 'FINAL_CROWN_DARPA_COPYSCRIPT.txt' was not found.")
            return

        matched = search_copyscript(csv_df, copyscript_content)

        if matched:
            print(
                "\nRelevant fields found in copy script (High-level view):",
                ", ".join(matched),
            )
        else:
            print(
                "\nNo related mathematical fields were identified in the copyscript by simple "
                "matching. Consider increasing match precision, or further manual checks "
                "to better correlate documents."
            )


if __name__ == "__main__":
    run_flask_app()
    analyze_files()

    print("\nScript Complete.")
