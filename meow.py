# coding: utf-8
import os, sys
from time import sleep
from random import randint
try: from playsound import playsound
except: pass

class Meow_Fighter():
	def __init__(self, rpg_class, weapon, armor, life_run):
		self.is_player = False
		self.autoRun = False
		self.rpg_class = rpg_class	# 1- warrior 2- sorcerer 3-rogue
		self.weapon = weapon -1		# 1- no 2- sword 3- staff 4- dagger
		self.armor = armor-1		# 1- no 2- leather 3- steel

		self.life = 10
		self.life_run = life_run	# run if under this amount

		self.strength     = 1 if rpg_class == 1 else 0
		self.intelligence = 1 if rpg_class == 2 else 0
		self.stealth 	  = 1 if rpg_class == 3 else 0

	def dice(self,qtd,number):
		if not self.autoRun and self.is_player: # player throw the dices
			entry = ""
			text = "/"+str(qtd)+"d"+str(number)
			while entry != text and not self.autoRun:
				entry = input("type "+text+" to run the dice (or /autorun to throw automatically)\n")
				if entry == "/autorun": self.autoRun = not self.autoRun
		sum = 0
		for _ in range(qtd):
			sum += randint(1,number)
		sleep(0.5)
		return sum

	def set_is_player(self):
		self.is_player = True

	def change_autorun(self, *args):
		try:
			self.autoRun = args[0]
		except:
			self.autoRun = not self.autoRun

	def attack(self):
		chance = self.dice(1,20)	# 1D20
		if self.rpg_class == self.weapon: chance += 2
		return chance

	def doge(self):
		chance = self.dice(1,20)
		return chance

	def take_damage(self, damage):
		damage = damage - (self.armor * 2)
		if damage < 0: damage = 0
		self.life -= damage
		return damage

	def is_alive(self):
		return self.life > 0

	def run_away(self):
		return self.life <= self.life_run

	def deal_damage(self):
		damage = self.dice(1,8)	# 1D8
		damage += self.strength * 2
		return damage

	def try_critical(self):
		luck = self.dice(1,20)	# 1D20
		luck += (self.intelligence + self.stealth) * 2
		return luck

