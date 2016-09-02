from ewindowui import eWindowUI
from time import sleep

ui = eWindowUI()
ui.showText("Verbindung wird hergestellt...");
sleep(5)
ui.showText("Verbunden. Anruf herstellen?");
sleep(5)
ui.showSelectionList("Anrufen?", ["MuMaLab", "Werkbox3", "FabLab"])
sleep(3)
ui.showSelectionList("Anrufen?", ["Werkbox3", "FabLab", "MuMaLab"])
sleep(3)
ui.showSelectionList("Anrufen?", ["FabLab", "MuMaLab", "Werkbox3"])
sleep(5)
ui.showText("Ring...ring...ring...");
sleep(5)
ui.showText("Fenster wird geoeffnet");
sleep(5)
ui.stop()
ui.showTextVideoOverlay("Klopf..klopf...")
sleep(5)
ui.stop()
