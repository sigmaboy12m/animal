#!/usr/bin/env python3
# Animal Rush backend - Railway edition (zero dependency, python stdlib only).
import json, os, random, threading, time
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

PORT = int(os.environ.get('PORT', '8899'))
HOST = '0.0.0.0'
DATA_DIR = os.environ.get('DATA_DIR', os.path.dirname(os.path.abspath(__file__)))
STATE_FILE = os.path.join(DATA_DIR, 'state.json')

CHARS = [
    {"id": 1, "name": "Freddy", "path": "res://assets/characters/Human/human.tscn", "card_path": "res://assets/characters/2D Card/Freddy_card.png", "tier": "Common"},
    {"id": 2, "name": "Frog", "path": "res://assets/characters/Frog/Frog.tscn", "card_path": "res://assets/characters/2D Card/Frog_card.png", "tier": "Common"},
    {"id": 3, "name": "Fox", "path": "res://assets/characters/Fox/Fox.tscn", "card_path": "res://assets/characters/2D Card/Fox_card.png", "tier": "Common"},
    {"id": 4, "name": "Horse", "path": "res://assets/characters/Horse/horse.tscn", "card_path": "res://assets/characters/2D Card/Horse_card.png", "tier": "Rare"},
    {"id": 5, "name": "Leopard", "path": "res://assets/characters/Leopard/Leopard.tscn", "card_path": "res://assets/characters/2D Card/Leopard_card.png", "tier": "Common"},
    {"id": 6, "name": "Tourist", "path": "res://assets/characters/Tourist/Tourist.tscn", "card_path": "res://assets/characters/2D Card/Ecotourist_card.png", "tier": "Rare"},
    {"id": 7, "name": "Sheep", "path": "res://assets/characters/Sheep/Sheep.tscn", "card_path": "res://assets/characters/2D Card/Sheep_card.png", "tier": "Common"},
    {"id": 8, "name": "Rabbit", "path": "res://assets/characters/Rabbid/Rabbid.tscn", "card_path": "res://assets/characters/2D Card/Rabbid_card.png", "tier": "Common"},
    {"id": 9, "name": "Monkey", "path": "res://assets/characters/Monkey/Monkey.tscn", "card_path": "res://assets/characters/2D Card/Monkey_card.png", "tier": "Common"},
    {"id": 10, "name": "Elephant", "path": "res://assets/characters/Elephant/Elephant.tscn", "card_path": "res://assets/characters/2D Card/Elephant_card.png", "tier": "Common"},
    {"id": 11, "name": "Lion", "path": "res://assets/characters/Lion/Lion.tscn", "card_path": "res://assets/characters/2D Card/Lion_card.png", "tier": "Common"},
    {"id": 12, "name": "Bear", "path": "res://assets/characters/Bear/Bear.tscn", "card_path": "res://assets/characters/2D Card/Bear_card.png", "tier": "Common"},
    {"id": 13, "name": "Samurai Bear", "path": "res://assets/characters/Bear/Samurai_Bear.tscn", "card_path": "res://assets/characters/2D Card/Samurai_Bear_card.png", "tier": "Legendary"},
    {"id": 14, "name": "Samurai Elephant", "path": "res://assets/characters/Elephant/Samurai_elephant.tscn", "card_path": "res://assets/characters/2D Card/Samurai_Elephant_card.png", "tier": "Legendary"},
    {"id": 15, "name": "Samurai Fox", "path": "res://assets/characters/Fox/Samurai_fox.tscn", "card_path": "res://assets/characters/2D Card/Samurai_Fox_card.png", "tier": "Legendary"},
    {"id": 16, "name": "Samurai Horse", "path": "res://assets/characters/Horse/Samurai_horse.tscn", "card_path": "res://assets/characters/2D Card/Samurai_Horse_card.png", "tier": "Legendary"},
    {"id": 17, "name": "Samurai Leopard", "path": "res://assets/characters/Leopard/Samurai_leopard.tscn", "card_path": "res://assets/characters/2D Card/Samurai_Leopard_card.png", "tier": "Legendary"},
    {"id": 18, "name": "Samurai Monkey", "path": "res://assets/characters/Monkey/Samurai_Monkey.tscn", "card_path": "res://assets/characters/2D Card/Samurai_Monkey_card.png", "tier": "Legendary"},
    {"id": 19, "name": "Samurai Lion", "path": "res://assets/characters/Lion/Samurai_Lion.tscn", "card_path": "res://assets/characters/2D Card/Samurai_Lion_card.png", "tier": "Legendary"},
    {"id": 20, "name": "Samurai Rabbit", "path": "res://assets/characters/Rabbid/Samurai_Rabbid.tscn", "card_path": "res://assets/characters/2D Card/Samurai_Rabbid_card.png", "tier": "Legendary"},
    {"id": 21, "name": "Samurai Sheep", "path": "res://assets/characters/Sheep/Samurai_Sheep.tscn", "card_path": "res://assets/characters/2D Card/Samurai_Sheep_card.png", "tier": "Legendary"},
    {"id": 33, "name": "Samurai Frog", "path": "res://assets/characters/Frog/Samurai_frog.tscn", "card_path": "res://assets/characters/2D Card/Samurai_Frog_card.png", "tier": "Legendary"},
    {"id": 22, "name": "Astronaut Bear", "path": "res://assets/characters/Astronaut/Astronaut_bear.tscn", "card_path": "res://assets/characters/2D Card/Astronaut_Bear_card.png", "tier": "Legendary"},
    {"id": 23, "name": "Astronaut Elephant", "path": "res://assets/characters/Astronaut/Astronaut_elephant.tscn", "card_path": "res://assets/characters/2D Card/Astronaut_Elephant_card.png", "tier": "Legendary"},
    {"id": 24, "name": "Astronaut Fox", "path": "res://assets/characters/Astronaut/Astronaut_fox.tscn", "card_path": "res://assets/characters/2D Card/Astronaut_Fox_card.png", "tier": "Legendary"},
    {"id": 25, "name": "Astronaut Frog", "path": "res://assets/characters/Astronaut/Astronaut_frog.tscn", "card_path": "res://assets/characters/2D Card/Astronaut_Frog_card.png", "tier": "Legendary"},
    {"id": 26, "name": "Astronaut Horse", "path": "res://assets/characters/Astronaut/Astronaut_horse.tscn", "card_path": "res://assets/characters/2D Card/Astronaut_Horse_card.png", "tier": "Legendary"},
    {"id": 27, "name": "Astronaut Leopard", "path": "res://assets/characters/Astronaut/Astronaut_leopard.tscn", "card_path": "res://assets/characters/2D Card/Astronaut_Leopard_card.png", "tier": "Legendary"},
    {"id": 28, "name": "Astronaut Lion", "path": "res://assets/characters/Astronaut/Astronaut_lion.tscn", "card_path": "res://assets/characters/2D Card/Astronaut_Lion_card.png", "tier": "Legendary"},
    {"id": 29, "name": "Astronaut Monkey", "path": "res://assets/characters/Astronaut/Astronaut_monkey.tscn", "card_path": "res://assets/characters/2D Card/Astronaut_Monkey_card.png", "tier": "Legendary"},
    {"id": 30, "name": "Astronaut Rabbit", "path": "res://assets/characters/Astronaut/Astronaut_rabbit.tscn", "card_path": "res://assets/characters/2D Card/Astronaut_Rabbid_card.png", "tier": "Legendary"},
    {"id": 31, "name": "Astronaut Sheep", "path": "res://assets/characters/Astronaut/Astronaut_sheep.tscn", "card_path": "res://assets/characters/2D Card/Astronaut_Sheep_card.png", "tier": "Legendary"},
    {"id": 32, "name": "Azari", "path": "res://assets/characters/AzariOutfits/human_azari.tscn", "card_path": "res://assets/characters/2D Card/Human_Azzari_Card.png", "tier": "Rare"},
    {"id": 34, "name": "Kurd", "path": "res://assets/characters/Kurd/human_kurd.tscn", "card_path": "res://assets/characters/2D Card/Human_Kurd_Card.png", "tier": "Rare"},
    {"id": 35, "name": "Parinaz", "path": "res://assets/characters/Human/Farinaz.tscn", "card_path": "res://assets/characters/2D Card/Farinaz_card.png", "tier": "Common"},
    {"id": 43, "name": "Dog", "path": "res://assets/characters/Dog/Dog.tscn", "card_path": "res://assets/characters/2D Card/Dog_card.png", "tier": "Common"},
    {"id": 44, "name": "Rhino", "path": "res://assets/characters/Rhino/Rhino.tscn", "card_path": "res://assets/characters/2D Card/Rhino_card.png", "tier": "Rare"},
    {"id": 45, "name": "Penguin", "path": "res://assets/characters/Penguin/Penguin.tscn", "card_path": "res://assets/characters/2D Card/Penguin_card.png", "tier": "Common"},
    {"id": 46, "name": "Shark", "path": "res://assets/characters/Shark/Shark.tscn", "card_path": "res://assets/characters/2D Card/Shark_card.png", "tier": "Rare"},
    {"id": 48, "name": "Police", "path": "res://assets/characters/Police/Police.tscn", "card_path": "res://assets/characters/2D Card/Police_card.png", "tier": "Legendary"},
    {"id": 47, "name": "Kouroosh", "path": "res://assets/characters/Kouroosh/Kouroosh.tscn", "card_path": "res://assets/characters/2D Card/Kouroosh_card.png", "tier": "Epic"},
    {"id": 49, "name": "Mia", "path": "res://assets/characters/Mia/Mia.tscn", "card_path": "res://assets/characters/2D Card/Mia_card.png", "tier": "Epic"},
    {"id": 50, "name": "Nopo", "path": "res://assets/characters/Nopo/Nopo.tscn", "card_path": "res://assets/characters/2D Card/Nopo_card.png", "tier": "Epic"},
    {"id": 51, "name": "Lor", "path": "res://assets/characters/Lor/Lor.tscn", "card_path": "res://assets/characters/2D Card/Lor_card.png", "tier": "Rare"},
    {"id": 52, "name": "Panda", "path": "res://assets/characters/Panda/Panda.tscn", "card_path": "res://assets/characters/2D Card/Panda_card.png", "tier": "Rare"},
    {"id": 53, "name": "Ninja", "path": "res://assets/characters/Ninja/Ninja.tscn", "card_path": "res://assets/characters/2D Card/Ninja_card.png", "tier": "Epic"},
    {"id": 54, "name": "Bee", "path": "res://assets/characters/Bee/Bee.tscn", "card_path": "res://assets/characters/2D Card/Bee_card.png", "tier": "Legendary"},
    {"id": 55, "name": "NaderShah", "path": "res://assets/characters/Nadershah/Nadershah.tscn", "card_path": "res://assets/characters/2D Card/Nadershah_card.png", "tier": "Epic"},
    {"id": 56, "name": "Patrick", "path": "res://assets/characters/Patrick/Patrick.tscn", "card_path": "res://assets/characters/2D Card/Patrick_card.png", "tier": "Epic"},
    {"id": 57, "name": "SpongeBob", "path": "res://assets/characters/SpongeBob/SpongeBob.tscn", "card_path": "res://assets/characters/2D Card/SpongeBob_card.png", "tier": "Epic"},
    {"id": 58, "name": "Engineer", "path": "res://assets/characters/Engineer/Engineer.tscn", "card_path": "res://assets/characters/2D Card/Engineer_card.png", "tier": "Rare"},
    {"id": 59, "name": "Graduated", "path": "res://assets/characters/Graduated/Graduated.tscn", "card_path": "res://assets/characters/2D Card/Graduated_card.png", "tier": "Rare"},
    {"id": 60, "name": "Leonardo", "path": "res://assets/characters/TMNT/Leonardo/Leonardo.tscn", "card_path": "res://assets/characters/2D Card/Leonardo_card.png", "tier": "Legendary"},
    {"id": 61, "name": "Rapheal", "path": "res://assets/characters/TMNT/Raphaeal/Raphael.tscn", "card_path": "res://assets/characters/2D Card/Rapheal_card.png", "tier": "Legendary"},
    {"id": 62, "name": "Danatello", "path": "res://assets/characters/TMNT/donatello/Danatello.tscn", "card_path": "res://assets/characters/2D Card/Danatello_card.png", "tier": "Legendary"},
    {"id": 63, "name": "Michelangelo", "path": "res://assets/characters/TMNT/Michelangelo/Michelangelo.tscn", "card_path": "res://assets/characters/2D Card/Michelangelo_card.png", "tier": "Legendary"},
    {"id": 64, "name": "Eren Yeager", "path": "res://assets/characters/Eren Yeager/Eren Yeager.tscn", "card_path": "res://assets/characters/2D Card/ErenYeager_card.png", "tier": "Epic"},
    {"id": 65, "name": "Soldier", "path": "res://assets/characters/Soldier/Soldier.tscn", "card_path": "res://assets/characters/2D Card/Soldier_card.png", "tier": "Legendary"},
    {"id": 66, "name": "RedHood", "path": "res://assets/characters/RedHood/RedHood.tscn", "card_path": "res://assets/characters/2D Card/RedHood_card.png", "tier": "Legendary"},
    {"id": 67, "name": "Pilot", "path": "res://assets/characters/Pilot/Pilot.tscn", "card_path": "res://assets/characters/2D Card/Pilot_card.png", "tier": "Legendary"},
    {"id": 68, "name": "Elsa", "path": "res://assets/characters/Elsa/Elsa.tscn", "card_path": "res://assets/characters/2D Card/Elsa_card.png", "tier": "Epic"},
    {"id": 69, "name": "Merida", "path": "res://assets/characters/Merida/Merida.tscn", "card_path": "res://assets/characters/2D Card/Merida_card.png", "tier": "Epic"},
    {"id": 70, "name": "Geek", "path": "res://assets/characters/Vision Pro/VisionPro.tscn", "card_path": "res://assets/characters/2D Card/VisionPro_card.png", "tier": "Legendary"},
    {"id": 71, "name": "FootBallPlayer", "path": "res://assets/characters/Football Player/FootBallPlayer.tscn", "card_path": "res://assets/characters/2D Card/FootballPlayer_card.png", "tier": "Epic"},
    {"id": 72, "name": "Scientist", "path": "res://assets/characters/Scientist/Scientist.tscn", "card_path": "res://assets/characters/2D Card/Scintist_card.png", "tier": "Legendary"},
    {"id": 73, "name": "Butcher", "path": "res://assets/characters/Butcher/Butcher.tscn", "card_path": "res://assets/characters/2D Card/Butcher_card.png", "tier": "Epic"},
    {"id": 74, "name": "Doctor", "path": "res://assets/characters/Doctor/Doctor.tscn", "card_path": "res://assets/characters/2D Card/Doctor_card.png", "tier": "Rare"},
    {"id": 75, "name": "BankClerk", "path": "res://assets/characters/BankClerk/BankClerk.tscn", "card_path": "res://assets/characters/2D Card/BankClerk_card.png", "tier": "Rare"},
    {"id": 76, "name": "Rostam", "path": "res://assets/characters/Rostam/Rostam.tscn", "card_path": "res://assets/characters/2D Card/Rostam_card.png", "tier": "Epic"},
    {"id": 77, "name": "PersianPrincess", "path": "res://assets/characters/PersianPrincess/PersianPrincess.tscn", "card_path": "res://assets/characters/2D Card/PersianPrincess_card.png", "tier": "Epic"},
    {"id": 78, "name": "AghaTakhti", "path": "res://assets/characters/AghaTakhti/AghaTakhti.tscn", "card_path": "res://assets/characters/2D Card/AghaTakhti_card.png", "tier": "Epic"},
    {"id": 79, "name": "AmirKabir", "path": "res://assets/characters/AmirKabir/AmirKabir.tscn", "card_path": "res://assets/characters/2D Card/AmirKabir_card.png", "tier": "Legendary"},
    {"id": 80, "name": "AndrewTate", "path": "res://assets/characters/AndrewTate/AndrewTate.tscn", "card_path": "res://assets/characters/2D Card/AndrewTate_card.png", "tier": "Epic"},
    {"id": 81, "name": "Batman", "path": "res://assets/characters/Batman/Batman.tscn", "card_path": "res://assets/characters/2D Card/Batman_card.png", "tier": "Epic"},
    {"id": 82, "name": "ElonMask", "path": "res://assets/characters/ElonMask/ElonMask.tscn", "card_path": "res://assets/characters/2D Card/ElonMask_card.png", "tier": "Epic"},
    {"id": 83, "name": "FireFighter", "path": "res://assets/characters/FireFighter/FireFighter.tscn", "card_path": "res://assets/characters/2D Card/FireFighter_card.png", "tier": "Rare"},
    {"id": 84, "name": "HassanYazdani", "path": "res://assets/characters/HassanYazdani/HassanYazdani.tscn", "card_path": "res://assets/characters/2D Card/HassanYazdani_card.png", "tier": "Legendary"},
    {"id": 85, "name": "HazMat", "path": "res://assets/characters/HazMat/HazMat.tscn", "card_path": "res://assets/characters/2D Card/HazMat_card.png", "tier": "Legendary"},
    {"id": 86, "name": "Jumong", "path": "res://assets/characters/Jumong/Jumong.tscn", "card_path": "res://assets/characters/2D Card/Jumong_card.png", "tier": "Epic"},
    {"id": 87, "name": "KarateKa", "path": "res://assets/characters/KarateKa/KarateKa.tscn", "card_path": "res://assets/characters/2D Card/KarateKa_card.png", "tier": "Rare"},
    {"id": 88, "name": "KaveAhangar", "path": "res://assets/characters/KaveAhangar/KaveAhangar.tscn", "card_path": "res://assets/characters/2D Card/KaveAhangar_card.png", "tier": "Epic"},
    {"id": 89, "name": "NaserAldinShah", "path": "res://assets/characters/NaserEldinShah/NaserEldinShah.tscn", "card_path": "res://assets/characters/2D Card/NaserAldinShah_Card.png", "tier": "Epic"},
    {"id": 90, "name": "PuriaVali", "path": "res://assets/characters/PuriaVali/PuriaVali.tscn", "card_path": "res://assets/characters/2D Card/PuriaVali_card.png", "tier": "Epic"},
    {"id": 91, "name": "Simurgh", "path": "res://assets/characters/Simurgh/Simurgh.tscn", "card_path": "res://assets/characters/2D Card/Simurgh_card.png", "tier": "Epic"},
    {"id": 92, "name": "WalterHazmat", "path": "res://assets/characters/HazMat/HazMatWalter.tscn", "card_path": "res://assets/characters/2D Card/WalterHazmat.png", "tier": "Epic"},
    {"id": 93, "name": "WalterWhite", "path": "res://assets/characters/WalterWhite/WalterWhite.tscn", "card_path": "res://assets/characters/2D Card/WalterWhite_card.png", "tier": "Legendary"},
    {"id": 94, "name": "ChefFemale", "path": "res://assets/characters/Chef/ChefFemale.tscn", "card_path": "res://assets/characters/2D Card/ChefFemale_Card.png", "tier": "Rare"},
    {"id": 95, "name": "ChefMale", "path": "res://assets/characters/Chef/ChefMale.tscn", "card_path": "res://assets/characters/2D Card/ChefMale_Card.png", "tier": "Rare"},
    {"id": 96, "name": "GarsonMale", "path": "res://assets/characters/Garson/GarsonMale.tscn", "card_path": "res://assets/characters/2D Card/GarsonMale_Card.png", "tier": "Rare"},
    {"id": 97, "name": "GarsonFemale", "path": "res://assets/characters/Garson/GarsonFemale.tscn", "card_path": "res://assets/characters/2D Card/GarsonFemale_Card.png", "tier": "Rare"},
    {"id": 98, "name": "Boss", "path": "res://assets/characters/Boss/Boss.tscn", "card_path": "res://assets/characters/2D Card/Boss_Card.png", "tier": "Legendary"},
    {"id": 99, "name": "DoctorFemale", "path": "res://assets/characters/Doctor/DoctorFemale.tscn", "card_path": "res://assets/characters/2D Card/DoctorFemale_Card.png", "tier": "Rare"},
    {"id": 100, "name": "Nurse", "path": "res://assets/characters/Nurse/Nurse.tscn", "card_path": "res://assets/characters/2D Card/Nurse_Card.png", "tier": "Rare"},
    {"id": 101, "name": "PoliceEntezami", "path": "res://assets/characters/PoliceEntezami/PoliceEntezami.tscn", "card_path": "res://assets/characters/2D Card/policeentezami.png", "tier": "Legendary"},
    {"id": 102, "name": "PoliceFemale", "path": "res://assets/characters/PoliceFemale/PoliceFemale.tscn", "card_path": "res://assets/characters/2D Card/pfr.png", "tier": "Legendary"},
    {"id": 103, "name": "Robber", "path": "res://assets/characters/Robber/Robber.tscn", "card_path": "res://assets/characters/2D Card/Robber.png", "tier": "Epic"},
    {"id": 104, "name": "SardarSepah", "path": "res://assets/characters/SardarSepah/SardarSepah.tscn", "card_path": "res://assets/characters/2D Card/sepah.png", "tier": "Epic"},
    {"id": 105, "name": "SardarArtesh", "path": "res://assets/characters/SardarArtesh/SardarArtesh.tscn", "card_path": "res://assets/characters/2D Card/sardarartesh.png", "tier": "Epic"},
    {"id": 106, "name": "Ronaldo", "path": "res://assets/characters/Ronaldo/Ronaldo.tscn", "card_path": "res://assets/characters/Ronaldo/ronaldorender.png", "tier": "Epic"},
    {"id": 107, "name": "Messi", "path": "res://assets/characters/Messi/Messi.tscn", "card_path": "res://assets/characters/Messi/messirender.png", "tier": "Epic"},
    {"id": 108, "name": "Nezoko", "path": "res://assets/characters/Nezoko/Nezoko.tscn", "card_path": "res://assets/characters/Nezoko/nezukorender.png", "tier": "Epic"},
    {"id": 109, "name": "SquidGame", "path": "res://assets/characters/SquidGame/SquidGame.tscn", "card_path": "res://assets/characters/SquidGame/rendersquidgame.png", "tier": "Epic"},
    {"id": 110, "name": "Tanjiro", "path": "res://assets/characters/Tanjiro/Tanjiro.tscn", "card_path": "res://assets/characters/Tanjiro/TANJIROrender.png", "tier": "Epic"},
    {"id": 111, "name": "Cyrus", "path": "res://assets/characters/Cyrus/Cyrus.tscn", "card_path": "res://assets/characters/Cyrus/Cyrusrender.png", "tier": "Epic"},
    {"id": 112, "name": "BossLady", "path": "res://assets/characters/BossLady/BossLady.tscn", "card_path": "res://assets/characters/BossLady/bossladyrender.png", "tier": "Legendary"},
    {"id": 113, "name": "Bride", "path": "res://assets/characters/Bride/Bride.tscn", "card_path": "res://assets/characters/Bride/briderender.png", "tier": "Legendary"},
    {"id": 114, "name": "Groom", "path": "res://assets/characters/Groom/Groom.tscn", "card_path": "res://assets/characters/Groom/GROOMRENDER.png", "tier": "Legendary"},
    {"id": 115, "name": "HadiChoopan", "path": "res://assets/characters/HadiChoopan/HadiChoopan.tscn", "card_path": "res://assets/characters/HadiChoopan/hadichoopanrender.png", "tier": "Epic"},
    {"id": 116, "name": "MoeinXM", "path": "res://assets/characters/MoeinXM/MoeinXM.tscn", "card_path": "res://assets/characters/2D Card/MoinXM_card.png", "tier": "Epic"},
    {"id": 117, "name": "Aghed", "path": "res://assets/characters/Aghed/Aghed.tscn", "card_path": "res://assets/characters/2D Card/Aghed_card.png", "tier": "Legendary"},
    {"id": 118, "name": "Spiderman", "path": "res://assets/characters/Spiderman/Spiderman.tscn", "card_path": "res://assets/characters/Spiderman/Spidermanrender.png", "tier": "Epic"},
    {"id": 119, "name": "ThomasShelby", "path": "res://assets/characters/ThomasShelby/ThomasShelby.tscn", "card_path": "res://assets/characters/ThomasShelby/shelbyrender.png", "tier": "Epic"},
    {"id": 120, "name": "HarryPotter", "path": "res://assets/characters/HarryPotter/HarryPotter.tscn", "card_path": "res://assets/characters/HarryPotter/HPRENDER.png", "tier": "Epic"},
    {"id": 121, "name": "AmongUs", "path": "res://assets/characters/AmongUs/AmongUs.tscn", "card_path": "res://assets/characters/AmongUs/amongusrender.png", "tier": "Epic"},
    {"id": 122, "name": "MrCrab", "path": "res://assets/characters/MrCrab/MrCrab.tscn", "card_path": "res://assets/characters/MrCrab/mrkrabsrender.png", "tier": "Epic"},
    {"id": 123, "name": "Luffy", "path": "res://assets/characters/Luffy/Luffy.tscn", "card_path": "res://assets/characters/Luffy/luffyrender.png", "tier": "Epic"},
    {"id": 124, "name": "FemaleClerk", "path": "res://assets/characters/FemaleClerk/FemaleClerk.tscn", "card_path": "res://assets/characters/FemaleClerk/FemaleClerk.png", "tier": "Rare"},
    {"id": 125, "name": "Shrek", "path": "res://assets/characters/Shrek/Shrek.tscn", "card_path": "res://assets/characters/Shrek/shrekrender.png", "tier": "Epic"},
    {"id": 126, "name": "Deadpool", "path": "res://assets/characters/Deadpool/Deadpool.tscn", "card_path": "res://assets/characters/Deadpool/DeadPool_card.png", "tier": "Epic"},
    {"id": 127, "name": "Leon", "path": "res://assets/characters/Leon/Leon.tscn", "card_path": "res://assets/characters/Leon/Leon_card.png", "tier": "Epic"},
    {"id": 128, "name": "Matilda", "path": "res://assets/characters/Matlida/Matlida.tscn", "card_path": "res://assets/characters/Matlida/Matilda_card.png", "tier": "Epic"},
    {"id": 129, "name": "ShahAbbas", "path": "res://assets/characters/ShahAbbas/ShahAbbas.tscn", "card_path": "res://assets/characters/ShahAbbas/ShahAbas.png", "tier": "Epic"},
    {"id": 130, "name": "Brucelee", "path": "res://assets/characters/Brucelee/BruceLee.tscn", "card_path": "res://assets/characters/Brucelee/bruceleerender.png", "tier": "Epic"},
    {"id": 131, "name": "DaeiHamed", "path": "res://assets/characters/DaeiHamed/DaeiHamed.tscn", "card_path": "res://assets/characters/DaeiHamed/DaiHamed_card.png", "tier": "Epic"},
    {"id": 132, "name": "Fiona", "path": "res://assets/characters/Fiona/Fiona.tscn", "card_path": "res://assets/characters/Fiona/Fiona_card.png", "tier": "Epic"},
    {"id": 133, "name": "Hitman", "path": "res://assets/characters/Hitman/Hitman.tscn", "card_path": "res://assets/characters/Hitman/hitmanrender.png", "tier": "Epic"},
    {"id": 134, "name": "Kaseb", "path": "res://assets/characters/Kaseb/Kaseb.tscn", "card_path": "res://assets/characters/Kaseb/kasebrender.png", "tier": "Epic"},
    {"id": 135, "name": "Khiabani", "path": "res://assets/characters/Khiabani/Khiabani.tscn", "card_path": "res://assets/characters/Khiabani/khiabanirender.png", "tier": "Epic"},
    {"id": 136, "name": "Looti", "path": "res://assets/characters/Looti/Looti.tscn", "card_path": "res://assets/characters/Looti/lootirender.png", "tier": "Epic"},
    {"id": 137, "name": "Mikasa", "path": "res://assets/characters/Mikasa/Mikasa.tscn", "card_path": "res://assets/characters/Mikasa/Mikasa_card.png", "tier": "Epic"},
    {"id": 138, "name": "MrBeast", "path": "res://assets/characters/MrBeast/Mrbeast.tscn", "card_path": "res://assets/characters/MrBeast/mrbeastrender.png", "tier": "Epic"},
    {"id": 139, "name": "Naruto", "path": "res://assets/characters/Naruto/Naroto.tscn", "card_path": "res://assets/characters/Naruto/narutorender.png", "tier": "Epic"},
    {"id": 140, "name": "Neymar", "path": "res://assets/characters/Neymar/Neymar.tscn", "card_path": "res://assets/characters/Neymar/neymar render.png", "tier": "Epic"},
    {"id": 141, "name": "Ragnar", "path": "res://assets/characters/Ragnar/Ragnar.tscn", "card_path": "res://assets/characters/Ragnar/ragnarrender.png", "tier": "Epic"},
    {"id": 142, "name": "Ronaldinho", "path": "res://assets/characters/Ronaldinho/Ronaldinho.tscn", "card_path": "res://assets/characters/Ronaldinho/ronaldinhorender.png", "tier": "Epic"},
    {"id": 143, "name": "Sakura", "path": "res://assets/characters/Sakura/Sakura.tscn", "card_path": "res://assets/characters/Sakura/Sakura_card.png", "tier": "Epic"},
    {"id": 144, "name": "Sandi", "path": "res://assets/characters/Sandi/Sandi.tscn", "card_path": "res://assets/characters/Sandi/Sandi_card.png", "tier": "Epic"},
    {"id": 145, "name": "Octopus", "path": "res://assets/characters/Octopus/Octopus.tscn", "card_path": "res://assets/characters/Octopus/octopusrender.png", "tier": "Epic"},
    {"id": 146, "name": "Steve", "path": "res://assets/characters/Steve/Steve.tscn", "card_path": "res://assets/characters/Steve/Steverender.png", "tier": "Epic"},
    {"id": 147, "name": "Arash", "path": "res://assets/characters/Arash/Arash.tscn", "card_path": "res://assets/characters/Arash/ArashKamanGir_card.png", "tier": "Epic"},
    {"id": 148, "name": "Diego", "path": "res://assets/characters/Diego/Diego.tscn", "card_path": "res://assets/characters/Diego/diegorender.png", "tier": "Epic"},
    {"id": 149, "name": "Manny", "path": "res://assets/characters/Manny/Manny.tscn", "card_path": "res://assets/characters/Manny/Mannyrender.png", "tier": "Special"},
    {"id": 150, "name": "Scrat", "path": "res://assets/characters/Scrat/Scrat.tscn", "card_path": "res://assets/characters/Scrat/scratrender.png", "tier": "Epic"},
    {"id": 151, "name": "Sid", "path": "res://assets/characters/Sid/Sid.tscn", "card_path": "res://assets/characters/Sid/sidrender.png", "tier": "Special"},
    {"id": 152, "name": "HassanSabbah", "path": "res://assets/characters/HassanSabbah/HassanSabbah.tscn", "card_path": "res://assets/characters/HassanSabbah/HassanSabah_card.png", "tier": "Special"},
    {"id": 153, "name": "JohnWick", "path": "res://assets/characters/John Wick/JohnWick.tscn", "card_path": "res://assets/characters/John Wick/JhonWick_card.png", "tier": "Special"},
    {"id": 154, "name": "Frontman", "path": "res://assets/characters/Frontman/Frontman.tscn", "card_path": "res://assets/characters/Frontman/frontmanrender.png", "tier": "Special"},
    {"id": 155, "name": "Ghost", "path": "res://assets/characters/Ghost/Ghost.tscn", "card_path": "res://assets/characters/Ghost/Ghost_card.png", "tier": "Special"},
    {"id": 156, "name": "Eskimoboy", "path": "res://assets/characters/Eskimoboy/Eskimoboy.tscn", "card_path": "res://assets/characters/Eskimoboy/eskimoboyrender.png", "tier": "Legendary"},
    {"id": 157, "name": "Eskimogirl", "path": "res://assets/characters/Eskimogirl/Eskimogirl.tscn", "card_path": "res://assets/characters/Eskimogirl/eskimogirlrender.png", "tier": "Legendary"},
    {"id": 158, "name": "Olaf", "path": "res://assets/characters/Olaf/Olaf.tscn", "card_path": "res://assets/characters/Olaf/olafrender.png", "tier": "Special"},
    {"id": 159, "name": "Sonic", "path": "res://assets/characters/Sonic/Sonic.tscn", "card_path": "res://assets/characters/Sonic/sonicrender.png", "tier": "Special"},
    {"id": 160, "name": "Mrbean", "path": "res://assets/characters/Mrbean/Mrbean.tscn", "card_path": "res://assets/characters/Mrbean/mrbeanrender.png", "tier": "Special"},
    {"id": 161, "name": "Joker", "path": "res://assets/characters/Joker/Joker.tscn", "card_path": "res://assets/characters/Joker/jokertex.png", "tier": "Special"},
    {"id": 162, "name": "Sattarkhan", "path": "res://assets/characters/Sattarkhan/Sattarkan.tscn", "card_path": "res://assets/characters/Sattarkhan/sattarkhanrender.png", "tier": "Special"},
    {"id": 163, "name": "Mohsenlor", "path": "res://assets/characters/Mohsenloretani/MohsenLor.tscn", "card_path": "res://assets/characters/Mohsenloretani/lorestanirender.png", "tier": "Special"},
    {"id": 164, "name": "Habbib", "path": "res://assets/characters/Habbib/Habbib.tscn", "card_path": "res://assets/characters/Habbib/Habbib_card.png", "tier": "Epic"},
    {"id": 165, "name": "Gigachad", "path": "res://assets/characters/Gigachad/Gigachad.tscn", "card_path": "res://assets/characters/Gigachad/gigarender.png", "tier": "Epic"},
    {"id": 166, "name": "Yeti", "path": "res://assets/characters/Yeti/Yeti.tscn", "card_path": "res://assets/characters/Yeti/yetirender.png", "tier": "Special"},
]

