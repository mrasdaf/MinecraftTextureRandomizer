import os
import random
from zipfile import ZipFile
import shutil
import sys

help = """
Minecraft Texture Randomizer
by mrasdaf

https://github.com/mrasdaf/MinecraftTextureRandomizer

/mode:X - Режим работы программы, версия 1.12 и ниже - /mode:0, версия 1.13 и выше - /mode:1
/dir:"" - Папка .minecraft
/version:"Fabric 1.16.5" - Имя версии, текстуры которой нужно рандомизировать

"""

def ParseArguments(arguments):
	for arg in arguments:
		if arg == "/mode:0":
			mode = arg.split("/mode:")[1]
		if arg == "/mode:1":
			mode = arg.split("/mode:")[1]
		if "/dir:" in arg:
			dir = arg.split("/dir:")[1]
		if "/version:" in arg:
			version = arg.split("/version:")[1]
	try:
		return [mode, dir, version]
	except Exception as e:
		print(help)
		print("Ошибка: Недостаточно аргументов")
		sys.exit()
settings = ParseArguments(sys.argv)


if os.path.exists(settings[1]):
	minecraft = settings[1]  # minecraft dir
else:
	print("Ошибка: Неверный /dir:")
	sys.exit()
versions = minecraft + R'\versions' # versions dir
if os.path.exists(settings[1] + "\\versions\\" + settings[2]):
	ver = settings[2] # version name
else:
	print("Ошибка: Неверный /version:")
	sys.exit()
if not settings[0] == "0":
	if not settings[0] == "1":
		print("Ошибка: неверный /mode:")
		sys.exit()
mode = int(settings[0])

def RandomizeFiles(dir):
	files = os.listdir(dir)
	cwd = os.getcwd()
	os.chdir(dir)
	for i in range(len(files)*2):
		try:
			shutil.copyfile(random.choice(files), random.choice(files))
		except Exception as e:
			pass
	os.chdir(cwd)


# for ver in os.listdir(versions):
# 	print(ver)
# ver = input("\nВыберите версию: ")

print("Распаковка текстур...")
if not os.path.exists(ver):
	with ZipFile(f"{versions}\\{ver}\\{ver}.jar", 'r') as j:
		for file in j.namelist():
			if file.startswith('assets/'):
				j.extract(file, ver)
print("Рандомизация блоков...")
try:
	if mode == 0:
		RandomizeFiles(f"{ver}\\assets\\minecraft\\textures\\blocks")
	elif mode == 1:
		RandomizeFiles(f"{ver}\\assets\\minecraft\\textures\\block")
	print("Рандомизация предметов...")
	if mode == 0:
		RandomizeFiles(f"{ver}\\assets\\minecraft\\textures\\items")
	elif mode == 1:
		RandomizeFiles(f"{ver}\\assets\\minecraft\\textures\\item")
	print("Сборка ресурспака...")
	if mode == 0:
		shutil.copytree(f"{ver}\\assets\\minecraft\\textures\\blocks", f"{ver} randomized\\assets\\minecraft\\textures\\blocks")
		shutil.copytree(f"{ver}\\assets\\minecraft\\textures\\items", f"{ver} randomized\\assets\\minecraft\\textures\\items")
	elif mode == 1:
		shutil.copytree(f"{ver}\\assets\\minecraft\\textures\\block", f"{ver} randomized\\assets\\minecraft\\textures\\block")
		shutil.copytree(f"{ver}\\assets\\minecraft\\textures\\item", f"{ver} randomized\\assets\\minecraft\\textures\\item")
	shutil.rmtree(ver)
	if mode == 0:
		shutil.copy("mcmeta\\pack.mcmeta", f"{ver} randomized\\pack.mcmeta")
	elif mode == 1:
		shutil.copy("mcmeta\\pack1.mcmeta", f"{ver} randomized\\pack.mcmeta")
except Exception as e:
	print(e, "\nПроизошла ошибка")
shutil.make_archive(f"{ver} randomized", 'zip', f"{ver} randomized")
shutil.rmtree(f"{ver} randomized")