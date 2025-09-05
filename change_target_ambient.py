import pathlib
import time

from kuksa_client.grpc import VSSClient
from kuksa_client.grpc import Datapoint

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
        current_values = client.set_target_values({
            "Vehicle.Cabin.Light.AmbientLight.Row1.DriverSide.IsLightOn": Datapoint(True),
            "Vehicle.Cabin.Light.AmbientLight.Row1.DriverSide.Intensity": Datapoint(100),
            "Vehicle.Cabin.Light.AmbientLight.Row1.DriverSide.Color": Datapoint("#ff00af")
        })
        time.sleep(5)
