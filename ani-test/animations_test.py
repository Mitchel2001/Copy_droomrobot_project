import asyncio
from mini.apis.api_sound import StartPlayTTS
from mini.apis.api_behavior import StartBehavior
from mini.apis.api_expression import PlayExpression
from mini.dns.dns_browser import WiFiDevice
from test_connect import test_connect, shutdown, test_start_run_program

async def async_input(prompt: str) -> str:
    loop = asyncio.get_running_loop()
    return await loop.run_in_executor(None, input, prompt)

class Droomrobot:
    def __init__(self, ip: str, port: int):
        self.device = WiFiDevice(name="", address=ip, port=port)

    async def initialize(self):
        success = await test_connect(self.device)
        if success:
            print("Connected to robot")
            await test_start_run_program()
        else:
            print("Failed to connect to robot")
            raise Exception("Connection failed")

    async def say(self, text: str):
        print(f"Robot TTS: {text}")
        # initiate TTS
        tts_block = StartPlayTTS(text=text)
        tts_task = asyncio.create_task(tts_block.execute())

        # loop action and expression simultanously 
        dance_task = asyncio.create_task(self.loop_dance(tts_task))
        expression_task = asyncio.create_task(self.loop_expression(tts_task))

        # wait TTS to complete
        resultType, response = await tts_task
        print(f"TTS response: {response}")

        # cancel loops when TTS completes
        dance_task.cancel()
        expression_task.cancel()
        try:
            await dance_task
        except asyncio.CancelledError:
            pass
        try:
            await expression_task
        except asyncio.CancelledError:
            pass
        print("TTS completed")

    async def loop_dance(self, tts_task: asyncio.Task):
        """loops action"""
        while not tts_task.done():
            dance_block = StartBehavior(name="015")
            resultType, response = await dance_block.execute()
            print(f"Dance action: {response}")
            await asyncio.sleep(0.5)  # interval 

    async def loop_expression(self, tts_task: asyncio.Task):
        """loop expression"""
        while not tts_task.done():
            expr_block = PlayExpression(express_name="codemao19")
            resultType, response = await expr_block.execute()
            print(f"Expression: {response}")
            await asyncio.sleep(0.5)  # interval

    async def run(self):
        """robot conversation"""
        await self.initialize()

        await self.say("Hallo, ik ben de droomrobot en ik ben hier voor jou.")

        answer = await async_input("Hou je van dieren? (yes/no):")
        if answer.lower().startswith("y"):
            fav_animal = await async_input("Wat is jouw lievelingsdier?")
            await self.say(f"Wat vind je zo leuk aan een {fav_animal}?")
        else:
            await self.say("Ik moet gaan, leuk je gesproken te hebben. Tot de volgende keer!")

        await shutdown()

if __name__ == '__main__':
    robot = Droomrobot(ip="172.20.10.4", port=8801)
    asyncio.run(robot.run())