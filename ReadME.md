# ChatBot project

## Authors
---
The team project was composed of : 
* BOUCHER Lucie (66862)
* BOURDAIS Rémi (66869)
* MONTIGNIER Lola (66860)

## Introduction
---
In the context of the Web data mining course, we had to implement a personal shopper in a chatbot for the website Farfetch.

## Description of our ChatBot
---

### How to run the code

To run the code you will have to install the followings : 
* [Install Python3](https://www.python.org/downloads/) (all the dependencies can be found in the file requirements.txt)

* [Install Flask](https://flask.palletsprojects.com/en/2.1.x/installation/)

* [Install PyTorch](https://pytorch.org/TensorRT/tutorials/installation.html)

Once those installations done, you will have to open a terminal and simply do the command python3 app.py once you are in the folder named Back-end

### Functionnalities Implemented
Once the code is working, you have to open, on a web window, [Farfetch website ](https://www.farfetch.com/pt/shopping/women/items.aspx) and the chatbot will open automatically. 
The list of the functionnalities that the user can access : 
1. Define a profile with his favorite items
2. Ask the chatbot about items in different ways:
    * Text Research
    * Image Research
    * Multimodal Research 
3. Ask the chatbot some recommendations, that will be based on the previous results and the profile (if one define)
4. Ask the chatbot more informations about the items displayed :
    * Materials
    * Colors
    * Category
5. Possibility to like or dislike products by clicking on the heart on the top of the products displayed
6. Possibility to visualize all the items liked by clicking on the profile icon


### How to use our chatbot

The use of our chatbot is quiet simple, you can discuss with it to find items of your choice. However, Opensearch limits the use of our chatbot, some advices to have the best use of our chatbot :
* To search a dress, ask for 'dresses'
* To have more informations about the previous items, ask 'more infos' or 'more informations'
* To ask for recommendations, ask for 'show me some products'

The chatbot will great you at the beginning and if you say goodbye or something similar you will exit the chatbot and you will not be able to do more requests, to solve that you will have to refresh the website.
