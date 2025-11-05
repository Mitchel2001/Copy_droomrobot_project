import asyncio
import time

from mini.apis.api_behavior import StartBehavior
from mini.apis.api_expression import PlayExpression
from mini.apis.api_sound import StartPlayTTS
from mini.dns.dns_browser import WiFiDevice
from test_connect import test_connect, test_start_run_program, shutdown

# test to play and record (video) and timing for all animations

# all actions from Droomrobot Drive sheet
action_filenames = [
    "007", "009", "011", "012", "013", "015", "017", "018", "019", "021", "024", "027", "028", "031",
    "037", "038", "039", "random_short2", "random_short3", "random_short4", "Surveillance_001", "Surveillance_003",
    "Surveillance_004", "Surveillance_006", "action_004", "action_005", "action_006", "action_007", "action_012",
    "action_013", "action_014", "action_015", "action_016", "action_019", "action_020"
]

action_descriptions = [
    "Rise from a seated position", "Reset", "Nod", "Push-ups", "Kung fu", "Welcome", "Raise both hands",
    "Lift the right leg", "Lift the left leg", "Bend at the waist", "Yoga", "Sit down", "Do a right lunge",
    "Squat down", "Shake the head", "Tilt the head", "Laugh out loud", "Hug", "Wave the left hand",
    "Wave the right hand", "Say hi", "Shake hands", "Blow a kiss", "Act cute", "Wow", "Give a thumb-up", "OK",
    "Beat you up", "Ask for a hug", "Make faces", "Invite", "Wiggle the hips", "Say goodbye", "Hold the head",
    "A smug face"
]

# all expressions from Droomrobot Drive sheet
expression_filenames = [
    "codemao1", "codemao2", "codemao3", "codemao4", "codemao5", "codemao6", "codemao7", "codemao8", "codemao9",
    "codemao10", "codemao11", "codemao12", "codemao13", "codemao14", "codemao15", "codemao16", "codemao17",
    "codemao18", "codemao19", "codemao20", "w_basic_0003_1", "w_basic_0005_1", "w_basic_0010_1", "w_basic_0011_1",
    "w_basic_0012_1", "emo_007", "emo_008", "emo_009", "emo_010", "emo_011", "emo_013", "emo_014", "emo_015",
    "emo_016", "emo_019", "emo_020", "emo_022", "emo_023", "emo_026", "emo_028"
]

expression_descriptions = [
    "Look around", "Heartbreaking", "Sad", "Asleep", "Frightened", "Sleepy", "Strange", "Shocked", "Sneeze",
    "Cheer up", "Fighting", "Exert strength", "Doubt", "Wake up", "Distressed", "A sly smile", "Depressed",
    "Eager", "Love", "Blink", "Look to the right", "Look to the left", "Look up", "Look left and right",
    "Look up and down", "Smile", "Agitated", "Tears", "Shy", "Cry aloud", "Angry", "Pathetic", "Arrogant",
    "Simper", "Dizzy", "Daze", "Wipe eye gunk", "Hurt", "Contemptuous look", "Cover up the face"
]

# play TTS
async def speak(text: str):
    tts = StartPlayTTS(text=text)
    await tts.execute()

# play action with timing
async def play_action(filename: str, description: str):
    await speak(f"Action: {filename}. {description}.")
    start = time.time()
    block = StartBehavior(name=filename)
    await block.execute()
    duration = time.time() - start
    await speak(f"Duration was {duration:.2f} seconds.")

# play expression with timing
async def play_expression(filename: str, description: str):
    await speak(f"Expression: {filename}. {description}.")
    start = time.time()
    block = PlayExpression(express_name=filename)
    await block.execute()
    duration = time.time() - start
    await speak(f"Duration was {duration:.2f} seconds.")

# sequential run of actions and expressions 
async def run_all():
    for filename, description in zip(action_filenames, action_descriptions):
        await play_action(filename, description)
        await asyncio.sleep(1)

    for filename, description in zip(expression_filenames, expression_descriptions):
        await play_expression(filename, description)
        await asyncio.sleep(1)

# explicit IP - solution for iPhone hotspot scanning issue
async def main():
    device = WiFiDevice(name="", address="172.20.10.10", port=8801)
    success = await test_connect(device)
    if success:
        print("Connected to the robot")
        await test_start_run_program()
        await run_all()
        await shutdown()
    else:
        print("Failed to connect to robot")

if __name__ == '__main__':
    asyncio.run(main())