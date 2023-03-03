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
		print("")
		input("Нажмите Enter для закрытия...")
		sys.exit(0)
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
with ZipFile(f"{versions}\\{ver}\\{ver}.jar", 'r') as j:
	# Текстуры блоков
	if mode == 1:
		for file in j.namelist():
			if file.startswith('assets/minecraft/textures/block/'):
				j.extract(file, f"tmp\\{ver}\\block")
	if mode == 0:
		for file in j.namelist():
			if file.startswith('assets/minecraft/textures/blocks/'):
				j.extract(file, f"tmp\\{ver}\\blocks")

	# Текстуры предметов
	if mode == 1:
		for file in j.namelist():
			if file.startswith('assets/minecraft/textures/item/'):
				j.extract(file, f"tmp\\{ver}\\item")
	if mode == 0:
		for file in j.namelist():
			if file.startswith('assets/minecraft/textures/items/'):
				j.extract(file, f"tmp\\{ver}\\items")
print("Рандомизация блоков...")
try:
	if mode == 0:
		RandomizeFiles(f"tmp\\{ver}\\blocks\\assets\\minecraft\\textures\\blocks")
		#print(1)
	elif mode == 1:
		RandomizeFiles(f"tmp\\{ver}\\block\\assets\\minecraft\\textures\\block")
		#print(1)
	print("Рандомизация предметов...")
	if mode == 0:
		RandomizeFiles(f"tmp\\{ver}\\items\\assets\\minecraft\\textures\\items")
		#print(1)
	elif mode == 1:
		RandomizeFiles(f"tmp\\{ver}\\item\\assets\\minecraft\\textures\\item")
		#print(1)
	print("Сборка ресурспака...")
	if mode == 0:
		shutil.move(f"tmp\\{ver}\\blocks\\assets\\minecraft\\textures\\blocks", f"tmp\\{ver} randomized\\assets\\minecraft\\textures\\blocks")
		shutil.move(f"tmp\\{ver}\\items\\assets\\minecraft\\textures\\items", f"tmp\\{ver} randomized\\assets\\minecraft\\textures\\items")
	elif mode == 1:
		shutil.move(f"tmp\\{ver}\\block\\assets\\minecraft\\textures\\block", f"tmp\\{ver} randomized\\assets\\minecraft\\textures\\block")
		shutil.move(f"tmp\\{ver}\\item\\assets\\minecraft\\textures\\item", f"tmp\\{ver} randomized\\assets\\minecraft\\textures\\item")
	if mode == 0:
		shutil.copy("mcmeta\\pack.mcmeta", f"tmp\\{ver} randomized\\pack.mcmeta")
	elif mode == 1:
		shutil.copy("mcmeta\\pack1.mcmeta", f"tmp\\{ver} randomized\\pack.mcmeta")
except Exception as e:
	print(e, "\nПроизошла ошибка, проверьте значение /mode:")
	sys.exit(1)
shutil.make_archive(f"tmp\\{ver} randomized", 'zip', f"tmp\\{ver} randomized")
shutil.move(f"tmp\\{ver} randomized.zip", f"{ver} randomized.zip")
shutil.rmtree(f"tmp\\{ver} randomized")
shutil.rmtree("tmp")