TIER_PRICE = {'Common': 1000, 'Rare': 3000, 'Legendary': 8000}
CLAN_LEVELS = [{'level': i, 'max_count': 10 + i * 10, 'price': 1000 * i} for i in range(1, 6)]
SYNC_PRICES = {
    'character_common': 1000, 'character_rare': 3000, 'character_legendary': 8000, 'character_epic': 20000,
    'character_common_exact': 1500, 'character_rare_exact': 4000, 'character_legendary_exact': 10000,
    'character_epic_exact': 25000, 'character_special_exact': 50000,
    'game_tax': 0, 'chat_cup': 0, 'change_name_price': 0, 'animation_price': 500,
    'coin_transfer_fee': 0, 'day_start_hour': 7, 'night_start_hour': 19,
    'reward_video_coins': 50, 'reward_video_hp': 20,
    'force_update_from_url': False, 'update_store_url': '',
    'voice_call_price': 50, 'voice_call_per_minute': 60,
    'force_version': 0, 'last_version': 0,
    'game_is_down': False, 'up_counter': 0,
}

_lock = threading.Lock()
state = {'accounts': {}, 'tokens': {}, 'userCounter': 0, 'servers': {'race': [], 'freeride': []}, 'serverCounter': 0, 'clans': []}

def log(msg):
    try:
        print('[' + time.strftime('%H:%M:%S') + '] ' + str(msg), flush=True)
    except Exception:
        pass

