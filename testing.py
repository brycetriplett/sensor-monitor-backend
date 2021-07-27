from data import Monitor, session, Device, Sleep
from datetime import datetime
import time


def main():
    with session() as s:
        s.add(
            Device(
                name = 'Test Device',
                oid = '0.0.0.0.0.0.0.0.0',
                response = 'good'
            )
        )

        print(
            "\n\n"
            "Test Device Response Data:\n"
            f"{(device := s.query(Device).filter_by(name='Test Device').first())}"
            "\n\n"
        )

        s.add(
            Monitor(
                ip = '1.1.1.1',
                name = 'test location',
                community = 'public',
                refresh = 60,
                active = True,
                device_id = device.id
            )
        )

        print(
            "\n\n"
            "Test Monitor Response Data:\n"
            f"{(monitor := s.query(Monitor).filter_by(ip='1.1.1.1').first())}"
            "\n\n"
        )

        s.add(
            Sleep(
                ip = monitor.ip,
                time = datetime.now(),
                duration = 30
            )
        )

        print(
            "\n\n"
            "Test Sleep Response Data:\n"
            f"{s.query(Sleep).filter_by(ip=monitor.ip).first()}"
            "\n\n"
        )




if __name__ == '__main__':
    start = datetime.now()
    time.sleep(5)
    end = datetime.now()

    runtime = (end-start).total_seconds()
    if runtime > 4:
        print('the thing works')
