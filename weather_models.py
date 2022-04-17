import pandas as pd
import numpy as np
from fbprophet import Prophet
import matplotlib.pyplot as plot
import json
from fbprophet.serialize import model_to_json, model_from_json


davis_weather_df = pd.read_csv("cal_weather_df_davis.csv").drop(columns=["Time","type","obs","Wx","Wind dir","speed","dry","Bulb wet","ETo",'RH max',"min.2", "Evap", "none"])
davis_weather_df = davis_weather_df.rename(columns={'min':"Air Temp Min",'min.1':"Soil Temp Min", "Precip":"Precipitation", "Air max":"Air Temp Max", "Air min":"Air temp min", "Solar":"Solar Radiation"})
davis_weather_df['Date'] = pd.to_datetime(davis_weather_df['Date'].astype(str))

yolo_weather_df = pd.read_csv("ad_viz_tile_data.csv")
yolo_weather_df['Date'] = pd.to_datetime(yolo_weather_df['Date'].astype(str))

features = ["Air Temp Min","Soil Temp Min", "Precipitation", "Air Temp Max", "Air Temp Min", "Solar Radiation"]
ylabels = {"Precipitation":"Inches", "Air Temp Max":"Fahrenheit", "Air Temp Min":"Fahrenheit", "Soil Temp Max":"Fahrenheit", "Soil Temp Min":"Fahrenheit", "Solar Radiation":"Langleys"}

def make_model(df, feature):
    data = zip(df['Date'], davis_weather_df[feature])
    prophet_df = pd.DataFrame(data, columns=['ds', 'y'])
    m = Prophet()
    m.fit(prophet_df)
    models[feature] = m
    return m

def save_model(model, feature):
    with open("models/" + feature + '_serialized_model.json', 'w') as fout:
        json.dump(model_to_json(model), fout)  # Save model


def load_model(feature):
    with open("models/" + feature + '_serialized_model.json', 'r') as fin:
        m = model_from_json(json.load(fin))  # Load model
        return m


def save_fig(fig1, fig2, name):
    fig1.savefig("plots/" + name + '.jpg')
    fig2.savefig("plots/" + name + '_trends' + '.jpg')


def make_fig(model, lookahead, title, ylabel, start=None, save=True):
    if lookahead <= 0 or start:
        old_history = model.history
    if lookahead >= 0:
        future = model.make_future_dataframe(periods=lookahead * 365)
        print(future.tail())
        forecast = model.predict(future)
    else:
        hist = model.history
        first_day = hist['ds'].iloc[0]
        last_day = model.history['ds'].iloc[-1] - pd.Timedelta(days=np.abs(lookahead * 365))
        print(len(hist))
        future = hist[(hist['ds'] >= first_day) & (hist['ds'] <= last_day)]
        print(len(future))
        print(future.tail())
        forecast = model.predict(future)
        model.history = model.history[(model.history['ds'] <= last_day)]
    if start:
        start_dt = pd.to_datetime("01/01/" + str(start))
        forecast = forecast[(forecast['ds'] >= start_dt)]
        model.history = model.history[(model.history['ds'] >= start_dt)]
        
    print(forecast[['ds', 'yhat', 'yhat_lower', 'yhat_upper']].tail())
    print(title)
    fig1 = model.plot(forecast, xlabel='Date', ylabel=ylabel)
    fig1.suptitle(title)
    fig2 = model.plot_components(forecast)
    if start:
        model.history = old_history
    if save:
        save_fig(fig1, fig2, title)
    return fig1, fig2

def run_model(feature, lookahead, start=None):
	if feature == "AQI Value":
		data = zip(yolo_weather_df['Date'], yolo_weather_df[" AQI Value"])
		prophet_df = pd.DataFrame(data, columns=['ds', 'y'])
		feature = "AQI Value"

		try:
		    yolo_m = load_model(feature)
		    print("Successfully loaded model", feature)
		except:
		    print("Couldn't load model", feature)
		    yolo_m = Prophet()
		    yolo_m.fit(prophet_df)
		    save_model(yolo_m, feature)
		make_fig(yolo_m, lookahead, "AQI Value", "AQI", start=start)
	else:
		try:
		    m = load_model(feature)
		    models[feature] = m
		    print("Successfully loaded model", feature)
		except:
		    print("Couldn't load model", feature)
		    m = make_model(davis_weather_df, feature)
		    save_model(m, feature)
		make_fig(m, lookahead, feature, ylabels[feature], start=start)