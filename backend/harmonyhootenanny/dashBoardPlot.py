import requests
import matplotlib.pyplot as plt
import os

# Sendet eine Anfrage an den /api/dashboard Endpunkt
response = requests.get('http://localhost:5000/api/dashboard')

# Überprüft, ob die Anfrage erfolgreich war
if response.status_code == 200:
    # Parst die Antwort als JSON
    data = response.json()

    for room, room_data in data.items():
        print(room, room_data)
        fig, axs = plt.subplots(2, 2)  # Erstellt eine neue Figur mit 2x2 Subplots

        # Erstellt ein Balkendiagramm für die Anzahl der Hörer
        axs[0, 0].bar('Number of Listeners', room_data['number_of_listeners'], color='blue', alpha=0.75)

        # Erstellt ein Balkendiagramm für die Gesamtspielzeit
        axs[0, 1].bar('Total Play Time', room_data['total_play_time'], color='red', alpha=0.75)

        # Erstellt ein Kreisdiagramm für den am häufigsten gespielten Song
        axs[1, 0].pie([1], labels=[room_data['most_played_song']], colors=['green'], autopct='%1.1f%%')

        # Erstellt ein Kreisdiagramm für den Top-Künstler
        axs[1, 1].pie([1], labels=[room_data['top_artist']], colors=['purple'], autopct='%1.1f%%')

        fig.suptitle(f'Data for {room}')

        print("Aktuelles Verzeichnis:", os.getcwd())
        
        # Speichert das Diagramm als Bild
        plt.savefig(os.path.join('charts', f'{room}.png'))