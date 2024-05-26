# SensorApp/views.py

from django.shortcuts import render
from SmartHospitalSystem.models import Sensor_List_int
from SmartHospitalSystem.models import Actuator_List
from datetime import datetime
import paho.mqtt.client as mqtt
import pandas as pd
import numpy as np
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score

# List of sensor names (assuming they are the same as the sensor topics)
sensor_names = ["IV_level_sensor", "heart_beat_sensor", "flourescent_based_sensor",
                "camera_sensor", "UV-C_sensor", "thermal_sensor", "room_pressure_sensor",
                "temperature_sensor", "humidity_sensor"]
actuator_names = ["Alert", "IV_flow_regulator", "Insulin_pump",
                "Laser_pointer", "Door_lock", "Disinfectant_spray", "Electric_damper", "HVAC_system", "Alarm"]
# Global dictionary to store the latest sensor data for each sensor
latest_sensor_data_dict = {}

# Global list to store the last 100 sensor readings
sensor_data_history_list = []
historical_sensor_data_dict = {sensor_name: [] for sensor_name in sensor_names}

def on_connect(client, userdata, flags, rc, ):
    print("Connected with result code " + str(rc))

    # Subscribe to topics for all sensors
    for sensor_name in sensor_names:
        client.subscribe(sensor_name)

def on_message(client, userdata, msg):
    global sensor_data_history_list

    sensor_name = msg.topic
    latest_sensor_data = float(msg.payload.decode())

    # Add the latest sensor data to the history list
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    sensor_data_history_list.append({'sensor_name': sensor_name, 'data': latest_sensor_data, 'timestamp': current_time})

    # Keep only the last 100 sensor readings in the list
    sensor_data_history_list = sensor_data_history_list[-20:]

    # Update the latest sensor data in the dictionary
    latest_sensor_data_dict[sensor_name] = latest_sensor_data
    historical_sensor_data_dict[sensor_name].append({'data': latest_sensor_data, 'timestamp': current_time})
    historical_sensor_data_dict[sensor_name] = historical_sensor_data_dict[sensor_name][-20:]

# Set up the MQTT client
mqtt_client = mqtt.Client()
mqtt_client.on_connect = on_connect
mqtt_client.on_message = on_message
mqtt_broker_address = "127.0.0.1"
mqtt_client.connect(mqtt_broker_address, 1889)
mqtt_client.loop_start()

