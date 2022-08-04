# UGS Remote Config access through API
# -*- coding: utf-8 -*-
# /usr/bin/python3

"""
Created on Thu 4 Aug 2022
@Author: Laurie McCulloch
"""

import os.path
import requests
import json

projectId = 'bdddc820-fcbb-4c23-8d24-1135bdf9606b'  # Flower Defence


def main():
    clearConsole()
    print("-= UGS Remote Config API Shenanigans =-\n")
    t, u = authenticate()
    menu(t, u)


def menu(t, u):
    print("\nP - GetPlayerSettings \nQ - Quit")
    i = input("\nChoose an option > ").lower()
    if i == "p":  # getPlayerSettings
        getPlayerSettings(t, u)
        menu(t, u)
    elif i == "q":  # quit
        print("Bye Bye")
        return
    else:
        menu(t, u)


def clearConsole():
    if os.name == 'nt':
        os.system('cls')
    else:
        os.system('clear')


def authenticate():
    print("Authenticating...")

    url = ('https://player-auth.services.api.unity.com'
           '/v1/authentication/anonymous')
    print(url)
    headers = ({"Content-length": "0",
                "projectId": projectId,
                "UnityEnvironment": "production"})

    response = requests.post(url=url, headers=headers)
    print(response.status_code)

    if response.status_code == 200:
        userId = json.loads(response.text)["userId"]
        idToken = json.loads(response.text)["idToken"]
        print("PlayerId ", userId)
        return idToken, userId
    else:
        print("Error Authenticating")
        return


def getPlayerSettings(idToken, playerId):
    print('Remote Config - GetPlayerSettings')

    url = ('https://config.unity3d.com/api/v1/settings?projectId='
           '{0}&userId={1}'.format(projectId, playerId))
    h = {"Content-type": "application/json"}
    h.update({"Authorization": "Bearer {0}".format(idToken)})

    response = requests.get(url=url, headers=h)

    print(url)
    print(response.status_code)
    parsed = json.loads(response.text)

    print(json.dumps(parsed, indent=4))


# standard boilerplate
# main is the starting function
if __name__ == '__main__':
    main()
    print("\n")
