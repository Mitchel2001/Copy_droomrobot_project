import asyncio
import time

from mini.apis.api_behavior import StartBehavior
from mini.apis.api_sound import StartPlayTTS
from mini.dns.dns_browser import WiFiDevice
from test_connect import test_connect, test_start_run_program, shutdown

# Acties van de Droomrobot Drive sheet (alleen de dance_0001en animatie)
ACTION_FILENAMES = [
    "dance_0001en"
]

# We geven hier meerdere beschrijvingen op, maar omdat er maar één animatie is,
# wordt alleen de eerste gebruikt.
ACTION_DESCRIPTIONS = [
    "Rise from a seated position", "Reset", "Nod", "1Push-ups", "1kung fu", "Welcome", "Raise both hands",
    "Lift the right leg", "Lift the left leg", "1Bend at the waist", "Yoga", "Sit down", "Do a right lunge",
    "Squat down"
]


async def speak(text: str) -> None:
    """
    Speelt een TTS-bericht af met de opgegeven tekst.
    """
    tts = StartPlayTTS(text=text)
    await tts.execute()


async def play_action(filename: str, description: str) -> None:
    """
    Voert een actie uit met een maximale uitvoeringstijd van 15 seconden.
    """
    await speak(f"Action: {filename}. {description}.")
    start_time = time.time()
    behavior = StartBehavior(name=filename)

    try:
        # Voer de actie uit met een timeout van 15 seconden.
        await asyncio.wait_for(behavior.execute(), timeout=15)
    except asyncio.TimeoutError:
        await speak("Animation stopped after 15 seconds.")

    duration = time.time() - start_time
    await speak(f"Duration was {duration:.2f} seconds.")


async def run_all() -> None:
    """
    Voert alle acties sequentieel uit met een korte pauze tussen elke actie.
    """
    for filename, description in zip(ACTION_FILENAMES, ACTION_DESCRIPTIONS):
        await play_action(filename, description)
        await asyncio.sleep(1)


async def main() -> None:
    """
    Probeert te verbinden met de robot en voert vervolgens alle acties uit.
    """
    # Specifiek IP-adres (oplossing voor iPhone hotspot scanning issue)
    device = WiFiDevice(name="", address="172.20.10.10", port=8801)

    if await test_connect(device):
        print("Connected to the robot")
        await test_start_run_program()
        await run_all()
        await shutdown()
    else:
        print("Failed to connect to robot")


if __name__ == '__main__':
    asyncio.run(main())