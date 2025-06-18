# app.py

from flask import Flask, render_template, request
import plotly.express as px
import plotly.io as pio
from weather import get_data
import pandas as pd


app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])  # ✅ Missing route added
def index():
    place = days = option = chart_html = None
    sky_images = []

    if request.method == 'POST':
        place = request.form.get('place')
        days = int(request.form.get('days'))
        option = request.form.get('option')

        if place:
            filtered_data = get_data(place, forecast_days=days)

        if option == "Temperature":
            try:
                temperatures = [round(item["main"]["temp"] - 273.15, 2) for item in filtered_data]
                dates = [item["dt_txt"] for item in filtered_data]
                df = pd.DataFrame({
                    "Date": dates,
                    "Temperature (°C)": temperatures
                })
                fig = px.line(df, x=dates, y=temperatures,
                              labels={"x": "Date", "y": "Temperature (°C)"},
                              title=f"Temperature Forecast for {place}")
                chart_html = pio.to_html(fig, full_html=False)
            except Exception as e:
                chart_html = f"<p>Error plotting temperature data: {e}</p>"

        elif option == "Sky":
            images = {
                "Clear": "images/clear.png",
                "Clouds": "images/cloud.png",
                "Rain": "images/rain.png",
                "Snow": "images/snow.png"
            }
            for item in filtered_data:
                condition = item["weather"][0]["main"]
                img_path = images.get(condition, "images/clear.png")
                sky_images.append({
                    "datetime": item["dt_txt"],
                    "condition": condition,
                    "img_path": img_path
                })

    return render_template('index.html',
                           place=place,
                           days=days,
                           option=option,
                           chart_html=chart_html,
                           sky_images=sky_images)

if __name__ == '__main__':
    app.run(debug=True, use_reloader=False)
