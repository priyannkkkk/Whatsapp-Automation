from flask import Flask, render_template, request, redirect
from services.supabase_service import supabase
from services.message_service import send_confirmation

app = Flask(__name__)


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/appointment", methods=["POST"])
def create_appointment():
    try:
        customer_name = request.form.get("customer_name")
        phone = request.form.get("phone")
        appointment_time = request.form.get("appointment_time")

        if not customer_name or not phone or not appointment_time:
            return "All fields are required", 400

        supabase.table("appointments").insert({
            "customer_name": customer_name,
            "phone": phone,
            "appointment_time": appointment_time
        }).execute()

        send_confirmation(
            customer_name,
            phone,
            appointment_time
        )

        return redirect("/dashboard")

    except Exception as e:
        return f"Error: {str(e)}", 500


@app.route("/dashboard")
def dashboard():
    try:
        response = (
            supabase
            .table("appointments")
            .select("*")
            .order("created_at", desc=True)
            .execute()
        )

        appointments = response.data

        return render_template(
            "dashboard.html",
            appointments=appointments,
            total=len(appointments)
        )

    except Exception as e:
        return f"Error: {str(e)}", 500


@app.route("/health")
def health():
    return {
        "status": "running"
    }

@app.route("/cancel/<int:appointment_id>", methods=["POST"])
def cancel_appointment(appointment_id):

    supabase.table("appointments").update({
        "status": "Cancelled"
    }).eq(
        "id",
        appointment_id
    ).execute()

    return redirect("/dashboard")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)