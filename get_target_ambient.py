import pathlib
import time
from kuksa_client.grpc import VSSClient

on_off = "Vehicle.Cabin.Light.AmbientLight.Row1.DriverSide.IsLightOn"
intensity = "Vehicle.Cabin.Light.AmbientLight.Row1.DriverSide.Intensity"
color = "Vehicle.Cabin.Light.AmbientLight.Row1.DriverSide.Color"

with VSSClient(
    "localhost",
    55555,
    root_certificates=pathlib.Path("/home/dev/token/CA.pem"),
    token=pathlib.Path("/home/dev/token/provide-all.token")
    .expanduser()
    .read_text(encoding="utf-8")
    .strip(),
) as client:
    while True:
        current_values = client.get_target_values([on_off, intensity, color])

        if (current_values[on_off] is not None and
            current_values[intensity] is not None and
            current_values[color] is not None):

            print(on_off, current_values[on_off].value)
            print(intensity, current_values[intensity].value)
            print(color, current_values[color].value)
            print("-" * 90)
        else:
            print("Ambient is empty")

        time.sleep(1)
