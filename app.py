with open("file_map.txt", "a") as f:from flask import Flask, request, render_template_string
import os

import time
import threading

def auto_delete(filepath, delay=900):  # 900 sec = 15 min
    def delete():
        time.sleep(delay)
        if os.path.exists(filepath):
            os.remove(filepath)
            print(f"[+] Deleted: {filepath}")
    threading.Thread(target=delete).start()

app = Flask(__name__)

UPLOAD_FOLDER = "uploads"

# ---------------- TOKEN FUNCTIONS ----------------
def load_tokens():
    if not os.path.exists("tokens.txt"):
        return set()
    with open("tokens.txt", "r") as f:
        return set([line.strip() for line in f if line.strip()])

def consume_token(token):
    token = token.strip()
    tokens = load_tokens()

    if token in tokens:
        tokens.remove(token)
        with open("tokens.txt", "w") as f:
            for t in tokens:
                f.write(t + "\n")
        return True
    return False


# ---------------- HTML (YOUR ORIGINAL STYLE) ----------------
HTML = """
<!DOCTYPE html>
<html>
<head>
<title>Secure DropBox</title>

<style>
body {
    background: #0a0f1a;
    color: #00ffcc;
    font-family: monospace;
    display: flex;
    justify-content: center;
    align-items: center;
    height: 100vh;
    margin: 0;
}

.container {
    border: 1px solid #00ffcc;
    padding: 35px;
    width: 420px;
    text-align: center;
    box-shadow: 0 0 25px #00ffcc33;
    border-radius: 10px;
}

h2 {
    margin-bottom: 20px;
    letter-spacing: 1px;
}

.upload-box {
    border: 2px dashed #00ffcc;
    padding: 20px;
    margin-bottom: 15px;
    transition: 0.3s;
}

.upload-box:hover {
    background: #00ffcc11;
}

input[type="file"] {
    margin-top: 10px;
    color: #00ffcc;
}

input[type="text"] {
    padding: 8px;
    width: 80%;
    background: black;
    border: 1px solid #00ffcc;
    color: #00ffcc;
    margin-bottom: 15px;
}

button {
    background: black;
    color: #00ffcc;
    border: 1px solid #00ffcc;
    padding: 10px 20px;
    cursor: pointer;
    transition: 0.3s;
}

button:hover {
    background: #00ffcc;
    color: black;
}

.note {
    margin-top: 15px;
    font-size: 12px;
    color: #888;
}

#status {
    margin-top: 10px;
    font-size: 14px;
}
</style>
</head>

<body>

<div class="container">
    <h2>🧅 Secure DropBox</h2>

    <div class="upload-box">
        <p>Select File</p>
        <input type="file" id="fileInput">
    </div>

    <input type="text" id="token" placeholder="Enter access token">

    <br>
    <button onclick="encryptAndUpload()">Encrypt & Upload</button>

    <p id="status"></p>

    <hr>
    
    <h3>📥 Download File</h3>
    
    <input type="text" id="downloadID" placeholder="Enter File ID"><br><br>
    
    <button onclick="downloadFile()">Download</button>

    <hr>
    
    <h3>🔓 Decrypt File</h3>
    
    <input type="file" id="encFile"><br><br>
    <input type="text" id="decKey" placeholder="Enter decryption key"><br><br>
    
    <button onclick="decryptFile()">Decrypt File</button>

    <div class="note">
        • Files are encrypted before upload<br>
        • One-time token access<br>
        • Files Are Wiped-Out (15 Min)
    </div>
</div>

<script>
async function encryptAndUpload() {
    const fileInput = document.getElementById("fileInput");
    const tokenInput = document.getElementById("token");

    const file = fileInput.files[0];
    const token = tokenInput.value;

    if (!file) {
        alert("Select file first");
        return;
    }

    if (!token) {
        alert("Enter token");
        return;
    }

    const reader = new FileReader();

    reader.onload = async function() {
        try {
            const data = new Uint8Array(reader.result);

            const key = await crypto.subtle.generateKey(
                { name: "AES-GCM", length: 256 },
                true,
                ["encrypt", "decrypt"]
            );

            const exportedKey = await crypto.subtle.exportKey("raw", key);
            const keyBase64 = btoa(String.fromCharCode(...new Uint8Array(exportedKey)));

            alert("SAVE THIS KEY:\\n" + keyBase64);

            const iv = crypto.getRandomValues(new Uint8Array(12));

            const encrypted = await crypto.subtle.encrypt(
                { name: "AES-GCM", iv: iv },
                key,
                data
            );

            const blob = new Blob([iv, new Uint8Array(encrypted)]);

            const formData = new FormData();
            formData.append("file", blob, file.name);
            formData.append("token", token);

            document.getElementById("status").innerText = "Uploading...";

            const response = await fetch("/", {
                method: "POST",
                body: formData
            });

            const text = await response.text();

            if (text === "INVALID_TOKEN") {
                document.getElementById("status").innerText = "❌ Invalid or used token";
            } else if (text.startsWith("SUCCESS:")) {
                const fileID = text.split(":")[1];
            
                document.getElementById("status").innerHTML =
                    "✅ File uploaded<br>File ID: " + fileID;
            } else {
                document.getElementById("status").innerText = "⚠️ Error occurred";
            }

        } catch (err) {
            console.error(err);
            alert("Encryption error");
        }
    };

    reader.readAsArrayBuffer(file);
}

function downloadFile() {
    const fileID = document.getElementById("downloadID").value;

    if (!fileID) {
        alert("Enter File ID");
        return;
    }

    window.location.href = "/download/" + fileID;
}

async function decryptFile() {
    const fileInput = document.getElementById("encFile");
    const keyInput = document.getElementById("decKey");

    const file = fileInput.files[0];
    const keyBase64 = keyInput.value;

    if (!file || !keyBase64) {
        alert("File and key required");
        return;
    }

    const reader = new FileReader();

    reader.onload = async function() {
        try {
            const data = new Uint8Array(reader.result);

            const iv = data.slice(0, 12);
            const encrypted = data.slice(12);

            // Decode key
            const keyRaw = Uint8Array.from(atob(keyBase64), c => c.charCodeAt(0));

            const key = await crypto.subtle.importKey(
                "raw",
                keyRaw,
                { name: "AES-GCM" },
                false,
                ["decrypt"]
            );

            const decrypted = await crypto.subtle.decrypt(
                { name: "AES-GCM", iv: iv },
                key,
                encrypted
            );

            const blob = new Blob([decrypted]);

            const url = URL.createObjectURL(blob);

            const a = document.createElement("a");
            a.href = url;
            a.download = "decrypted_file";
            a.click();

        } catch (err) {
            console.error(err);
            alert("Decryption failed (wrong key or corrupted file)");
        }
    };

    reader.readAsArrayBuffer(file);
}

</script>

</body>
</html>
"""

# ---------------- UPLOAD ROUTE ----------------
@app.route("/", methods=["GET", "POST"])
def upload_file():

    if request.method == "POST":
        token = request.form.get("token")

        if not token or not consume_token(token):
            return "INVALID_TOKEN"

        file = request.files.get("file")

        if not file:
            return "NO_FILE"

        import uuid
        filename = str(uuid.uuid4())

        filepath = os.path.join(UPLOAD_FOLDER, filename)
        file.save(filepath)

        auto_delete(filepath)
        
        original_name = file.filename
        with open("file_map.txt", "a") as f:
            f.write(f"{filename} -> {original_name}\n")
        
        return f"SUCCESS:{filename}" 

    return render_template_string(HTML)

from flask import send_from_directory

@app.route("/download/<filename>")
def download_file(filename):
    return send_from_directory(UPLOAD_FOLDER, filename, as_attachment=True)

# ---------------- RUN ----------------
if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000)