def load_state():
    try:
        with open(STATE_FILE, 'r', encoding='utf-8') as fp:
            state.update(json.load(fp))
    except Exception:
        pass

def save_state():
    try:
        with open(STATE_FILE, 'w', encoding='utf-8') as fp:
            json.dump(state, fp)
    except Exception:
        pass

def _ensure_chat():
    if 'chat' not in state:
        state['chat'] = {'next': 1, 'rooms': {}}


def new_account(username):
    state['userCounter'] += 1
    return {
        'username': username,
        'handle': 'Player' + str(state['userCounter']),
        'coin': 100000,
        'cup': 0, 'crown': 0, 'win_count': 0, 'game_count': 0,
        'hunger': 100, 'warmth': 100,
        'title': '', 'title_color': '',
        'is_test': False, 'name_changed_count': 0, 'show_debug': False,
        'ban_time': 0, 'free_admin': False, 'bazras': False, 'stealth': False, 'chat_admin': False,
        'jail_time': 0, 'in_prison': False,
        'email': '', 'daily_claim_time': 0,
        'progress_level': 1, 'is_meta_progress_finished': True,
        'characters': [dict(c) for c in CHARS],
        'purchases': [], 'animations': {}, 'data': {}, 'clan_id': None,
    }

def account_for(token):
    if not token:
        return None
    if token in state['tokens']:
        return state['accounts'].get(state['tokens'][token])
    state['userCounter'] += 1
    rnd = ''.join(random.choice('abcdefghijklmnopqrstuvwxyz0123456789') for _ in range(5))
    username = 'u' + str(state['userCounter']) + '_' + rnd
    state['accounts'][username] = new_account(username)
    state['tokens'][token] = username
    save_state()
    return state['accounts'][username]