class Meow():
	def __init__(self):
		self.english = True
		self.print_images = True
		self.play_sound = True
		self.autoRun = False
		self.last_text = ""
		self.text_list = []
		with open("text.txt", 'r') as f:
			for line in f:
				self.text_list.append(line[:-1])

		#
		self.coins = 0				#
		self.clothes = 1			# 1- no 2- normal 3- fancy
		self.help = 3				# 1- Fig1 or 2- Fig or 3- none

	def meow_say(self, i):
		if self.play_sound:
			try:
				playsound("meow"+str(i)+".mp3")
			except:
				os.system("start meow"+str(i)+".mp3")
				sleep(1.5)

	def meows(self, text):
		list_words = text.split()
		new_text = ""
		for word in list_words:
			punctuation = ""
			for l in word:
				if l == "." or l == "," or l == ":" or l == "?" or l == "-":
					punctuation = l
			new_text += "meow"+punctuation+" "
		# new_text = "meow " * len(list_words)
		self.last_text = text
		if self.english: return text	# get english text
		return new_text

	def meow_get_input(self):
		while True:
			all_meows = True
			n_meows = 0
			for word in input().split():
				if   word == "/meow":
					self.english = not self.english
					self.meow_print(self.last_text)
					all_meows = False
				elif word == "/print_images":
					self.print_images = not self.print_images
					all_meows = False
					self.meow_print("changed to "+str(self.print_images))
				elif word == "/play_sound":
					self.play_sound = not self.play_sound
					all_meows = False
					self.meow_print("changed to "+str(self.play_sound))
				elif word == "/autorun":
					try: self.fighter.change_autorun()
					except: self.autoRun = not self.autoRun
					self.meow_print("changed autoRun preferences")
					all_meows = False
				elif word != "meow":
					all_meows = False
					self.meow_print("sorry, i didn't understand that, can you repeat?")

				n_meows += 1
			if all_meows:
				return n_meows

	def meow_print(self, text, *args):
		text = self.meows(text)
		for i in range(len(text)):
			sys.stdout.write('\r'+text[:i+1])
			sys.stdout.flush()
			try:
				sleep(args[0])
			except:
				sleep(0.05)
		# go to next line
		print()

	def meow_print_line(self, i):
		text = self.text_list[i].split(" ", 1)[1]
		self.meow_print(text)

	def meow_misspell_print_line(self, i1, i2):
		text1 = self.text_list[i1].split(" ", 1)[1]
		text2 = self.text_list[i2].split(" ", 1)[1]
		remove = "_" * len(text1)
		self.meow_misspell_print(text1+remove+text2)

	def meow_misspell_print(self, text, *args):
		text = self.meows(text)
		# tranforms "abcef__def" to "abcef__  __def"
		# using this trick it will erase the word first, istead of just writing over
		new_text = []
		old_l = None
		n_ = 0
		for l in text:
			if l == "_":
				n_ += 1
			if old_l == "_" and l != "_":
				new_text.append(" "*n_ + "_"*n_)
				n_ = 0
			old_l = l
			new_text.append(l)
		text = "".join(new_text)
		# tranforms "abcef__def" to "abcdef"
		new_text = []
		for l in text:
			if l == "_":
				new_text.pop(-1)
			else:
				new_text.append(l)
			# prints the sequence
			sys.stdout.write('\r'+"".join(new_text))
			sys.stdout.flush()
			try:
				sleep(args[0])
			except:
				sleep(0.05)
		# go to next line
		print()

	def change_to_space(self, line):
		# change . to space
		new_line = []
		beggin = True
		for l in line:
			if l != "." and l != " ": beggin = False
			if l == "." and beggin: l = " "
			new_line.append(l)
		return new_line

	def meow_draw(self, i):
		if self.print_images:
			with open("meow"+str(i)+".txt", 'r') as f:
				for line in f:
					new_line = self.change_to_space(line[:-1])
					new_line = self.change_to_space(new_line[::-1])[::-1]
					new_line = "".join(new_line)
					# see if its only spaces
					just_spaces = True
					for l in new_line:
						if l != " ": just_spaces = False
					if not just_spaces:
						print(new_line)
						sleep(0.1)
			# go to next line
			print()

	def meow_try_buy(self, prices):
		while True:
			n = self.meow_get_input()
			if n < 1: n = 1
			if n > len(prices): n =1
			if prices[n-1] > self.coins:
				self.meow_print("sorry you dont have enough money, try again")
			else:
				self.coins -= prices[n-1]
				return n

	def meow_create_fighter(self, rpg_class, weapon, armor):
		self.fighter = Meow_Fighter(rpg_class, weapon, armor, 0)
		self.fighter.set_is_player()
		self.fighter.change_autorun(self.autoRun)

	def meow_turn(self, order, text):
		for i in range(2):
			j = (i+1)%2
			if not order[i].is_alive():
				continue
			sleep_time = 1
			# atack
			self.meow_print(text[i]+" attack dice: ")
			attack = order[i].attack()
			self.meow_print(str(attack))
			sleep(sleep_time)
			# doge
			self.meow_print(text[j]+" doge dice: ")
			doge = order[j].doge()
			self.meow_print(str(doge))
			sleep(sleep_time)
			if attack >= doge:
				# damage
				self.meow_print(text[i][:-1]+" hit the attack")
				sleep(sleep_time)
				self.meow_print("deals:")
				damage = order[i].deal_damage()
				# critical
				if order[i].is_player:
					self.meow_print("try get a critical hit:")
				critical = order[i].try_critical()
				if order[i].is_player:
					self.meow_print(str(critical))
				if critical >= 20:
					self.meow_print("critical hit")
					damage = damage * 2
				self.meow_print(str(damage)+" damage")
				# take damage
				sleep(sleep_time)
				damage = order[j].take_damage(damage)
				self.meow_print(text[j][:-1]+" took "+str(damage)+" damage")
			else:
				self.meow_print(text[i][:-1]+" miss the attack")
			sleep(sleep_time)

	def meow_fight(self,enemy):
		self.meow_print("a fight starts")
		order = [self.fighter, enemy]
		order.append(order.pop(randint(0,1)))	# random who goes first
		text = ["your","enemys"] if order[0].is_player else ["enemys","your"]
		while True:
			self.meow_turn(order, text)
			ret = 0
			if not self.fighter.is_alive():
				self.meow_print("you died")
				return 0
			elif not enemy.is_alive():
				self.meow_print("you kill the enemy")
				ret = 1
			elif enemy.run_away():
				self.meow_print("the enemy run away to prevent dying")
				ret = 2
			if ret == 2 or ret == 1:
				self.meow_print("you leave the combat with "+str(self.fighter.life)+" life points")
				return ret

