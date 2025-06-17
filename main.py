from flask import Flask, render_template, request
import plotly.express as px
import plotly.io as pio

app = Flask(__name__)

def get_data(days):
    dates = ["2022-10-25", "2022-10-26", "2022-10-27"]
    temperatures = [10, 11, 15]
    temperatures = [days * temp for temp in temperatures]
    return dates, temperatures

@app.route('/', methods=['GET', 'POST'])
def index():
    place = days = option = chart_html = None

    if request.method == 'POST':
        place = request.form.get('place')
        days = int(request.form.get('days'))
        option = request.form.get('option')

        if option == "Temperature":
            d, t = get_data(days)
            fig = px.line(x=d, y=t, labels={"x": "Date", "y": "Temperature (°C)"},
                          title=f"Temperature Forecast for {place}")
            chart_html = pio.to_html(fig, full_html=False)

    return render_template('index.html',
                           place=place,
                           days=days,
                           option=option,
                           chart_html=chart_html)

if __name__ == '__main__':
    app.run(debug=True)
