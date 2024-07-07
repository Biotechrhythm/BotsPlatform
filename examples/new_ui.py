import asyncio
import random

from swiftbots import PeriodTrigger, SwiftBots, depends
from swiftbots.all_types import ILogger


def input_async(*args, **kwargs):
    return asyncio.to_thread(input, *args, **kwargs)


def print_async(*args, **kwargs):
    return asyncio.to_thread(print, *args, **kwargs)


class CalculatorService:
    def add(self, a, b):
        return a + b
    def sub(self, a, b):
        return a - b

def get_calculator_service():
    return CalculatorService()


app = SwiftBots()

calc_bot = ChatBot()

@calc_bot.listener()
async def listen_async():
    print("Welcome in the command line chat! Good day, Friend!")
    print("Type expression to solve like `add 2 2` or `- 70 1`")
    while True:
        message = await input_async('-> ')
        yield {
            'message': message,
            'user': 'Schweine'
        }

@calc_bot.sender()
async def send_async(message, user):
    await print_async(message)

@calc_bot.command_handler(commands=['+', 'add'])
async def add(message: str, logger: ILogger, chat: calc_bot.Chat):
    await logger.debug_async(f'User is requesting ADD operation: {message}')
    num1, num2 = message.split(' ')
    result = float(num1) + float(num2)
    await chat.reply_async(str(result))

@calc_bot.command_handler(commands=['-', 'sub'])
async def subtract(message: str, logger: ILogger, chat: calc_bot.Chat):
    await logger.debug_async(f'User is requesting ADD operation: {message}')
    num1, num2 = message.split(' ')
    result = float(num1) - float(num2)
    await chat.reply_async(str(result))

@calc_bot.default_handler()
async def default_handler(message: str, logger: ILogger, chat: calc_bot.Chat):
    await chat.reply_async(f'Unknown command: {message}')

@calc_bot.task(PeriodTrigger(seconds=5), run_at_start=True, name='my-task')
async def period_printer(
        logger: ILogger,
        calculator: CalculatorService = depends(get_calculator_service),
):
    r = random.Random()
    result = calculator.add(r.randint(1000, 4999), r.randint(1000, 5000))
    await logger.report_async(str(result))


app = SwiftBots([calc_bot])

app.run()
