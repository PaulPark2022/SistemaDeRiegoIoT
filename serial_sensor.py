
import time

import serial 

BAUDRATES = [ # Velocidad a la que se reciben o envian los caracteres
    2400,
    4800, 
    9600, 
    19200, 
    38400, 
    57600, 
    115200
]

class SerialSensor:
    
    
    def __init__(self,
                 port: str,
                 baudrate: int = 115200,
                 timeout: float = 2.,
                 connection_time: float = 3.,
                 reception_time: float = .5
        ) -> None:
        self._serial = serial.Serial(
            port=port,
            baudrate=baudrate,
            timeout=timeout
        )
        self.connection_time = connection_time
        self.reception_time = reception_time
        time.sleep(connection_time)
        received = self.send('OK')
        
    def send(self, to_send:str) -> str:
        self._serial.write(to_send.encode('utf-8'))
        time.sleep(self.reception_time)
        received = self._serial.readline()
        return received.decode(encoding='utf-8')
    
    def receive(self,) -> str:
        received = self._serial.readline()
        return received.decode(encoding='utf-8')
    
    def close(self) -> None:
        self._serial.close()
    
    def __str__(self) -> str:
        return f"SerialSensor({self._serial=}, {self.connection_time=}, {self.reception_time=})"
    
    def __repr__(self) -> str:
        return f"SerialSensor({self._serial=}, {self.connection_time=}, {self.reception_time=})"
    
    def __del__(self) -> None:
        self.close()