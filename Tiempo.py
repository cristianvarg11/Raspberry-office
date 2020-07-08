#------------ Importacion de modulos ---------------#
import time
from datetime import datetime
from gpiozero import RGBLED
from gpiozero import LED
#----------- Definiciones --------------------------#
now   = datetime.now()
format_hor = '%H:%M:%S'  # formato hora
#---------------------#
#Horas significativas-#
Inicio_jornada  = '7:30:00'
Almuerzo_inicio = '12:00:00'
Almuerzo_final  = '13:00:00'
Final_jornada   = '18:00:00'
#---------------------#
Error = 0
#--------- Alarmas ----------#
Start_day = datetime.strptime(Inicio_jornada, format_hor)
Alm_start = datetime.strptime(Almuerzo_inicio, format_hor)
Alm_final = datetime.strptime(Almuerzo_final, format_hor)
Final_day = datetime.strptime(Final_jornada, format_hor)
#--- Terminales de salida ---#
rgb0 = RGBLED(18, 23, 24)
buzzer = LED(10)
office = LED(15)
office.off()
#---------------------------------------------------#
#<<<<<<<<<<<<<<<<<< Funciones >>>>>>>>>>>>>>>>>>>>>>#
def Cap_hor():  # obtener datetime actual
    now   = datetime.now()
    horita = '{:%H:%M:%S}'.format(now)
    horams = datetime.strptime(horita, format_hor)
    data = {'dia': now.day, 'mes':now.month, 'anio':now.year, 'Hora':now.hour, 'Minutos':now.minute, 'Segundos':now.second, 'all':now, 'horams': horams}
    return data
#------------ Comparaciones de tiempo --------------#
#----------------------------------#
def Comparacion(actual, alarma):  # tiempo restante para proximo evento
    Final_comp = alarma - actual
    restante = {'Segundos': Final_comp.seconds, 'Dias': Final_comp.days,'Todo': Final_comp}
    return restante
#----------------------------------#
def mitad_ending(inicio):         # 50% y 10% del alarma
    Mitad = inicio.second * 0.5
    Termi = inicio.second * 0.1
    return Mitad, Termi
#----------------------------------#
def event_is_coming(temporizador, alarma):
    while temporizador['Segundos'] >= 0:
        now       = datetime.now()
        dia       = '{:%a}'.format(now)
        Fecha_1   = '{:%a %d de %b del %Y | Hora --> %H:%M:%S}'.format(now)
        print('===', Fecha_1, '===')
        Actual = Cap_hor()
        temporizador = Comparacion(Actual['all'], alarma)
        event_m_c = mitad_ending(now)
        #------------------------------------------------#
        if temporizador['Segundos'] > event_m_c[0]:
            print('===== Aun queda tiempo para proximo evento =======')
            rgb0.color = (0,1,0)  # Verde
        elif event_m_c[1] <= temporizador['Segundos']:
            print('===== Mitad del tiempo para proximo evento =======')
            rgb0.red = 100/100  # Amarillo
            rgb0.green = 25/100
            
        elif temporizador['Segundos'] < event_m_c[1] and temporizador['Segundos'] > 0:
            print('===== Va a iniciar proximo evento ================')
            rgb0.red = 100/100  # Naranja
            rgb0.green = 6/100
            
        elif temporizador['Segundos'] == 0:
            print('\n\r<<<<<<<<<<<<<<<<<<<<<>>>>>>>>>>>>>>>>>>>>')
            print('=========== En evento ===============')
            print('<<<<<<<<<<<<<<<<<<<<<>>>>>>>>>>>>>>>>>>>>\n\r')
            for i in range (15):
                buzzer.on()
                rgb0.color = (1,1,1)
                time.sleep(0.12)
                buzzer.off()
                rgb0.color = (0,0,0)
                time.sleep(0.12)
        elif temporizador['Segundos'] < 0:
            Error = 1
        time.sleep(1)  # wait 1 seconds
        break
#----------------------------------#
def Working():                    # jornada laboral
    while True:
        #-------- Actualizar constantemente Fecha y hora ---------#
        now   = datetime.now()
        Actual = Cap_hor()
        dia   = '{:%a}'.format(now)
        Fecha_1 = '{:%a %d de %b del %Y | Hora --> %H:%M:%S}'.format(now)
        #---------------------------------------------------------#
        if dia != 'Sat' or dia != 'Sun':
            if Actual['Hora'] == 7 and Actual['minutos'] == 30:  # inicio de la jornada
                print('\n\r=============== Inicio de jornada laboral ========================')
                print('===', Fecha_1, '===')
                print('=================================================================\n')
                office.on()  # luz encendida
        
            elif Actual['Hora'] >= 7 and Actual['Hora'] < 12:
                print('\n\r=============== Working ==========================')
                #----- Proximo evento es inicio de almuerzo ------#
                tempori = Comparacion(Actual['horams'], Alm_start)
                event_is_coming(tempori, Alm_start)
                office.on()  # luz encendida

            elif Actual['Hora'] >= 12 and Actual['Hora'] < 13:
                print('\n\r=============== En almuerzo ======================')
                #----- Proximo evento es final del almuerzo -------#
                tempori = Comparacion(Actual['horams'], Alm_final)
                event_is_coming(tempori, Alm_final)
                office.on()  # luz encendida

            elif Actual['Hora'] >= 13 and Actual['Hora'] < 18:
                print('\n\r=============== Working ==========================')
                #----- Proximo evento es final de la jornada -------#
                tempori = Comparacion(Actual['horams'], Final_day)
                event_is_coming(tempori, Final_day)
                office.on()  # luz encendida

            elif Actual['Hora'] >= 18:
                print('\n=============== Final de la jornada laboral ========================')
                print('===', Fecha_1, '===')
                #----- Proximo evento es inicio de la jornada -------#
                tempori = Comparacion(Actual['horams'], Start_day)
                event_is_coming(tempori, Start_day)
                office.off()  # luz apagada
                rgb0.color = (0,0,0)
                
            elif Error == 1:
                print('!!!!!!!!!!!!!!!!!!!!! Error Temporal !!!!!!!!!!!!!!!!!!!!!!')
                break
        else:
            print('\n=============== Dia no laboral ===============\n')
            office.off()  # luz apagada
            rgb0.color = (0,0,0)
            break
#----------------------------------# 
#<<<<<<<<<<<<<<<<<<<<<<<<<<>>>>>>>>>>>>>>>>>>>>>>>>>#
if __name__ == '__main__':
    Working()
