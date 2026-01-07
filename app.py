from flask import Flask, request, render_template_string, make_response

app = Flask(__name__)

HOME_HTML = """
<!doctype html>
<html>
<head>
  <meta charset="utf-8">
  <title>Mini Burp CTF</title>
  <style>
    body { font-family: system-ui, sans-serif; margin: 24px; }
    .card { border: 1px solid #ddd; border-radius: 12px; padding: 16px; max-width: 780px; }
    input { width: 100%; padding: 8px; margin: 8px 0; }
    button { padding: 10px 12px; }
    a { display:block; margin: 8px 0; }
    .hint { color: #666; font-size: 14px; }
    code { background:#f6f6f6; padding:2px 6px; border-radius:6px; }
  </style>
</head>
<body>
  <div class="card">
    <h1>Mini Burp CTF</h1>
    <p class="hint">Use Burp and find FLAG.</p>
    <h2>1) Login Tampering</h2>
    <p class="hint">
      Goal: Login as <code>admin</code> with right <code>access_level</code>.
    </p>
    <form method="POST" action="/login">
      <label>user</label>
      <input name="user" value="guest">

      <!-- hidden field -->
      <input type="hidden" name="access_level" value="1">

      <button type="submit">Login</button>
    </form>

    <hr>

    <h2>2) Cookie + Method</h2>
    <p class="hint">
      Start here: <a href="/challenge/cookie">/challenge/cookie</a>
    </p>

    <h2>3) User-Agent</h2>
    <p class="hint">
      Start here: <a href="/challenge/header">/challenge/header</a>
    </p>
  </div>
</body>
</html>
"""

@app.get("/")
def index():
    return render_template_string(HOME_HTML)

# ---------- 1) Login Tampering ----------
@app.post("/login")
def login():
    user = request.form.get("user", "")
    access_level = request.form.get("access_level", "")

# You can keep this simple; players will use Repeater + Intruder
    if user == "admin" and access_level == "9":
        return "FLAG{admin_and_level9}"
    return "Access denied. Please make sure you have right access level."

# ---------- 2) Cookie + Method ----------
@app.route("/challenge/cookie", methods=["GET", "POST"])
def cookie_plus_method():
    """
    GET: sets role=guest cookie and shows instructions.
    POST: returns flag only if role=admin cookie is present.
    """
    role = request.cookies.get("role")

    # Winning condition: must be POST + cookie role=admin
    if request.method == "POST" and role == "admin":
        return "FLAG{cookie_and_method}"

    if request.method == "GET":
        resp = make_response("""
Use Burp repeater to resend this endpoint as POST, not GET. Also make sure cookie role is admin.

""".strip())
        resp.set_cookie("role", "guest", httponly=False)
        return resp

    # POST but wrong/missing cookie
    return "Nope. (Hint: method + cookie both matter.)"

# ---------- 3) User-Agent ----------
@app.get("/challenge/header")
def ua_challenge():
    """
    Keep it simple, or add a light extra condition if you want.
    """
    ua = request.headers.get("User-Agent", "")

    if "CTF" in ua:
        resp = make_response("""
Looks great! Did you check the response headers?               
                             
                             """.strip())
        resp.headers["X-CTF-FLAG"] = "FLAG{user_agent_header_modified}"
        return resp

    return """
Send a request where the User-Agent header contains <code>CTF</code> using Burp Repeater.
""".strip()

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=True)