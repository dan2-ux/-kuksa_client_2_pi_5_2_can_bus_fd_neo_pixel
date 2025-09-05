import pathlib
import time
import subprocess

from kuksa_client.grpc import Datapoint
from kuksa_client.grpc import VSSClient

on_off = "Vehicle.Cabin.Light.AmbientLight.Row1.DriverSide.IsLightOn"
intent = "Vehicle.Cabin.Light.AmbientLight.Row1.DriverSide.Intensity"
color = "Vehicle.Cabin.Light.AmbientLight.Row1.DriverSide.Color"

#l_on_off = False
l_intent = 0
l_color = 0x000000

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
        target_value = client.get_target_values([on_off,intent,color])
        if (target_value[on_off] is not None or
            target_value[intent] is not None or
            target_value[color] is not None):
            if target_value[on_off].value == True: # and target_value[on_off].value != l_on_off :
                client.set_current_values({
                    on_off: Datapoint(target_value[on_off].value)
                })
                #l_on_off = client.get_current_values(["Vehicle.Speed"])
                if target_value[intent].value != l_intent:
                    client.set_current_values({
                        intent: Datapoint(target_value[intent].value)
                    })
                    scaled = round(target_value[intent].value * 255 / 100)
                    l_intent = target_value[intent].value
                if target_value[color].value != l_color:
                    client.set_current_values({
                        color: Datapoint(target_value[color].value)
                    })
                    l_color = target_value[color].value
                subprocess.run(
                    ["cansend", "can0", f"123#01.{target_value[color].value.lstrip("#")}.{scaled:02X}"]
                )
            elif target_value[on_off].value == False:
                print("Ambient Light is Off")
                subprocess.run(
                        ["cansend", "can0", f"123#00.00.00.00.00"]
                    )

        time.sleep(1)
