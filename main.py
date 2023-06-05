import os
from time import sleep
from psutil import sensors_battery
from win11toast import toast

def check_if_battery_percentage_has_changed(func):
    def wrapper(*args, **kwargs):
        last_battery_percentage = 0
        while True:
            battery_percentage = sensors_battery().percent
            if battery_percentage != last_battery_percentage:
                func(battery_percentage)
                last_battery_percentage = battery_percentage

            sleep(0.5)

    return wrapper


@check_if_battery_percentage_has_changed
def send_notification(battery_percentage):
    battery_is_charging = sensors_battery().power_plugged
    if battery_percentage < 20 and not battery_is_charging:
        toast(
            f'Battery charge is {battery_percentage}%',
            'Turn on charging!',
            icon=os.path.dirname(os.path.abspath(__file__))+'\\20-.ico',
            audio=os.path.dirname(os.path.abspath(__file__))+'\\20-80+.wav'
        )
    if battery_percentage == 20 and not battery_is_charging:
        toast(
            f'Battery charge is 20%',
            'Turn on charging!',
            icon=os.path.dirname(os.path.abspath(__file__))+'\\20.ico',
            audio=os.path.dirname(os.path.abspath(__file__))+'\\20.wav'
        )
    if battery_percentage == 80 and battery_is_charging:
        toast(
            f'Battery charge is 80%',
            'Turn off charging!',
            icon=os.path.dirname(os.path.abspath(__file__))+'\\80.ico',
            audio=os.path.dirname(os.path.abspath(__file__))+'\\80.wav'
        )
    if battery_percentage > 80 and battery_is_charging:
        toast(
            f'Battery charge is {battery_percentage}%',
            'Turn off charging!',
            icon=os.path.dirname(os.path.abspath(__file__))+'\\80+.ico',
            audio=os.path.dirname(os.path.abspath(__file__))+'\\20-80+.wav'
        )


def main():
    toast(
        'BatteryNotify is running.',
        icon=os.path.dirname(os.path.abspath(__file__))+'\\icon.ico'
    )
    battery_percentage = sensors_battery().percent
    send_notification(battery_percentage)


if __name__ == '__main__':
    main()

