# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


# This is a simple example for a custom action which utters "Hello World!"

from typing import Any, Text, Dict, List
import rasa_sdk # type: ignore
import random
import pandas as pd # type: ignore
from rasa_sdk import Action, Tracker  # type: ignore
from rasa_sdk.events import SlotSet # type: ignore
from rasa_sdk.executor import CollectingDispatcher # type: ignore
import logging
import os

#
#
# logger = logging.getLogger(__name__)
# logger.setLevel(logging.DEBUG)


# log_file_path = os.path.join('/Users/payodhi/aiproject/skinrecommendationchatbot/conversationLogs.log')
# file_handler = logging.FileHandler(log_file_path)
# file_handler.setLevel(logger.DEBUG)

# formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
# file_handler.setFormatter(formatter)


# logger.addHandler(file_handler)

class ActionRecommendProduct(Action):
#
    def name(self) -> str:
        return "action_recommend_products"
    
    def __init__(self):
        self.products = pd.read_csv("/Users/payodhi/aiproject/skinrecommendationchatbot/cosmetics.csv")
#
    def run(self, dispatcher, tracker, domain):
        
        #Get the user's request
        #logger.dubug("Action Recommend Product Triggered")
        
        user_request = tracker.latest_message.get('text')
        #Extract product category from the user requrest
        category = tracker.get_slot("category")
        print(f"Category slot value: {category}")
        if not category:
            category = self.extract_category(user_request)

        if category:
            dispatcher.utter_message(f"Looking for {category} products")
            recommended_products = self.get_recommended_products(category)
            if recommended_products:
                response = f"List of recommended {category} products"
                for product in recommended_products:
                    response += f"- {product['Label']} | ${product['Brand']} | Rating: {product['Rank']}\n"
                dispatcher.utter_message(response)
                return [SlotSet("category", category)]
            else:
                dispatcher.utter_message(f"Sorry, I couldn't find {category} that matches your preference")
                return [SlotSet("category", None)]
        else:
            dispatcher.utter_message("Could you specify product category")
            return [SlotSet("category", None)]

    def extract_category(self, user_input):
        #category matching 
        categories = ['moisturizer', 'cleanser', 'face mask', 'sunscreen', 'treatment']

        for category in categories:
            if category in user_input.lower():
                return category
        return None
    
    def get_recommended_products(self, category):
        category_map = {"moisturizer":["lotion", "cream", "moisturizer", "face cream"], "sun protect":["sunscreen", "sun protect", "sunprotect", "sun screen", "spf", "sun block"]}
        for key, value in category_map.items():
            if category in value:
                recommended_product = self.products[(self.products["Label"].str.lower() == key.lower()) & (self.products['Rank'] > 4.5)]
                return recommended_product.to_dict(orient='records')
    
    # def get_recommended_products(self, category):
    #     #filter products based on category
    #     recommended_product = self.products[(self.products['Label'].str.lower() == category.lower()) & (self.products['Rank'] > 4.5)]
    #     return recommended_product.to_dict(orient='records')

class ActionFilterProduct(Action):
    def name(self) -> str:
        return "action_filter_products"

    def run(self, dispatcher, tracker, domain):
        product = next(tracker.get_latest_entity_values("product"), None)
        
        filtered_product = [product for product in ["moisturizer A", "moisturizer B", "Cleanser A"]
                            if (product == product)]
        
        if filtered_product:
            dispatcher.utter_message(f"Here is the product I found {', '.join(filtered_product)}")
        else:
            dispatcher.utter_message(f"Sorry, couldn't find what you are looking for")

        return []
             

