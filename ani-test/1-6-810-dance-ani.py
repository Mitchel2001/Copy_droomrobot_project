import asyncio
import time

from mini.apis.api_behavior import StartBehavior
from mini.apis.api_sound import StartPlayTTS
from mini.dns.dns_browser import WiFiDevice
from test_connect import test_connect, test_start_run_program, shutdown

# Acties van de Droomrobot Drive sheet (alleen acties tussen 7 en 31)
ACTION_FILENAMES = [
    "dance_0001en", "dance_0002en", "dance_0003en", "dance_0004en", "dance_0005en", "dance_0006en",
    "dance_0008en", "dance_0010en"
]

ACTION_DESCRIPTIONS = [
    "Rise from a seated position", "Reset", "Nod", "Push-ups", "Kung fu", "Welcome", "Raise both hands",
    "Lift the right leg", "Lift the left leg", "Bend at the waist", "Yoga", "Sit down", "Do a right lunge",
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
    Voert een actie uit en meet de duur van de uitvoering.
    """
    await speak(f"Action: {filename}. {description}.")
    start_time = time.time()
    behavior = StartBehavior(name=filename)
    await behavior.execute()
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