def get_char(cid):
    for c in CHARS:
        if c['id'] == cid:
            return c
    return None

_MEMBER_KEYS = ['cup','coin','crown','email','daily_claim_time','hunger','warmth','title','title_color','is_test','name_changed_count','show_debug','ban_time','free_admin','bazras','stealth','chat_admin','jail_time','in_prison','progress_level','is_meta_progress_finished','win_count','game_count']


PHONES = [
    {'id': 1, 'name': 'Nokia 1201', 'motto': 'Iconic Brick', 'price': 0, 'scene_path': 'res://Scenes/Mobile/Phones/1201/Nokia1201.tscn'},
    {'id': 2, 'name': 'Poco X6', 'motto': 'Power Player', 'price': 5000, 'scene_path': 'res://Scenes/Mobile/Phones/PocoX6/PocoX6.tscn'},
    {'id': 3, 'name': 'iPhone 16 Pro Max', 'motto': 'Pro Style', 'price': 15000, 'scene_path': 'res://Scenes/Mobile/Phones/iPhone/iPhone16ProMax.tscn'},
    {'id': 4, 'name': 'Galaxy S24 Ultra', 'motto': 'Flagship', 'price': 25000, 'scene_path': 'res://Scenes/Mobile/Phones/S24Ultra/S24Ultra.tscn'},
]

