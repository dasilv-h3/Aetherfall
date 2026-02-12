from Character import *
from EnemyFactory import *

def main():
    print("1 - Nouvelle partie")
    print("2 - Charger partie")
    print("3 - Quitter")

    choice = input("Votre choix : " )

    if choice == "1":
        player = Warrior("charlie")
        # print("Player : ", player)
        enemy = Wolf(10)
        # print("Ennemy : ", player)
        player.attack(enemy)
        enemy.attack(player)
        # print("Warrior Skill : ", player.skill1())
        print(vars(player))
        return 0
    elif choice == "2":
        return 0
    elif choice == "3":
        return 0
    return 0

if __name__ == "__main__":
    main()