def meow():
	meow = Meow()
	meow.meow_print("MEOW the game", 0.1)
	# basics
	meow.meow_print_line(0)
	meow.meow_get_input()
	meow.meow_draw(1)
	meow.meow_say(1)
	meow.meow_print_line(1)
	meow.meow_print_line(2)
	meow.meow_print_line(3)
	while meow.meow_get_input() != 5:
		meow.meow_print_line(4)
	meow.meow_print_line(5)
	meow.meow_print_line(6)
	meow.meow_print_line(7)
	# class
	n = meow.meow_get_input()
	if not (n == 2 or n == 3): n = 1
	rpg_class = n
	meow.meow_print_line(8)
	meow.coins = 50
	# store
	meow.meow_draw(2)
	meow.meow_say(2)
	meow.meow_misspell_print_line(9, 10)
	meow.meow_print_line(11)
	meow.meow_print_line(12)
	meow.clothes = meow.meow_try_buy([0, 10, 30])		# no normal fancy
	meow.meow_print_line(13)
	meow.meow_print_line(14)
	weapon = meow.meow_try_buy([0, 25, 25, 10])	# no sword staff dagger
	meow.meow_print_line(15)
	meow.meow_print_line(16)
	armor = meow.meow_try_buy([0, 15, 30])			# no leather steel
	meow.meow_create_fighter(rpg_class, weapon, armor)
	meow.meow_print_line(17)
	# street fight
	meow.meow_print_line(18)
	meow.meow_print_line(19)
	meow.meow_draw(3)
	meow.meow_say(3)
	meow.meow_print_line(20)
	meow.meow_draw(4)
	meow.meow_say(4)
	meow.meow_print_line(21)
	meow.meow_print_line(22)
	n = meow.meow_get_input()
	destiny = randint(1,2)
	# create the atacker
	attacker = Meow_Fighter(3,2,1,6)
	if n == 1:		# help Fig1
		meow.help = 1
		meow.meow_print_line(23)
		# fig1 is right (he got robbed)
		if destiny == 1:
			meow.meow_print_line(24)
			meow.meow_print_line(25)
			meow.coins += 20
		# fig2 is right	(he didnt steal)
		else:
			meow.meow_print_line(26)
			result = meow.meow_fight(attacker)
			if result == 2:			# the enemy run away
				meow.meow_print_line(27)
			elif result == 1:		# kill the enemy
				meow.meow_print_line(28)
				meow.meow_print_line(29)
				meow.meow_print_line(30)
				meow.meow_print_line(31)
				meow.meow_create_fighter(rpg_class, 1, 1)
				meow.coins = 0
				meow.clothes = 1
			else:					# you died
				meow.meow_print_line(32)
				meow.fighter.life = 3
				meow.meow_print("you have 3 life points")
	elif n == 2:	# help Fig2
		meow.help = 2
		meow.meow_print_line(33)
		# fig1 is right (he got robbed)
		if destiny == 1:
			meow.meow_print_line(34)
			meow.meow_print_line(35)
			meow.fighter.life -= 4
		# fig2 is right	(he didnt steal)
		else:
			meow.meow_print_line(36)
			meow.meow_print_line(37)
			meow.fighter.armor += 1
	else:			# help none
		meow.help = 3
	# leave the city
	meow.meow_print_line(38)
	meow.meow_print_line(39)
	meow.meow_print_line(40)
	meow.meow_misspell_print_line(41, 42)
	# create the atacker
	attacker = Meow_Fighter(1,2,3,0)
	result = meow.meow_fight(attacker)
	if result == 1:		# kill the enemy
		meow.meow_print_line(43)
	else:					# you died
		meow.meow_print_line(44)
		meow.meow_print_line(45)
	meow.meow_print_line(46)
	meow.meow_misspell_print_line(47, 48)
	meow.meow_print_line(49)

meow()
