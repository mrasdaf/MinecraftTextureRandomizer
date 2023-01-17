import os
import random
from zipfile import ZipFile
import shutil
import config
minecraft = config.MINECRAFT
versions = minecraft + R'\versions'

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

for ver in os.listdir(versions):
	print(ver)
ver = input("\nВыберите версию: ")


if os.path.exists(f"{versions}\\{ver}"):
	print("Распаковка текстур...")
	if not os.path.exists(ver):
		with ZipFile(f"{versions}\\{ver}\\{ver}.jar", 'r') as j:
			for file in j.namelist():
				if file.startswith('assets/'):
					j.extract(file, ver)
	print("Рандомизация блоков...")
	try:
		if config.MODE == 0:
			RandomizeFiles(f"{ver}\\assets\\minecraft\\textures\\blocks")
		elif config.MODE == 1:
			RandomizeFiles(f"{ver}\\assets\\minecraft\\textures\\block")
		print("Рандомизация предметов...")
		if config.MODE == 0:
			RandomizeFiles(f"{ver}\\assets\\minecraft\\textures\\items")
		elif config.MODE == 1:
			RandomizeFiles(f"{ver}\\assets\\minecraft\\textures\\item")
		print("Сборка ресурспака...")
		if config.MODE == 0:
			shutil.copytree(f"{ver}\\assets\\minecraft\\textures\\blocks", f"{ver} randomized\\assets\\minecraft\\textures\\blocks")
			shutil.copytree(f"{ver}\\assets\\minecraft\\textures\\items", f"{ver} randomized\\assets\\minecraft\\textures\\items")
		elif config.MODE == 1:
			shutil.copytree(f"{ver}\\assets\\minecraft\\textures\\block", f"{ver} randomized\\assets\\minecraft\\textures\\block")
			shutil.copytree(f"{ver}\\assets\\minecraft\\textures\\item", f"{ver} randomized\\assets\\minecraft\\textures\\item")
		shutil.rmtree(ver)
		if config.MODE == 0:
			shutil.copy("pack.mcmeta", f"{ver} randomized\\pack.mcmeta")
		elif config.MODE == 1:
			shutil.copy("pack1.mcmeta", f"{ver} randomized\\pack.mcmeta")
	except Exception as e:
		print(e, "\nПроизошла ошибка, проверьте что вы установили в конфиге правильное значение MODE")
	shutil.make_archive(f"{ver} randomized", 'zip', f"{ver} randomized")
	shutil.rmtree(f"{ver} randomized")

else:
	print("Такой версии не существует")