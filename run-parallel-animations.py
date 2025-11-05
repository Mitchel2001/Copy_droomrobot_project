# Demonstrates animations and TTS for the Droomrobot development.

import asyncio
import random
import time

from mini.apis.base_api import MiniApiResultType
from mini.apis.api_action import PlayAction, PlayActionResponse
from mini.apis.api_expression import PlayExpression, PlayExpressionResponse
from mini.apis.api_sound import StartPlayTTS
from mini.dns.dns_browser import WiFiDevice

from test_connect import shutdown, test_connect, test_start_run_program

# Animation lists
# Note: names are case sensitive. speakingAct, face_, photograph_ series are
# gestures without legs. w_basic_0003_ expressions aim eyes right. 
# codemao13 is looking up (thinking). codemao20 is blinking when idle. 
# emo_007 is happy squinting eyes.

calm_random = [
    "face_007",
    "Drive_016",
    "speakingAct10",
    "speakingAct11",
    "speakingAct12",
    "speakingAct14",
]

animated_random = [
    "speakingAct1",
    "speakingAct15",
    "photograph_017",
    "speakingAct11",
    "speakingAct12",
    "face_028a",
    "speakingAct13",
    "speakingAct16",
    "speakingAct14",
    "speakingAct17",
    "random_short1",
    "action_010",
    "speakingAct5",
    "speakingAct6",
]

general_expressions = [
    "emo_007",
    "w_basic_0003_1",
    "w_basic_0011_1",
    "codemao13",
    "codemao20",
]

welcome_expressions = [
    "emo_007",
    "codemao20",
]

current_speaking_animations = None
tts_active = asyncio.Event()

# Script text segments with animation specifications
tts_events = [
    {"text": "Hallo, ik ben de droomrobot! Wat fijn dat ik je mag helpen vandaag.",
     "spec": "boc_welcome"},
    {"text": "Wat is jouw naam?", "spec": "1"},
    {"text": "Hoi naam kind, wat leuk je te ontmoeten.", "spec": "2"},
    {"text": "Wat een leuke naam, fijn dat je er bent.", "spec": "2"},
    {"text": ("Als je geen zin hebt om je naam te zeggen, is dat ook prima."),
     "spec": "1"},
    {"text": "En hoe oud ben je?", "spec": "1"},
    {"text": "robot-listens", "spec": "idle"},
    {"text": ("Oh wat goed, dan kan ik je een trucje leren om alles in "
              "het ziekenhuis makkelijker te maken."),
     "spec": "2"},
    {"text": "Dat trucje werkt bij veel kinderen heel goed", "spec": "2"},
    {"text": "Ik ben benieuwd hoe goed het bij jou gaat werken.", "spec": "2"},
    {"text": "Jij kunt jezelf helpen door je lichaam en gedachten te ontspannen.",
     "spec": "2"},
    {"text": "We gaan het samen doen, op jouw eigen manier.", "spec": "1"},
    {"text": ("Ik ben even nieuwsgierig, heb je al verdovingszalfpleisters "
              "gekregen?"),
     "spec": "1"},
    {"text": "robot-listens", "spec": "idle"},
]


async def play_action(filename: str) -> None:
    """
    Execute an action using PlayAction and measure its duration.
    """
    print(f"Action: {filename}")
    start_time = time.time()
    block = PlayAction(action_name=filename)
    result, response = await block.execute()
    duration = time.time() - start_time

    if (result != MiniApiResultType.Success
            or not isinstance(response, PlayActionResponse)
            or not response.isSuccess):
        print(f"Action {filename} failed: {response}")
    else:
        print(f"Action duration: {duration:.2f} seconds")


async def play_expression(filename: str) -> None:
    """
    Execute an expression using PlayExpression and measure its duration.
    """
    print(f"Expression: {filename}")
    start_time = time.time()
    block = PlayExpression(expression_name=filename)
    result, response = await block.execute()
    duration = time.time() - start_time

    if (result != MiniApiResultType.Success
            or not isinstance(response, PlayExpressionResponse)
            or not response.isSuccess):
        print(f"Expression {filename} failed: {response}")
    else:
        print(f"Expression duration: {duration:.2f} seconds")


async def speak(text: str) -> None:
    """
    Execute the TTS task using StartPlayTTS.
    """
    print(f"TTS started: {text}")
    tts = StartPlayTTS(text=text)
    await tts.execute()
    print("TTS completed.")


async def animations_loop() -> None:
    """
    Loop through speaking animations when TTS is active; otherwise idle.
    """
    idle_animation = ["codemao20"]

    while True:
        if tts_active.is_set():
            if current_speaking_animations is None:
                print("Current speaking animations list not set; skipping")
                await asyncio.sleep(0.5)
                continue

            animation = random.choice(current_speaking_animations)
            try:
                if animation.startswith(("speakingAct", "face_", "photograph_")):
                    await play_action(animation)
                else:
                    await play_expression(animation)
            except Exception as exc:
                print(f"Error executing {animation}: {exc}")
        else:
            animation = random.choice(idle_animation)
            try:
                await play_expression(animation)
            except Exception as exc:
                print(f"Error executing idle expression {animation}: {exc}")


async def parallel_expression_loop(
        animation_list: list, interval: float = 1.0) -> None:
    """
    Run expressions from animation_list at fixed intervals until cancelled.
    """
    while True:
        if animation_list == general_expressions:
            weights = [1, 2, 2, 2, 4]
            animation = random.choices(
                animation_list, weights=weights, k=1
            )[0]
        else:
            animation = random.choice(animation_list)

        print(f"Parallel expression: {animation}")
        try:
            await play_expression(animation)
        except Exception as exc:
            print(f"Error in parallel expression {animation}: {exc}")

        await asyncio.sleep(interval)


async def process_events() -> None:
    """
    Process each TTS event and launch simultaneous tasks based on spec.
    """
    global current_speaking_animations  # pylint: disable=global-statement

    for event in tts_events:
        text_segment = event["text"]
        spec = event["spec"]

        if spec == "boc_welcome":
            print("Playing boc_welcome with parallel expressions")
            parallel = asyncio.create_task(
                parallel_expression_loop(welcome_expressions, interval=2)
            )
            await asyncio.gather(
                speak(text_segment),
                play_action("boc_welcome")
            )
            parallel.cancel()
            try:
                await parallel
            except asyncio.CancelledError:
                print("Welcome expressions task cancelled")

            await asyncio.sleep(2)

        elif spec in {"1", "2"}:
            tts_active.set()
            current_speaking_animations = (
                calm_random if spec == "1" else animated_random
            )

            parallel = asyncio.create_task(
                parallel_expression_loop(general_expressions, interval=1.5)
            )
            await speak(text_segment)
            parallel.cancel()

            try:
                await parallel
            except asyncio.CancelledError:
                print("Parallel spec animations task cancelled")

            tts_active.clear()
            await asyncio.sleep(2)
        else:
            print(f"Unknown spec '{spec}'; skipping event.")
            await asyncio.sleep(2)


async def main() -> None:
    """
    Connect to robot with explicit IP + port and run the script.
    """
    device = WiFiDevice(name="", address="172.20.10.10", port=8801)

    if not await test_connect(device):
        print("Failed to connect to the robot")
        return

    print("Robot connected")
    await test_start_run_program()

    anim_task = asyncio.create_task(animations_loop())
    await process_events()
    anim_task.cancel()

    try:
        await anim_task
    except asyncio.CancelledError:
        print("Animations loop stopped")

    await shutdown()


if __name__ == "__main__":
    asyncio.run(main())