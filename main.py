import logging
import subprocess
import requests
from aiogram.utils import markdown as md
from aiogram import Bot, Dispatcher, executor, types

API_TOKEN = ''
PROXY_URL = ''
SHOW_PUBLIC_IP = False

logging.basicConfig(level=logging.INFO)
bot = Bot(token=API_TOKEN, proxy=PROXY_URL)
dp = Dispatcher(bot)


def icmp_ping(ip):
	process = subprocess.Popen(f"ping {ip} -c 4", shell=True, stdout=subprocess.PIPE)
	process.wait()
	result = ''
	for line in process.stdout.read().decode().split('\n'):
		if not ('PING' in line or '---' in line):
			result += line + '\n'
	return result.strip()


def tcp_ping(ip, port):
	# result = tcping.Ping(ip, port, 4).ping(4).result.table
	process = subprocess.Popen(f"tcping {ip} -p {port} -c 4 --report", shell=True, stdout=subprocess.PIPE)
	process.wait()
	result_arr = process.stdout.read().decode().split('\n')
	keys = result_arr[-5].strip('|').split('|')
	values = result_arr[-3].strip('|').split('|')
	result = ''
	for subscript in range(2, 8):
		result += md.escape_md(keys[subscript].strip()) + ": " + md.code(values[subscript].strip()) + '\n'
	return result.strip()


@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
	content = '''
Hello!
I'm Ping Bot!
I can ping your server with ICMP or TCP protocols.

Usage:
/icmp <ip> - ICMP ping to IP
/tcp <ip> <port> - TCP ping to IP:PORT
'''
	if SHOW_PUBLIC_IP:
		ip = requests.get("https://ipinfo.io/json").json()['ip']
		await message.reply(f"{content}\nRunning on {ip}".strip())
	else:
		await message.reply(content.strip())


@dp.message_handler(commands=['icmp'])
async def icmp(message: types.Message):
	ip = message.get_args()
	logging.info(f'ICMP ping {ip}')
	if not ip:
		await message.reply("You must specify IP address!")
		return
	waiting_message = await message.reply(f"ICMP pinging to {ip} ...")
	try:
		result = icmp_ping(ip)
		if result:
			await waiting_message.edit_text(f"ICMP ping to {ip}:\n{result}")
		else:
			await waiting_message.edit_text(f"ICMP ping to {ip}:\nNo result")
	except Exception as e:
		await waiting_message.edit_text(f"ICMP ping to {ip}:\n{e}")


@dp.message_handler(commands=['tcp'])
async def tcp(message: types.Message):
	args = message.get_args().split()
	if len(args) < 2:
		await message.reply("You must specify IP address and port!")
		return
	ip = args[0]
	port = args[1]
	logging.info(f'TCP ping {ip} {port}')
	waiting_message = await message.reply(f"TCP pinging to {ip}:{port} ...")
	try:
		result = tcp_ping(ip, port)
		await waiting_message.edit_text(md.escape_md(f"TCP ping to {ip}:{port}:\n") + result, parse_mode='MarkdownV2')
	except Exception as e:
		await waiting_message.edit_text(f"TCP ping to {ip}:{port}:\n{e}")


if __name__ == '__main__':
	executor.start_polling(dp)
