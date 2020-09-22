# oregon-scientific-temp-viewer
The idea of this project was to intercept the signal my oregon scientific termometers and store it

To archeive this I used Django as backend an React in front end. This is my fisrt project in react and I used the framework Material UI. To display the charts I used a react Charts.js wrapper.

To intercept the temperature from my sensors I used a rapsberry pi, an RC receptor and this project https://github.com/1000io/OregonPi. Adicionaly I used the sensor DHT22 to measure aditional records.

This poject is not finished yet as there are many features I want to introduce

# Actual features
  - It works
  - Records 4 sensors and shows the battery status
  - The tempperature and the humidity is displayed on a line chart
 




# Features I want to add
  - Using websockets for data updating (Migrating from wsgi to uswsgi)
  - Make the detector work with django instead of a separate script
  - Display the local temperature (Investigate what API I should use)
  - Clean code, and better ui...
  

# Screenshots

![Pantallazos](https://i.imgur.com/ZBLL51K.png )
![Pantallazos](https://i.imgur.com/3myfOXc.png)
![Pantallazos](https://i.imgur.com/CWRBd0C.png )
![Pantallazos](https://i.imgur.com/aZdWeFh.png )