PROGRESS = [
    {'level': 1, 'progress_type': 'GameCount', 'game_count': 3, 'cup': 0, 'prize_type': 'Coin', 'prize_coin': 3000, 'prize_character': None},
    {'level': 2, 'progress_type': 'Cup', 'cup': 10, 'game_count': 3, 'prize_type': 'Coin', 'prize_coin': 5000, 'prize_character': None},
    {'level': 3, 'progress_type': 'GameCount', 'game_count': 10, 'cup': 10, 'prize_type': 'Coin', 'prize_coin': 8000, 'prize_character': None},
    {'level': 4, 'progress_type': 'Cup', 'cup': 30, 'game_count': 10, 'prize_type': 'Character', 'prize_coin': 0, 'prize_character': CHARS[5]},
    {'level': 5, 'progress_type': 'WinCount', 'game_count': 5, 'cup': 30, 'prize_type': 'Coin', 'prize_coin': 12000, 'prize_character': None},
    {'level': 6, 'progress_type': 'Cup', 'cup': 60, 'game_count': 5, 'prize_type': 'Character', 'prize_coin': 0, 'prize_character': CHARS[15]},
    {'level': 7, 'progress_type': 'GameCount', 'game_count': 25, 'cup': 60, 'prize_type': 'Coin', 'prize_coin': 20000, 'prize_character': None},
    {'level': 8, 'progress_type': 'Cup', 'cup': 100, 'game_count': 25, 'prize_type': 'Character', 'prize_coin': 0, 'prize_character': CHARS[40]},
]


