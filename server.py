from flask import Flask, render_template, request
import requests

app = Flask(__name__)

def beaufort_scale(wind_speed):
    if wind_speed < 0.3:
        return "Calm"
    elif wind_speed < 1.6:
        return "Light air"
    elif wind_speed < 3.4:
        return "Light breeze"
    elif wind_speed < 5.5:
        return "Gentle breeze"
    elif wind_speed < 8.0:
        return "Moderate breeze"
    elif wind_speed < 10.8:
        return "Fresh breeze"
    elif wind_speed < 13.9:
        return "Strong breeze"
    elif wind_speed < 17.2:
        return "Near gale"
    elif wind_speed < 20.8:
        return "Gale"
    elif wind_speed < 24.5:
        return "Strong gale"
    elif wind_speed < 28.5:
        return "Storm"
    elif wind_speed < 32.7:
        return "Violent storm"
    else:
        return "Hurricane"

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        user_input = request.form.get("user_input")

        # Perform the weather API request and data processing
        BASE_URL = "https://api.openweathermap.org/data/2.5/weather"
        CITY = user_input
        API_KEY = "your_api_key"  # Replace with your OpenWeatherMap API key

        params = {
            "q": CITY,
            "appid": "578a54a68b3bc63868efdd07292723a0"
        }

        response = requests.get(BASE_URL, params=params)
        data = response.json()

        main = data.get("main")

        if main is not None:
            temperature = main.get("temp")
            feels_like = main.get("feels_like")
            humidity = main.get("humidity")
            pressure = main.get("pressure")

            if temperature is not None:
                temperature = round(temperature - 273.15, 2)
            else:
                temperature = None

            if feels_like is not None:
                feels_like = round(feels_like - 273.15, 2)
            else:
                feels_like = None

            weather_report = data.get("weather")
            if weather_report is not None:
                report = weather_report[0].get("description")
            else:
                report = None

            wind_report = data.get("wind")
            if wind_report is not None:
                wind_speed = wind_report.get("speed")
            else:
                wind_speed = None

            timezone_offset = data.get('timezone')
            from datetime import datetime
            import pytz

            timezone = pytz.FixedOffset(timezone_offset // 60)
            current_time = datetime.now(timezone)
            current_time_string = current_time.strftime("%H:%M:%S")

            return render_template(
                "index.html",
                c=user_input,
                te=temperature,
                f=feels_like,
                h=humidity,
                p=pressure,
                r=report,
                w=wind_speed,
                b=f'{wind_speed}: {beaufort_scale(wind_speed)}',
                ti=current_time_string
            )

    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)
