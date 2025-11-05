import asyncio
from mini import mini_sdk as MiniSdk
from mini.apis.api_action import GetActionList, GetActionListResponse, RobotActionType
from mini.apis.api_action import MoveRobot, MoveRobotDirection, MoveRobotResponse
from mini.apis.api_action import PlayAction, PlayActionResponse
from mini.apis.base_api import MiniApiResultType
from mini.dns.dns_browser import WiFiDevice

# Testfunctie: Voer een enkele actie (actie '018') uit
async def test_play_action():
    """Voer een enkele actie demo uit met actie '018'."""
    block = PlayAction(action_name='018')
    resultType, response = await block.execute()
    print(f'test_play_action result: {response}')
    assert resultType == MiniApiResultType.Success, 'test_play_action timeout'
    assert response and isinstance(response, PlayActionResponse), 'test_play_action result unavailable'
    assert response.isSuccess, 'play_action failed'

# Nieuwe functie: Voer meerdere acties uit met een pauze tussen elke actie
async def test_play_multiple_actions():
    """Voer meerdere acties uit met een tijdspauze ertussen."""
    actions = ['039', '011', '013']
    delay_seconds = 3

    for action in actions:
        print(f'Uitvoeren actie: {action}')
        block = PlayAction(action_name=action)
        resultType, response = await block.execute()
        print(f'Resultaat van actie {action}: {response}')
        if not response.isSuccess:
            print(f'Actie {action} is mislukt.')
        await asyncio.sleep(delay_seconds)

# Testfunctie: Laat de robot bewegen
async def test_move_robot():
    """Laat de robot 10 stappen naar links bewegen."""
    block = MoveRobot(step=10, direction=MoveRobotDirection.LEFTWARD)
    resultType, response = await block.execute()
    print(f'test_move_robot result: {response}')
    assert resultType == MiniApiResultType.Success, 'test_move_robot timeout'
    assert response and isinstance(response, MoveRobotResponse), 'test_move_robot result unavailable'
    assert response.isSuccess, 'move_robot failed'

# Testfunctie: Haal de lijst met ingebouwde acties op
async def test_get_action_list():
    """Haal de lijst met ingebouwde acties van de robot op."""
    block = GetActionList(action_type=RobotActionType.INNER)
    resultType, response = await block.execute()
    print(f'test_get_action_list result: {response}')
    assert resultType == MiniApiResultType.Success, 'test_get_action_list timeout'
    assert response and isinstance(response, GetActionListResponse), 'test_get_action_list result unavailable'
    assert response.isSuccess, 'get_action_list failed'

async def main():
    """Hoofdprogramma om de robot aan te sturen."""
    device = WiFiDevice(
        name="AlphaMini",  
        address="172.20.10.4",  # Vervang met het correcte IP-adres van je Alpha Mini
        port=8801
    )

    success = await MiniSdk.connect(device)
    print(f"DEBUG: Connection status: {success}")

    if success:
        print("Connected successfully")
        await MiniSdk.enter_program()
        
        # Voer eerst de oorspronkelijke actie (actie '018') uit
        await test_play_action()
        # Voer daarna de nieuwe functie uit voor meerdere acties
        await test_play_multiple_actions()
        await test_move_robot()
        await test_get_action_list()

        await MiniSdk.quit_program()
        await MiniSdk.release()
    else:
        print("Failed to connect to robot")

if __name__ == '__main__':
    asyncio.run(main())
