from tkinter import BOTH, Tk, Frame, messagebox, Label
from tkinter.ttk import Combobox, Button, Style, LabelFrame
import threading
import time

from utils_riego import find_available_serial_ports
from serial_sensor_riego import BAUDRATES
from serial_sensor_riego import SerialSensor

class App(Frame):
    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.parent: Tk = parent
        self.serial_device: SerialSensor | None = None

        # Establecer el estilo
        style = Style()
        style.configure('TButton', font=('Helvetica', 12), padding=10)
        style.configure('TLabel', font=('Helvetica', 14))
        style.configure('TCombobox', font=('Helvetica', 12))
        style.configure('Custom.TLabelFrame.Label', font=('Helvetica', 16, 'bold'))

        # Crear todos los componentes gráficos
        self.serial_frame = self._create_serial_frame()
        self.humidity_frame = self._create_humidity_frame()

        self.init_gui()

    def init_gui(self) -> None:
        self.parent.title('SistemaRiego')
        self.parent.geometry('600x400')
        self['bg'] = 'lightgrey'
        self.pack(expand=True, fill=BOTH)

        # Colocar los frames
        self.serial_frame.grid(row=0, column=0, padx=20, pady=20, sticky='ew')
        self.humidity_frame.grid(row=2, column=0, padx=20, pady=20, sticky='ew')

        # Ajustar las columnas
        self.columnconfigure(0, weight=1)

    def refresh_serial_devices(self) -> None:
        ports = find_available_serial_ports()
        self.serial_devices_combobox['values'] = ports
        
    def connect_serial_device(self) -> None:
        # Ejecutar la conexión en un hilo separado
        threading.Thread(target=self._connect_serial_device).start()

    def _connect_serial_device(self) -> None:
        try:
            baudrate = int(self.baudrate_combobox.get())
            port = self.serial_devices_combobox.get()
            if port == '':
                messagebox.showerror('Port not selected', 'Please select a valid port.')
                return
            self.serial_device = SerialSensor(port=port, baudrate=baudrate)
            time.sleep(2)  # Simulación del tiempo de conexión (eliminar si no es necesario)
            messagebox.showinfo('Connection', 'Serial device connected successfully.')
        except ValueError:
            messagebox.showerror('Wrong baudrate', 'This baudrate is not valid.')
            return
        except Exception as e:
            messagebox.showerror('Connection error', f"An error occurred: {e}")

    def read_humidity(self) -> None:
        if self.serial_device is not None:
            humidity = self.serial_device.send('HC2')
            self.humidity_label['text'] = f"{humidity[1:-2]} %"  # Ajustar según el formato de salida del sensor
            return
        messagebox.showerror(title='Serial connection Error', message='Serial Device not initialized.')


    def _create_serial_frame(self) -> LabelFrame:
        frame = LabelFrame(self, text='Serial Connection', padding=20)
        self.serial_devices_combobox = Combobox(frame, values=find_available_serial_ports(), font=("Courier", 14))
        self.refresh_serial_devices_button = Button(frame, text="Refresh", command=self.refresh_serial_devices, style='TButton')
        self.baudrate_combobox = Combobox(frame, values=['BAUDRATE'] + BAUDRATES, font=("Courier", 14))
        self.connect_button = Button(frame, text='Connect', command=self.connect_serial_device, style='TButton')

        # Organizar los widgets dentro del frame
        self.serial_devices_combobox.grid(row=0, column=0, padx=5, pady=5, sticky='ew')
        self.refresh_serial_devices_button.grid(row=0, column=1, padx=5, pady=5)
        self.baudrate_combobox.grid(row=1, column=0, padx=5, pady=5, sticky='ew')
        self.connect_button.grid(row=1, column=1, padx=5, pady=5)

        # Ajustar las columnas
        frame.columnconfigure(0, weight=1)

        return frame

    def _create_humidity_frame(self) -> LabelFrame:
        frame = LabelFrame(self, text='Humidity Reading', padding=20)
        self.humidity_label = Label(frame, text='XX %', foreground='blue', font=("Courier", 20))
        self.read_humidity_button = Button(frame, text='Read humidity', command=self.read_humidity)
       
        # Organizar los widgets dentro del frame
        self.humidity_label.grid(row=0, column=0, padx=5, pady=5)
        self.read_humidity_button.grid(row=0, column=1, padx=5, pady=5)
       
        return frame

root = Tk()

if __name__ == '__main__':
    ex = App(root)
    root.mainloop()
