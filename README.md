# Raspberry-office
in this program it's used a Raspberry pi model 3B+. From module datetime of python and gpiozero of Raspberry is generate an automatic signal for illumination of offices, using the GPIOs 18, 23, 24 for a RGB Led for indicate the proximity of events, 10 for a buzzer and  15 for indicate a state of illumination of the office.the office only work the five days of the week(Mon - Fri) in the interval the 7am at 6pm, any value out of this ranges (days or hours) the office is close.