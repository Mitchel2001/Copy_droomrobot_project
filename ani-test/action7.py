import asyncio
import time

from mini.dns.dns_browser import WiFiDevice
from mini.apis.api_action import PlayAction, PlayActionResponse
from mini.apis.base_api import MiniApiResultType
from test_connect import test_connect, test_start_run_program, shutdown

# action list from robot itself
ACTION_FILENAMES = [
    "001", "001_custom_v", "001_tapHead", "002", "002_1", "003", "004", "006", "007_1", "008",
    "010", "011_1_1", "012_1", "012_1_1", "012_1_2", "016", "016_1", "016_2", "017_1", "018_1",
    "018_2", "019_1", "019_2", "021_1", "021_2", "022", "022_1", "022_1_1", "022_1_2", "022_1_3",
    "022_2", "022_2_1", "022_2_2", "022_3", "022_3_1", "023", "023_1", "023_1_1", "023_1_2", "023_1_3",
    "023_2", "023_2_1", "023_2_2", "023_3", "023_3_1", "024_1", "024_2", "025", "025_1", "025_1_1",
    "026", "026_1", "026_1_1", "027_1", "027_face_v", "029", "030", "037_1_1", "038_1_1", "40_1_1",
    "41_1_1", "42_1_1", "Drive_001", "Drive_002", "Drive_003", "Drive_004", "Drive_005", "Drive_006",
    "Drive_007", "Drive_008", "Drive_009", "Drive_010", "Drive_011", "Drive_012", "Drive_013",
    "Drive_013_1", "Drive_014", "Drive_015", "Drive_016", "Drive_017", "Drive_018", "Drive_019",
    "Drive_024", "act_cute_avatar", "action_002", "action_003", "action_008", "action_009",
    "action_010", "action_011", "action_017", "action_018", "aging", "air_kiss_avatar", "balance", "current", "dance_00011en", "dance_0006",
    "dance_0007en", "dance_0009en", "dance_0011en", "face_001b", "face_003b", "face_005", "face_007",
    "face_008", "face_010", "face_011", "face_014", "face_015", "face_018a", "face_018b", "face_019b",
    "face_022a", "face_022c", "face_026b", "face_028a", "face_028b", "face_029", "face_030",
    "face_035", "face_036", "face_037", "face_039", "gongxi", "handshake_avatar", "hug_avatar",
    "jointcheck", "move_forward_avatar", "photograph_001", "photograph_002", "photograph_003",
    "photograph_004", "photograph_009", "photograph_010", "photograph_011", "photograph_012",
    "photograph_013", "photograph_014", "photograph_015", "photograph_016", "photograph_017",
    "photograph_018", "photograph_019", "photograph_020", "photograph_022", "random_short1",
    "random_short3_1", "random_short4_1", "random_short5", "rap", "reboot_001", "reboot_003",
    "reboot_004", "say_hello_avatar", "sleepmode_001", "sleepmode_002", "speakingAct1", "w_stand_001", "w_stand_002",
    "w_stand_003", "w_stand_004", "w_stand_005", "w_stand_006", "w_stand_007", "w_stand_008",
    "w_stand_009", "w_stand_010"
]

async def play_action(filename: str) -> None:
    """
    Voert een actie uit met PlayAction en meet de duur van de uitvoering.
    """
    print(f"Action: {filename}")
    start_time = time.time()
    block: PlayAction = PlayAction(action_name=filename)
    (resultType, response) = await block.execute()
    duration = time.time() - start_time

    if resultType != MiniApiResultType.Success or not isinstance(response, Pl0yActionResponse) or not response.isSuccess:
        print(f"Action {filename} failed with result: {response}")
    else:
        print(f"Duration was {duration:.2f} seconds.")


async def run_all() -> None:
    """
    Voert alle acties sequentieel uit met een korte pauze tussen elke actie.
    """
    for filename in ACTION_FILENAMES:
        await play_action(filename)
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