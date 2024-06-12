/*
 * autoriego.c
 *
 * Created: 11/06/2024 09:57:24 p. m.
 * Author: diego
 */

/*
 * SistemaRiego.c
 *
 * Created: 6/11/2024 9:35:29 AM
 * Author: pablo
 */

#include <io.h>
#include <mega328p.h>  
#include <delay.h>
#include <stdio.h>

//Valores de totalmente seco y totalmente humedo que da el sensor de humedad del suelo 

#define VALOR_SECO 1023    // Valor del sensor cuando el suelo está seco
#define VALOR_HUMEDO 272   // Valor del sensor cuando el suelo está completamente húmedo


// ADC Voltage Reference: AVCC pin
#define ADC_VREF_TYPE ((0<<REFS1) | (1<<REFS0) | (0<<ADLAR)) // El ultimo se desactiva si no usas 8 bits    

// Read the AD conversion result
// Read Voltage=read_adc*(Vref/1024.0)
unsigned int read_adc(unsigned char adc_input) 
{
    ADMUX = adc_input | ADC_VREF_TYPE;
    // Delay needed for the stabilization of the ADC input voltage
    delay_us(10);
    // Start the AD conversion
    ADCSRA |= (1<<ADSC);
    // Wait for the AD conversion to complete
    while ((ADCSRA & (1<<ADIF)) == 0);
    ADCSRA |= (1<<ADIF);
    return ADCW;
}

unsigned int humedadDigital;
unsigned char porEnt;
int porcentajeHumedad;

int mates(int x, int in_min, int in_max, int out_min, int out_max) {
    return (x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min;
}

void main(void)
{
    // ADC initialization
    // ADC Clock frequency: 250.000 kHz
    // ADC Auto Trigger Source: Software
    // Only the 8 most significant bits of
    // the AD conversion result are used
    ADCSRA = (1<<ADEN) | (0<<ADSC) | (0<<ADATE) | (0<<ADIF) | (0<<ADIE) | (1<<ADPS2) | (0<<ADPS1) | (1<<ADPS0);
    ADCSRB = (0<<ADTS2) | (0<<ADTS1) | (0<<ADTS0); // Estas dos lineas cambiaran segun la frecuencia
    // Digital input buffers on ADC0: On, ADC1: On, ADC2: On, ADC3: On
    // ADC4: On, ADC5: Off
    DIDR0 = (1<<ADC5D) | (0<<ADC4D) | (0<<ADC3D) | (0<<ADC2D) | (0<<ADC1D) | (0<<ADC0D);   
    // Desactiva bits con un 1 si quieres entradas analógicas y digitales 
    
    // USART initialization
    // Communication Parameters: 8 Data, 1 Stop, No Parity
    // USART Receiver: On
    // USART Transmitter: On
    // USART Mode: Asynchronous
    // USART Baud Rate: 9600 (Double Speed Mode)
    UCSR0A=(0<<RXC0) | (0<<TXC0) | (0<<UDRE0) | (0<<FE0) | (0<<DOR0) | (0<<UPE0) | (1<<U2X0) | (0<<MPCM0);
    UCSR0B=(0<<RXCIE0) | (0<<TXCIE0) | (0<<UDRIE0) | (1<<RXEN0) | (1<<TXEN0) | (0<<UCSZ02) | (0<<RXB80) | (0<<TXB80);
    UCSR0C=(0<<UMSEL01) | (0<<UMSEL00) | (0<<UPM01) | (0<<UPM00) | (0<<USBS0) | (1<<UCSZ01) | (1<<UCSZ00) | (0<<UCPOL0);
    UBRR0H=0x00;
    UBRR0L=0x0C;
    
    DDRD.2 = 1;  
    PORTD.2 = 0;
    
    while (1)
    {
        humedadDigital = read_adc(0); // leer adc usando el puerto 0 
        // Convierte el valor del sensor a un porcentaje de humedad
        porcentajeHumedad = mates(humedadDigital, VALOR_SECO, VALOR_HUMEDO, 0, 100);
        
        // Limita el porcentaje a los valores entre 0 y 100
        if (porcentajeHumedad < 0) {
            porcentajeHumedad = 0;
        } else if (porcentajeHumedad > 100) {
            porcentajeHumedad = 100;
        }
        
       // Calcular la parte entera y decimal del porcentaje con redondeo
        porEnt = porcentajeHumedad; // Parte entera  
        
        printf(" %i", porEnt);
        delay_ms(1000); // Esperar 1 segundo
        
        if (porEnt < 10) 
        {            
            delay_ms(1000); 
            PORTD.2 = 1;
            delay_ms(1000);
            PORTD.2 = 0;
        }
        else 
        {    
            delay_ms(1000); 
            PORTD.2 = 1;
        }
    }
}