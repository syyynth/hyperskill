import os
import secrets
import sys
from datetime import datetime, timedelta

import requests
from flask import Flask, flash, redirect, render_template, request
from sqlalchemy import create_engine, select
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, sessionmaker


class Base(DeclarativeBase):
    pass


class City(Base):
    __tablename__ = 'city'

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(unique=True, nullable=False)


DB_PATH = '/weather.db'
engine = create_engine(f'sqlite://{DB_PATH}', echo=True)
Session = sessionmaker(bind=engine)

app = Flask(__name__)
app.config['SECRET_KEY'] = secrets.token_hex()


def get_weather_data(city):
    key = os.getenv('OPEN_WEATHER_API')
    units = 'metric'
    url = f'https://api.openweathermap.org/data/2.5/weather?q={city}&appid={key}&units={units}'
    data = requests.get(url).json()

    if data['cod'] == 200:
        state = data['weather'][0]['main']
        degrees = data['main']['temp']
        timestamp = data['dt']
        timezone = data['timezone']
        city = data['name']

        return {
            'time_of_day': get_time_of_day(timestamp, timezone),
            'degrees': degrees,
            'state': state,
            'city': city
        }
    return {}


def get_time_of_day(timestamp, timezone_offset):
    time = datetime.fromtimestamp(timestamp) + timedelta(seconds=timezone_offset)

    if 0 <= time.hour < 7:
        return 'night'
    if 12 <= time.hour < 19:
        return 'day'
    return 'evening-morning'


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        process_city()

    weather_data = get_cities_weather()
    return render_template('index.html', cards=weather_data)


def process_city():
    city_name = request.form.get('city_name', None)

    with Session() as session:
        stmt = select(City).filter_by(name=city_name.lower())
        existing_city = session.execute(stmt).scalar()

    if existing_city is None:
        weather_data = get_weather_data(city_name)

        if weather_data:
            with Session.begin() as session:
                new_city = City(name=city_name.lower())
                session.add(new_city)
        else:
            flash("The city doesn't exist!")
    else:
        flash('The city has already been added to the list!')


def get_cities_weather():
    with Session() as session:
        cities = session.execute(select(City)).scalars().all()

    weather_data = [get_weather_data(city.name) for city in cities]
    return weather_data


@app.route('/api/remove', methods=['POST'])
def remove():
    city_id = request.form.get('id', None)

    if city_id:
        with Session.begin() as session:
            city_to_remove = session.execute(select(City).filter_by(name=city_id.lower())).scalar()
            if city_to_remove:
                session.delete(city_to_remove)

    return redirect('/')


if __name__ == '__main__':
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)

    if len(sys.argv) > 1:
        arg_host, arg_port = sys.argv[1].split(':')
        app.run(host=arg_host, port=arg_port)
    else:
        app.run(host='0.0.0.0', debug=True)
