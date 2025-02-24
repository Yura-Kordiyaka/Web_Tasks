class EuropeanSocket:
    def voltage(self):
        return 230


class USASocket:
    def voltage(self):
        return 120


class USBDevice:
    def required_voltage(self):
        return 5


class TypeCDevice:
    def required_voltage(self):
        return 9


class SocketAdapter:
    def __init__(self, socket):
        self.socket = socket

    def get_voltage(self, device):
        socket_voltage = self.socket.voltage()

        if isinstance(device, USBDevice):
            return socket_voltage / 46
        elif isinstance(device, TypeCDevice):
            return socket_voltage / 25
        else:
            raise ValueError("Unknown device type!")


european_socket = EuropeanSocket()
adapter = SocketAdapter(european_socket)

usb_device = USBDevice()
type_c_device = TypeCDevice()

print(f"USB device receives {adapter.get_voltage(usb_device)}V")
print(f"Type-C device receives {adapter.get_voltage(type_c_device)}V")
