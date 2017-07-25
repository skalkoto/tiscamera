from ctypes import *

MAX_CAMERAS = 64

class TcamCamera(Structure):
    _fields_ = [("model_name", c_char * 64),
                ("serial_number", c_char * 64),
                ("current_ip", c_char * 16),
                ("current_gateway", c_char * 16),
                ("current_netmask", c_char * 16),
                ("persistent_ip", c_char * 16),
                ("persistent_gateway", c_char * 16),
                ("persistent_netmask", c_char * 16),
                ("user_defined_name", c_char * 64),
                ("firmware_version", c_char * 64),
                ("mac_address", c_char * 64),
                ("interface_name", c_char * 64),
                ("is_static_ip", c_int),
                ("is_dhcp_enabled", c_int),
                ("is_reachable", c_int),
                ("is_controllable", c_int)
    ]

DISCOVER_CALLBACK_FUNC = CFUNCTYPE(None, TcamCamera)
UPLOAD_CALLBACK_FUNC = CFUNCTYPE(None, c_char_p, c_int)

def _tobytes(value):
    if bytes == str:
        return bytes(value)
    else:
        return bytes(value, "utf-8")

class CameraController:
    def __init__(self):
        try:
            self.dll = cdll.LoadLibrary("libtcam_gigewrapper.so")
        except OSError:
            _path = os.path.dirname(__file__)
            if not _path:
                _path = "."
            self.dll = cdll.LoadLibrary(os.path.join(_path,"libtcam_gigewrapper.so"))
        self.dll.init()
        self.dll.set_persistent_parameter_s.argtypes = [c_char_p, c_char_p, c_char_p]
        self.dll.set_persistent_parameter_i.argtypes = [c_char_p, c_char_p, c_int]
        self.dll.rescue.argtypes = [c_char_p, c_char_p, c_char_p, c_char_p]
        self.dll.upload_firmware.argtypes = [c_char_p, c_char_p, UPLOAD_CALLBACK_FUNC]
        self.cameras = []

    SUCCESS = 0x0
    FAILURE = 0x8000
    NO_DEVICE = 0x8001
    INVALID_PARAMETER = 0x8002

    @staticmethod
    def __getdict(struct):
        d = dict((field, getattr(struct, field)) for field, _ in struct._fields_)
        for f in d:
            if type(d[f]) == bytes:
                d[f] = d[f].decode("utf-8")
        return d

    def __discover_callback(self, camera):
        self.cameras.append(self.__getdict(camera))

    def discover(self, get_persistent_values=False):
        self.cameras = []
        self.dll.get_camera_list(DISCOVER_CALLBACK_FUNC(self.__discover_callback), get_persistent_values)
        return self.cameras

    def set_persistent_parameter(self, identifier, key, value):
        if type(value) == str:
            return self.dll.set_persistent_parameter_s(_tobytes(identifier),
                                                       _tobytes(key),
                                                       _tobytes(value))
        else:
            return self.dll.set_persistent_parameter_i(_tobytes(identifier),
                                                       _tobytes(key), value)

    def upload_firmware(self, identifier, _path, callback):
        return self.dll.upload_firmware(_tobytes(identifier), _tobytes(_path), callback)

    def get_camera_details(self, identifier):
        cam = TcamCamera()
        self.dll.get_camera_details(_tobytes(identifier), byref(cam))
        return self.__getdict(cam)

    def rescue(self, identifier, ip, netmask, gateway):
        mac = None
        for cam in self.cameras:
            if identifier in [cam["serial_number"], cam["user_defined_name"], cam["mac_address"]]:
                if mac is not None:
                    print("Camera identifier is ambiguous")
                    return -2
                mac = cam["mac_address"]

        if mac is None:
            print("No matching camera")
            return -1

        # print("send rescue to: ", mac, ip, netmask, gateway)

        self.dll.rescue(_tobytes(mac), _tobytes(ip), _tobytes(netmask), _tobytes(gateway))
