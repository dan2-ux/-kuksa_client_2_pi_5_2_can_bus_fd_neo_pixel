import pathlib
import time

from kuksa_client.grpc import VSSClient

#import aiohttp
#import socketio

# print("Hello")

with VSSClient(
    "localhost",
    55555,
    root_certificates=pathlib.Path("/home/dev/token/CA.pem"),
    token=pathlib.Path("/home/dev/token/provide-all.token")
    .expanduser()
    .read_text(encoding="utf-8")
    .rstrip("\n"),
) as client:
    while True:
        current_values = client.get_current_values([
            "Vehicle.Cabin.Light.AmbientLight.Row1.DriverSide.IsLightOn",
            "Vehicle.Cabin.Light.AmbientLight.Row1.DriverSide.Intensity",
            "Vehicle.Cabin.Light.AmbientLight.Row1.DriverSide.Color"
            ])
        if current_values["Vehicle.Cabin.Light.AmbientLight.Row1.DriverSide.IsLightOn"] is not None and current_values["Vehicle.Cabin.Light.AmbientLight.Row1.DriverSide.Intensity"] is not None and current_values["Vehicle.Cabin.Light.AmbientLight.Row1.DriverSide.Color"] is not None :
            print("Vehicle.Cabin.Light.AmbientLight.Row1.DriverSide.IsLightOn:", 
                  current_values["Vehicle.Cabin.Light.AmbientLight.Row1.DriverSide.IsLightOn"].value)
            print("Vehicle.Cabin.Light.AmbientLight.Row1.DriverSide.Intensity", 
                  current_values["Vehicle.Cabin.Light.AmbientLight.Row1.DriverSide.Intensity"].value)
            print("Vehicle.Cabin.Light.AmbientLight.Row1.DriverSide.Color", 
                  current_values["Vehicle.Cabin.Light.AmbientLight.Row1.DriverSide.Color"].value)
            print("----------------------------------------------------------------------------------")
        else:
            print("Ambient is empty")

        time.sleep(5)