def update_page(request):
    result_true_1_list = []
    result_true_2_list = []
    result_true_3_list = []
    global sensor_data_history_list

    # Update Sensor_List_int objects
    for sensor_name in sensor_names:
        if sensor_name in latest_sensor_data_dict:
            latest_sensor_data = latest_sensor_data_dict[sensor_name]

            sensor = Sensor_List_int.objects.get(name=sensor_name)
            sensor.Data = latest_sensor_data
            current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            sensor.timestamp = current_time
            sensor.save()
            
    # Retrieve Sensor_List_int and Actuator_List objects for rendering
    sensors = Sensor_List_int.objects.all()

    # Update Actuator_List objects
    actuators = Actuator_List.objects.all()

    # Divide the sensors and actuators into three equal parts
    num_sensors = len(sensors)
    num_actuators = len(actuators)

    sensors_per_table = num_sensors // 3
    actuators_per_table = num_actuators // 3    
    sensors_table1 = sensors[:sensors_per_table]
    sensors_table2 = sensors[sensors_per_table:2 * sensors_per_table]
    sensors_table3 = sensors[2 * sensors_per_table:]

    actuators_table1 =  actuators[:actuators_per_table]
    actuators_table2 = actuators[actuators_per_table:2 * actuators_per_table]
    actuators_table3 = actuators[2 * actuators_per_table:]

    for actuator in actuators_table1:
        df = pd.read_csv("C:/Calvin Institute of Technology/2023 (Semester 5)/Pemrograman Web Berbasis IoT/M13 - Proyek - Martin_Moses/Project_UAS/csv/" + str(actuator) + ".csv")

        sensor_names_table1 = [sensor.name for sensor in sensors_table1]
        features = df[sensor_names_table1]
        target = df[str(actuator)]

        X_train, X_test, y_train, y_test = train_test_split(features, target, test_size=0.2, random_state=42)

        # Create a logistic regression model
        model = LogisticRegression()

        # Train the model
        model.fit(X_train, y_train)

        # Make predictions on the test set
        predictions = model.predict(X_test)

        # Calculate accuracy (you might want to store or log this value for evaluation)
        accuracy = accuracy_score(y_test, predictions)

        # Use the latest sensor data for prediction
        #new_data = [[latest_sensor_data_dict[sensor] for sensor in features.columns]]

        new_data = pd.DataFrame( 
        np.array([[latest_sensor_data_dict[sensor] for sensor in features.columns]]).reshape(1, -1), 
        columns=['IV_level_sensor', 'heart_beat_sensor', 'flourescent_based_sensor'] 
    )
        result = model.predict(new_data)

        actuator.Data = result[0]
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        actuator.timestamp = current_time
        actuator.save()
        
        result_true_1_list.append(result[0])
        #print(f'{actuator} : {new_data} results in {result} with an accuracy of {accuracy}')

    for actuator in actuators_table2:
        df = pd.read_csv("C:/Calvin Institute of Technology/2023 (Semester 5)/Pemrograman Web Berbasis IoT/M13 - Proyek - Martin_Moses/Project_UAS/csv/" + str(actuator) + ".csv")

        sensor_names_table2 = [sensor.name for sensor in sensors_table2]
        features = df[sensor_names_table2]
        target = df[str(actuator)]

        X_train, X_test, y_train, y_test = train_test_split(features, target, test_size=0.2, random_state=42)

        # Create a logistic regression model
        model = LogisticRegression()

        # Train the model
        model.fit(X_train, y_train)

        # Make predictions on the test set
        predictions = model.predict(X_test)

        # Calculate accuracy (you might want to store or log this value for evaluation)
        accuracy = accuracy_score(y_test, predictions)

        # Use the latest sensor data for prediction
        new_data = pd.DataFrame( 
        np.array([[latest_sensor_data_dict[sensor] for sensor in features.columns]]).reshape(1, -1), 
        columns=['camera_sensor', 'UV-C_sensor', 'thermal_sensor'] 
    )
        result = model.predict(new_data)

        actuator.Data = result[0]

        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        actuator.timestamp = current_time
        actuator.save()
        
        result_true_2_list.append(result[0])

    for actuator in actuators_table3:
        df = pd.read_csv("C:/Calvin Institute of Technology/2023 (Semester 5)/Pemrograman Web Berbasis IoT/M13 - Proyek - Martin_Moses/Project_UAS/csv/" + str(actuator) + ".csv")

        sensor_names_table3 = [sensor.name for sensor in sensors_table3]
        features = df[sensor_names_table3]
        target = df[str(actuator)]

        X_train, X_test, y_train, y_test = train_test_split(features, target, test_size=0.2, random_state=42)

        # Create a logistic regression model
        model = LogisticRegression()

        # Train the model
        model.fit(X_train, y_train)

        # Make predictions on the test set
        predictions = model.predict(X_test)

        # Calculate accuracy (you might want to store or log this value for evaluation)
        accuracy = accuracy_score(y_test, predictions)

        # Use the latest sensor data for prediction
        new_data = pd.DataFrame( 
        np.array([[latest_sensor_data_dict[sensor] for sensor in features.columns]]).reshape(1, -1), 
        columns=['room_pressure_sensor', 'temperature_sensor', 'humidity_sensor'] )

        actuator.Data = result[0]

        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        actuator.timestamp = current_time
        actuator.save()
        
        result_true_3_list.append(result[0])

    last_20_sensor_data_per_sensor = {sensor_name: [entry['data'] for entry in historical_sensor_data_dict[sensor_name]] for sensor_name in sensor_names}

    historical_sensors = {sensor_name: Sensor_List_int.history.all().filter(name=sensor_name) for sensor_name in sensor_names}
    historical_actuators = {actuator_name: Actuator_List.history.all().filter(name=actuator_name) for actuator_name in actuator_names}

    return render(request, 'SmartHospitalSystem/base.html', {
        'sensors_table1': sensors_table1,
        'sensors_table2': sensors_table2,
        'sensors_table3': sensors_table3,
        'actuators_table1': actuators_table1,
        'actuators_table2': actuators_table2,
        'actuators_table3': actuators_table3,
        'last_100_sensor_data': last_20_sensor_data_per_sensor,
        'result_true_1_list': result_true_1_list,
        'result_true_2_list': result_true_2_list,
        'result_true_3_list': result_true_3_list,
        'historical_sensors': historical_sensors,
        'historical_actuators': historical_actuators,
    })