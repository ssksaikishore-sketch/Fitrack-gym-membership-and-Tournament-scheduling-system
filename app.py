
from flask import Flask, request, render_template_string
from datetime import date, timedelta

app = Flask(__name__)

html = """
<style>
body { font-family: Arial; background: #f2f5f9; margin: 40px; }
h1 { color: #1769aa; }
input, select { padding: 8px; margin: 5px; }
button { padding: 10px 16px; background: #1769aa; color: white; }
form {
  background: white;
  padding: 20px;
  max-width: 500px;
}
h3 { color: #444; }
p { font-size: 16px; }
button:hover { background: #0d4f85; }
select { padding: 8px; }
</style>
<h1>FitTrack</h1>
<h3>Gym Membership and Access Management System</h3>
<form method="POST">
Member Name: <input name="name" required><br><br>
Member ID: <input name="mid" required><br><br>
Membership Type:
<select name="plan">
<option>Monthly</option><option>Quarterly</option>
<option>Yearly</option></select><br><br>
Start Date: <input type="date" name="start" required><br><br>
<button type="submit">Check Gym Access</button>
</form>
{% if result %}
<h2>Membership Details</h2>
<p>Name: {{ name }}</p>
<p>Member ID: {{ mid }}</p>
<p>Plan: {{ plan }}</p>
<p>Expiry Date: {{ expiry }}</p>
<h2>{{ result }}</h2>
{% endif %}
"""

@app.route("/", methods=["GET", "POST"])
def home():
    result = expiry = name = mid = plan = ""
    if request.method == "POST":
        name = request.form["name"]
        mid = request.form["mid"]
        plan = request.form["plan"]
        start = date.fromisoformat(request.form["start"])
        days = {"Monthly": 30, "Quarterly": 90, "Yearly": 365}
        expiry_date = start + timedelta(days=days[plan])
        expiry = expiry_date.strftime("%d-%m-%Y")
        result = "ACCESS GRANTED" if start <= date.today() <= expiry_date else "ACCESS DENIED"
    return render_template_string(html, result=result, name=name, mid=mid,
                                   plan=plan, expiry=expiry)

if __name__ == "__main__":
    app.run(debug=True)