def _prog_met(a, pr):
    t = pr.get('progress_type')
    if t == 'Cup':
        return a.get('cup', 0) >= pr.get('cup', 0)
    if t == 'GameCount':
        return a.get('game_count', 0) >= pr.get('game_count', 0)
    if t == 'WinCount':
        return a.get('win_count', 0) >= pr.get('game_count', 0)
    return False


def current_progress(a):
    for pr in PROGRESS:
        if not _prog_met(a, pr):
            return pr
    return None


def member_json(a):
    out = {'id': a['username'], 'handle': a['handle']}
    for k in _MEMBER_KEYS:
        out[k] = a.get(k)
    cur = current_progress(a)
    out['progress_level'] = cur if cur is not None else PROGRESS[-1]
    out['is_meta_progress_finished'] = cur is None
    return out



def rank_rows(sort_key):
    rows = []
    for a in state['accounts'].values():
        rows.append({'id': a['username'], 'handle': a['handle'], 'name': a['handle'], 'cup': a['cup'], 'coin': a['coin'], 'crown': a['crown'], 'win_count': a['win_count'], 'value': a.get(sort_key, 0), 'count': a.get(sort_key, 0), 'title': a.get('title', ''), 'rank': 0, 'character': CHARS[0]['path'], 'path': CHARS[0]['path'], 'card_path': CHARS[0]['card_path']})
    rows.sort(key=lambda r: r.get(sort_key, 0), reverse=True)
    rows = rows[:50]
    for i, r in enumerate(rows):
        r['rank'] = i + 1
    return rows


