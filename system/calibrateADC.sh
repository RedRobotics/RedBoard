# Author: Neil Lambeth. neil@redrobotics.co.uk @NeilRedRobotics

echo
echo Measure your battery voltage with a multimeter and enter it here.
echo The voltage should be between 7 - 24, you can use 2 decimal places eg. 11.99
echo Press [Enter] once you have typed in your measurement. 
  
while read battery
 
do

    if [[ "$battery" =~ ^-?[7-9]|1[0-9]|2[0-4]+[.,]?[0-9]*$ ]]
    then
        break
    else
        echo Please enter a number between 7-24.
    fi

done


adc_Old=`python3 /home/pi/RedBoard/system/bat_check.py`

echo Old Battery Measurement = $adc_Old

adc=`python3 /home/pi/RedBoard/system/adc_conversion.py`

echo ADC reading = $adc
num=$(python -c "print $adc/$battery")
num1=$(python -c "print round($num)")

echo Calibration value = $num1

sed -i "/Value =/c\ADC_bat_conversion_Value = ${num1}" /home/pi/RedBoard/system/bat_check.py

echo ADC calibrated successfully!
echo
adc2=`python3 /home/pi/RedBoard/system/bat_check.py`

echo New battery measurement = $adc2
echo
