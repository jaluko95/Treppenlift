# Treppenlift
Steuerung für einen Treppenlift

Warum überhaupt das Ganze?
Die eingebaute Steuerung ging regelmäßig kaputt und der Lift war für die Zeit der Ersatzteilbeschaffung (2- 3 Wochen) nicht nutzbar.
Mit Ablauf der Garantie, habe ich dann für den gleichen Preis eines Ersatzteiles eine eigene Steuerung entworfen und implementieren können.

"Das Gehirn" der Steuerung ist ein RPi Zero W - dieser lässt sich bequem über VNC ansprechen und bietet eine über mehr als ausreichende Anzahl an I/O's.
Darüber hinaus ist der Rpi überaus sparsam im Stromverbrauch und bietet dennoch mehr als genug Leistungsreserven. 

Die beiden Motoren werden simpel über zwei H-Brücken gesteuert. Hierbei musste auf eine ordentliche Reserve bezüglich Dauer- und Spitzenstromverträglichkeit
sowie auf Wärmeentwicklung und Platzverbrauch geachtet werden. Fündig wurde ich bei einem regionalen Elektronikladen. 
Ein ungewolltes Durchschalten der H-Brücken muss auf jeden Fall verhindert werden. Simulationen schafften hier eine Gewissheit. 


Schaltplan:
Alle Taster welche sicherstellen, dass der Weg frei ist, sind in Reihe geschaltet. Unterbricht ein Taster den Stromkreis wird über eine Abfrage im Programm sofort ein Stop ausgelöst.
Zum entprellen der Taster wurde der integrierte PullUp-Widerstand verwendet.

Zur Erkennung ob der Lift bereits an einer der Enden angekommen ist, sind unterhalb des Lifts drei Taster mit Rollenhebel verbaut. Diese Rollen knapp oberhalb
der Schiene und werden am Ende des Weges über eine auf der Schiene befestigten Rampe, betätigt. Hierbei entfällt jeweils ein Taster für die Enden 
und ein Dritter für einen eventuellen Notstop - dieser unterbricht über ein Relais (unabhängig des RPi's) den Stromkreis zwischen Akku und Motor. 

Zur Verhinderung von Spannungsspitzen und eines unangenehmen Rucks wurde für den Normalfall ein sanfter Start/ Stop programmiert. 
Für eventuell auftretende Spannungsspitzen beim sofortigen Stop, schließt eine Diode an den Polen der H-Brücken den Stromkreis kurz. Darüber kann sich die Spannung über die Motorwicklung abbauen und zerstört nicht die H-Brücken. 