def route(path, body, a):
    now = int(time.time())
    # ---- account ----
    if path == '/account/register/':
        state['userCounter'] += 1
        rnd = ''.join(random.choice('abcdefghijklmnopqrstuvwxyz0123456789') for _ in range(5))
        username = 'u' + str(state['userCounter']) + '_' + rnd
        acct = new_account(username)
        state['accounts'][username] = acct
        tok = 'T' + username + '.' + ''.join(random.choice('abcdefghijklmnopqrstuvwxyz0123456789') for _ in range(10))
        state['tokens'][tok] = username
        save_state()
        log('register -> ' + username)
        return 200, {'handle': acct['handle'], 'token': tok, 'username': username}
    if a is None:
        return 401, {'error': 'unauthorized'}
    if path == '/account/sync/':
        return 200, {'data': {'data': a.get('data', {})}, 'member': member_json(a), 'characters': a['characters'], 'sync': SYNC_PRICES, 'online_count': max(1, len(state['accounts'])), 'public_chat': 'PublicChat', 'progresses': PROGRESS, 'phones': PHONES, 'clan': None, 'clan_levels': CLAN_LEVELS}
    if path == '/account/save_data/':
        jwt = a.get('data', {}).get('JWT') if isinstance(a.get('data'), dict) else None
        a['data'] = body
        if jwt:
            a['data']['JWT'] = jwt
        if body.get('hunger') is not None:
            a['hunger'] = body.get('hunger')
        if body.get('warmth') is not None:
            a['warmth'] = body.get('warmth')
        save_state()
        return 200, {}
    if path == '/account/change_handle/':
        if body.get('handle'):
            a['handle'] = str(body.get('handle'))[:12]
        save_state()
        return 200, {}
    if path == '/account/am_i_ban/':
        return 200, {'member': {'ban_time': a['ban_time'], 'coin': a['coin'], 'title': a['title'], 'title_color': a['title_color'], 'jail_time': a['jail_time'], 'in_prison': a['in_prison']}}
    if path in ('/account/tutorial_started/', '/account/tutorial_finished/', '/account/nakama_connect/', '/account/server_test_fail/', '/game/request_error/', '/account/update_presence/'):
        return 200, {}
    if path == '/account/request_code/':
        a['email'] = body.get('email') or a['email']
        save_state()
        return 200, {}
    if path == '/account/verify_code/':
        a['email'] = body.get('email') or a['email']
        save_state()
        return 200, {'ok': True}
    if path == '/account/remove_email/':
        a['email'] = ''
        save_state()
        return 200, {}
    if path == '/account/claim_progress_prize/':
        cur = current_progress(a)
        lvl = int(body.get('level') or (cur['level'] if cur else 0))
        target = None
        for pr in PROGRESS:
            if pr['level'] == lvl:
                target = pr
                break
        claimed = a.setdefault('progress_claimed', [])
        if target is None or lvl in claimed or not _prog_met(a, target):
            return 200, {'coin': a['coin'], 'ok': False}
        claimed.append(lvl)
        if target.get('prize_type') == 'Coin':
            a['coin'] += int(target.get('prize_coin') or 0)
        elif target.get('prize_type') == 'Character' and target.get('prize_character'):
            a['characters'].append(dict(target['prize_character']))
        save_state()
        return 200, {'coin': a['coin'], 'ok': True}
    if path == '/account/ami_content_creator/':
        return 200, {'is_creator': False}
    if path == '/account/content_creator_stats/':
        return 200, {'stats': {}, 'refers': []}
    if path == '/account/coin_creator_cashout/':
        return 400, {}
    if path == '/account/refer_content_creator/':
        return 200, {}
    # ---- shop ----
    if path == '/shop/list_shop/':
        return 200, {'gateway_type': 'IAP', 'items': [], 'phones': PHONES}
    if path == '/shop/verify_purchase/':
        return 200, {'coin': a['coin'], 'characters': [], 'id': 0}
    if path == '/shop/ipg/':
        return 400, {}
    if path == '/shop/list_gifts/':
        return 200, {'gifts': []}
    if path == '/shop/seen_gifts/':
        return 200, {}
    if path == '/shop/daily_reward/':
        if a['daily_claim_time'] and now - a['daily_claim_time'] < 24 * 3600:
            return 200, {'prize': 0, 'coins': a['coin']}
        prize = random.choice([50, 60, 70, 80, 90, 95, 100, 200])
        a['coin'] += prize
        a['daily_claim_time'] = now
        save_state()
        return 200, {'prize': prize, 'coins': a['coin']}
    if path == '/shop/unlock_new_character_v2/':
        tier = body.get('tier') or 'Common'
        price = TIER_PRICE.get(tier, 1000)
        if a['coin'] < price:
            return 400, {}
        pool = [c for c in CHARS if c['tier'] == tier] or [CHARS[0]]
        c = random.choice(pool)
        a['coin'] -= price
        a['characters'].append(dict(c))
        save_state()
        return 200, {'coin': a['coin'], 'character': dict(c)}
    if path == '/shop/unlock_exact_character/':
        c = get_char(int(body.get('character_id') or 0))
        if not c:
            return 400, {}
        if any(x['id'] == c['id'] for x in a['characters']):
            return 401, {}
        price = TIER_PRICE.get(c['tier'], 1000)
        if a['coin'] < price:
            return 400, {}
        a['coin'] -= price
        a['characters'].append(dict(c))
        save_state()
        return 200, {'coin': a['coin'], 'character': dict(c)}
    if path == '/shop/unlock_animation/':
        return 200, {'character_id': body.get('character_id'), 'coin': a['coin'], 'unlocks': []}
    if path == '/game/purchase_with_coin/':
        price = int(body.get('price') or 0)
        if a['coin'] < price:
            return 400, {'coin': a['coin']}
        a['coin'] -= price
        save_state()
        return 200, {'coin': a['coin']}
    if path == '/game/add_coin/':
        a['coin'] += int(body.get('value') or 0)
        save_state()
        return 200, {'coin': a['coin']}
    if path == '/police/jail_reduce/':
        red = int(body.get('reduce') or 0)
        price = int(body.get('price') or 0)
        if price and a['coin'] < price:
            return 400, {'coin': a['coin']}
        a['coin'] -= price
        a['jail_time'] = max(0, int(a.get('jail_time') or 0) - red)
        if a['jail_time'] <= 0:
            a['in_prison'] = False
        save_state()
        return 200, {'coin': a['coin'], 'jail_time': a['jail_time']}
    if path in ('/game/job_done/', '/game/contact_us/', '/game/finish_game/', '/game/change_server_password/'):
        return 200, {}
    if path == '/game/redeem/':
        return 400, {}
    if path == '/game/my_job_stats/':
        return 200, {'coin': a['coin'], 'stats': {}}
    if path == '/game/hire_me/':
        return 200, {'coin': a['coin'], 'ok': True}
    if path == '/game/transfer_money/':
        amount = int(body.get('amount') or body.get('coin') or 0)
        if a['coin'] < amount:
            return 400, {'coin': a['coin']}
        a['coin'] -= amount
        save_state()
        return 200, {'coin': a['coin']}
    if path == '/game/fetch_member_by_username/':
        return 200, {'member': None}
    if path == '/game/list_transactions/':
        return 200, {'transactions': []}
    # ---- matchmaking / servers ----
    if path == '/game/register/':
        mode = body.get('mode') or 'Race'
        ip = body.get('ip') or '127.0.0.1'
        port = int(body.get('port') or 9000)
        key = 'freeride' if mode == 'FreeRide' else 'race'
        lst = state['servers'][key]
        for x in lst:
            if x['ip'] == ip and x['port'] == port:
                return 200, {'id': x['id'], 'is_test': False, 'total_stage': x['total_stage']}
        state['serverCounter'] += 1
        sid = state['serverCounter']
        entry = {'id': sid, 'mode': mode, 'ip': ip, 'port': port, 'players_joined': 0, 'state': 'Lobby', 'map_id': 0, 'bot_count': 0, 'max_players_start': 32, 'total_stage': 3, 'has_password': False, 'password': '', 'name': ('FreeRide ' if mode == 'FreeRide' else 'Race ') + 'Server ' + str(sid)}
        lst.append(entry)
        save_state()
        log('server registered id=' + str(sid) + ' mode=' + mode + ' ' + ip + ':' + str(port))
        return 200, {'id': sid, 'is_test': False, 'total_stage': entry['total_stage']}
    if path == '/game/update/':
        for s in state['servers']['race'] + state['servers']['freeride']:
            if s['id'] == int(body.get('id') or 0):
                s['players_joined'] = int(body.get('players_joined') or 0)
                s['state'] = body.get('state') or s['state']
                s['map_id'] = body.get('map_id') or 0
                s['bot_count'] = int(body.get('bot_count') or 0)
                save_state()
        return 200, {}
    if path == '/game/start_game/':
        count = int(body.get('player_count') or 1)
        return 200, {'game_id': random.randint(0, 999999999), 'container_id': 1, 'qualified_count': max(1, count // 2)}
    if path == '/game/find_game_v2/':
        alive = [s for s in state['servers']['race'] if s['players_joined'] < s['max_players_start']]
        if not alive:
            return 400, {}
        best = alive[0]
        return 200, {'best_server': {'ip': best['ip'], 'port': best['port'], 'total_stage': best['total_stage']}, 'all_servers': [{'ip': s['ip'], 'port': s['port'], 'total_stage': s['total_stage']} for s in alive[1:]]}
    if path == '/game/select_map/':
        # سرور تعیین می‌کند هر مرحله کدام نقشه باشد
        gid = int(body.get('id') or 0)
        games = state.setdefault('games', {})
        g = games.setdefault('g' + str(gid), {'stage': 0})
        g['stage'] = int(g.get('stage', 0)) + 1
        maps = [
            ('res://Scenes/maps/CannonLevel.tscn', 10),
            ('res://Scenes/maps/RunningLevel.tscn', 10),
            ('res://Scenes/maps/Hexagon_elimination_level.tscn', 10),
        ]
        idx = min(g['stage'], len(maps)) - 1
        mpath, bots = maps[idx]
        save_state()
        log('select_map game=' + str(gid) + ' stage=' + str(g['stage']) + ' -> ' + mpath)
        return 200, {'map': {'id': g['stage'], 'path': mpath, 'max_players_count': 32, 'min_players_count': 1, 'bot_count': bots, 'bot_wait_remove': 100, 'bot_reset_time': 30}, 'settings': {'game_time': 120, 'lobby_time': 60, 'countdown_time': 10, 'result_time': 10, 'player_join_add_time': 5}}
    if path == '/game/results_v2/':
        return 200, {'my_result': {'coin': 50, 'cup': 10, 'crown': 0}, 'winner': None}
    if path == '/game/list_freeride_servers/':
        return 200, {'servers': state['servers']['freeride']}
    if path == '/game/get_freeride_server_owner/':
        return 200, {'owner': None, 'owner_handle': ''}
    if path == '/game/leaderboard_v2/':
        rows = rank_rows('cup')
        wins = rank_rows('win_count')
        return 200, {'ranks': rows, 'wins': wins, 'my_rank': next((r['rank'] for r in rows if r.get('id') == a.get('username')), 0), 'my_win_rank': next((r['rank'] for r in wins if r.get('id') == a.get('username')), 0)}
    if path == '/game/coin_leaderboard/':
        rows = rank_rows('coin')
        return 200, {'ranks': rows, 'my_rank': next((r['rank'] for r in rows if r.get('id') == a.get('username')), 0)}
    if path == '/game/char_leaderboard/':
        rows = rank_rows('cup')
        return 200, {'ranks': rows, 'my_rank': next((r['rank'] for r in rows if r.get('id') == a.get('username')), 0)}
    # ---- chat ----
    if path == '/chat/send/':
        _ensure_chat()
        room = str(body.get('room') or 'PublicChat')[:64]
        content = body.get('content')
        if not isinstance(content, str):
            content = json.dumps(content or {})
        mid = state['chat']['next']
        state['chat']['next'] = mid + 1
        msg = {
            'id': mid,
            'content': content[:4000],
            'channel_id': room,
            'sender_id': a['username'],
            'handle': a['handle'],
            'create_time': time.strftime('%Y-%m-%dT%H:%M:%S', time.gmtime()),
        }
        room_msgs = state['chat']['rooms'].setdefault(room, [])
        room_msgs.append(msg)
        if len(room_msgs) > 200:
            del room_msgs[0:len(room_msgs) - 200]
        save_state()
        return 200, {'ok': True, 'id': mid}
    if path == '/chat/fetch/':
        _ensure_chat()
        room = str(body.get('room') or 'PublicChat')[:64]
        since = int(body.get('since') or 0)
        room_msgs = state['chat']['rooms'].get(room, [])
        out = [m for m in room_msgs if int(m.get('id', 0)) > since]
        return 200, {'messages': out[-100:]}
    if path == '/chat/history/':
        _ensure_chat()
        room = str(body.get('room') or 'PublicChat')[:64]
        limit = int(body.get('limit') or 50)
        room_msgs = state['chat']['rooms'].get(room, [])
        out = list(room_msgs)[-limit:]
        out.reverse()
        return 200, {'messages': out}
    # ---- police ----
    if path == '/police/arrest_list/':
        return 200, {'arrests': [], 'results': []}
    if path == '/police/jail_stat/':
        return 200, {'jail_time': int(a.get('jail_time') or 0), 'stats': {}, 'players': []}
    if path == '/police/police_call/':
        return 200, {'calls': []}
    if path == '/police/police_call_list/':
        return 200, {'calls': []}
    if path == '/police/police_law/':
        return 200, {'law': 'قوانین شهر:\n۱) آسیب به دیگران ممنوع است.\n۲) دزدی و تخریب اموال عمومی جرم است.\n۳) توهین و فحاشی در چت ممنوع است.\n۴) رانندگی پرخطر و تصادف عمدی جرم است.\n۵) در صورت دستگیری، جریمه یا زندان در انتظار شماست.', 'last_update': time.strftime('%Y-%m-%dT%H:%M:%S', time.gmtime())}
    if path == '/police/job_q_stats/':
        return 200, {'players': []}
    if path.startswith('/police/'):
        return 200, {}
    if path in ('/game/ban_user/', '/game/report_message/', '/game/free_admin_ban/', '/game/free_admin_unban/', '/game/free_admin_set_title/'):
        return 200, {}
    log('unhandled route: ' + str(path))
    return 200, {}

class Handler(BaseHTTPRequestHandler):
    protocol_version = 'HTTP/1.1'

    def _send(self, code, obj):
        body = json.dumps(obj if obj is not None else {}).encode('utf-8')
        self.send_response(code)
        self.send_header('Content-Type', 'application/json')
        self.send_header('Content-Length', str(len(body)))
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Headers', '*')
        self.send_header('Access-Control-Allow-Methods', 'POST, GET, OPTIONS')
        self.end_headers()
        self.wfile.write(body)

    def do_OPTIONS(self):
        self.send_response(204)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Headers', '*')
        self.send_header('Access-Control-Allow-Methods', 'POST, GET, OPTIONS')
        self.end_headers()

    def do_GET(self):
        p = self.path.split('?')[0]
        if p in ('/', '/health', '/healthz'):
            self._send(200, {'ok': True, 'service': 'animal-rush-backend', 'accounts': len(state['accounts']), 'time': int(time.time())})
        else:
            self._send(404, {'error': 'not found'})

    def do_POST(self):
        length = int(self.headers.get('Content-Length') or 0)
        raw = self.rfile.read(length) if length else b''
        try:
            body = json.loads(raw.decode('utf-8') or '{}')
        except Exception:
            body = {}
        if not isinstance(body, dict):
            body = {}
        auth = self.headers.get('Authorization') or ''
        token = auth[4:] if auth.startswith('JWT ') else auth
        path = self.path.split('?')[0]
        with _lock:
            a = account_for(token)
            try:
                code, obj = route(path, body, a)
            except Exception as exc:
                log('route error ' + str(path) + ': ' + repr(exc))
                code, obj = 500, {'error': 'internal'}
            save_state()
        self._send(code, obj)

    def log_message(self, fmt, *args):
        pass

def main():
    load_state()
    log('Animal Rush backend (Railway) listening on ' + HOST + ':' + str(PORT))
    srv = ThreadingHTTPServer((HOST, PORT), Handler)
    try:
        srv.serve_forever()
    except KeyboardInterrupt:
        pass

if __name__ == '__main__':
    main()
