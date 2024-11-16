# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


# This is a simple example for a custom action which utters "Hello World!"

# from typing import Any, Text, Dict, List
# import rasa_sdk # type: ignore
# import random
# import pandas as pd # type: ignore
# from rasa_sdk import Action, Tracker  # type: ignore
# from rasa_sdk.events import SlotSet # type: ignore
# from rasa_sdk.executor import CollectingDispatcher # type: ignore
# from rasa_sdk.forms import FormAction # type: ignore
# import logging
# import os

import csv
import os
import pandas as pd
from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import SlotSet
from sklearn.preprocessing import LabelEncoder
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

class ActionSaveUserInfo(Action):
    def name(self) -> Text:
        return "action_save_customer_information"

    # def run(self, dispatcher, tracker,domain):
        
    #     cust_name = tracker.get_slot('name')
    #     cust_age = tracker.get_slot('age')
    #     cust_skin_type = tracker.get_slot('skin_type')
    #     cust_allergies= tracker.get_slot('allergies')

    #     #headerList = ['Name', 'Age', 'Skin Type', 'Allergy'] 

    #     # Save to CSV
    #     with open('user_info.csv', mode='w', newline='') as file:
            
    #         writer = csv.writer(file)
    #         writer.writerow(['Name', 'Age', 'Skin Type', 'Allergy'] )
    #         writer.writerows([cust_name, cust_age, cust_skin_type, cust_allergies])

    #     dispatcher.utter_message(text="Thank you! Your information has been saved.")

    #     return []
    def run(self, dispatcher, tracker, domain):
        
        cust_name = tracker.get_slot('name')
        cust_age = tracker.get_slot('age')
        cust_skin_type = tracker.get_slot('skin_type')
        cust_allergies = tracker.get_slot('allergies')
        cust_price_range = tracker.get_slot('price_range')

        file_path = r"dataset/customer_information.csv"
        
        # Check if the file exists and is non-empty
        file_exists = os.path.isfile(file_path) and os.path.getsize(file_path) > 0

        # Open the file in append mode
        with open(file_path, mode='a', newline='') as cust_file:
            writer = csv.writer(cust_file)
            
            # Write the header only if the file doesn't already contain data
            if not file_exists:
                writer.writerow(['Name', 'Age', 'Skin Type', 'Allergy', 'Price Range'])
            
            # Write the user's data
            writer.writerow([cust_name, cust_age, cust_skin_type, cust_allergies, cust_price_range])

        dispatcher.utter_message(text="Thank you! Your information has been saved.")
        
        return []

class ActionRecommendation(Action):
    def name(self) -> str:
        return "action_get_product_recommendation"

    def __init__(self):
        self.product_details = pd.read_csv(r"dataset/product_details.csv")
        self.customer_details = pd.read_csv(r"dataset/customer_information.csv")
    
    def run(self, dispatcher, tracker, domain) -> list:

        #Extracting customer name and product category from the user request
        customer_name = tracker.get_slot("name")

        self.product_details['Brand'] = self.product_details['Brand'].str.strip()  # Remove leading/trailing spaces
        self.product_details['Skin Type'] = self.product_details['Skin Type'].str.strip().str.lower()  # Convert skin types to lowercase

        # Ensure there are no NaN values in 'Labels' and split by commas if labels are stored as a string
        self.product_details['Labels'] = self.product_details['Label'].fillna('')

        # Step 2: Extract distinct labels from the 'Labels' column
        distinct_labels = self.product_details['Labels'].unique()

        # Encode categorical columns like Skin Type using LabelEncoder
        skin_type_encoder = LabelEncoder()

        # Ensure all skin types are consistently encoded
        self.product_details['Skin type_encoded'] = skin_type_encoder.fit_transform(self.product_details['Skin Type'])  

        # Step 3: TF-IDF Vectorizer for Ingredients
        tfidf_vectorizer = TfidfVectorizer(stop_words='english')
        self.product_details['Ingredients'] = self.product_details['Ingredients'].fillna('')

        # Transform the ingredients column into a TF-IDF matrix
        ingredients_matrix = tfidf_vectorizer.fit_transform(self.product_details['Ingredients'])

        # Step 4: Calculate Cosine Similarity between products
        cosine_sim = cosine_similarity(ingredients_matrix, ingredients_matrix)

        #print(f"{cust_age, cust_skinType, cust_allergies, type(cust_price_range)}")
        for _, customer in self.customer_details.iterrows():

            #Encoding the customer skin type
            if isinstance(customer['Skin Type'], str):  # Ensure it's a string
                cust_skinType = skin_type_encoder.transform([customer['Skin Type'].lower()])[0]
            else:
                cust_skinType = -1  # Assign a default value if the skin type is missing or invalid

            
            cust_name = customer['Name']
            cust_price_range = customer['Price Range']
            recommended_product = self.get_product_recommendation_based_on_user_preference(cust_skinType, cust_price_range, distinct_labels, cosine_sim)

            response = f"Recommendations for {cust_name} with skin type {customer['Skin Type']} and budget {cust_price_range}:\n"
            #if system is able to fetch the product based on user preference then this flow
            if recommended_product:
                for label, products in recommended_product.items():
                    response += f"Recommendation for {label}:\n"
                    for product in products:
                        response += f"- \nProduct: {product[0]}, Price: {product[2]}, Rank: {product[3]}\n"

                
                dispatcher.utter_message(response)
                return [SlotSet("name", customer_name)]
                # return [SlotSet("category", product_category), SlotSet("name", customer_name)]
            else:
                dispatcher.utter_message(f"Sorry, Couldn't find any product based on your preference\n")
                return []
                # return [SlotSet("category", None), SlotSet("name", customer_name)]
    
    def get_product_recommendation_based_on_user_preference(self, cust_skinType, cust_price_range, labels, cosine_sim, top_n=2):
        

        recommendations_by_label = {}
        #processing the price_range
        if cust_price_range.startswith('$'):
            cust_price_range = float(cust_price_range[1:])
        else:
            cust_price_range = float(cust_price_range)

        for label in labels:
            # Filter products by skin type, price, and label
            filtered_df = self.product_details[(self.product_details['Skin type_encoded'] == cust_skinType) & 
                         (self.product_details['Price'] <= cust_price_range) & 
                         (self.product_details['Labels'].str.contains(label, case=False))]
        
            if not filtered_df.empty:
                product_indices = filtered_df.index.tolist()
                cosine_scores = cosine_sim[product_indices]

                # Step 5.2: Get top N recommended products per label
                recommendations = []
                for i, index in enumerate(product_indices):
                    sim_scores = cosine_scores[i]
                    similar_indices = sim_scores.argsort()[-top_n-1:][::-1]  # Exclude self
                    for similar_index in similar_indices:
                        recommendations.append((self.product_details.iloc[similar_index]['Name'], sim_scores[similar_index], self.product_details.iloc[similar_index]['Price'], self.product_details.iloc[similar_index]['Rank']))

                # Sort and store the recommendations for the label
                recommendations = sorted(recommendations, key=lambda x: x[1], reverse=True)
                recommendations_by_label[label] = recommendations[:top_n]
    
        return recommendations_by_label



    # def get_product_recommendation_based_on_user_preference(self, customer_name):
    #     #Extract customer details based on the customer name from customer details database
    #     #customer = self.customer_details[self.customer_details['Name'].lower().strip() == cust_name.lower().strip()].iloc[0]
    #     customer = self.customer_details[self.customer_details['Name'] == customer_name].iloc[0]
    #     cust_age = customer['Age']
    #     cust_skinType = customer['Skin_type']
    #     cust_allergies = customer['Allergies']
    #     cust_price_range = customer['Price Range']

    #     #iterating over product database to get required product based on skin type and allergies
    #     product_to_recommend = []
    #     for idx, product in self.product_details.iterrows():
    #         if (cust_skinType in product[cust_skinType].lower().strip() and cust_allergies not in product['Ingredients'].lower().strip()):
    #             product_to_recommend.append(product)
            
    #     product_to_recommend = pd.DataFrame(product_to_recommend)
    #     return product_to_recommend

# class ActionProceedToStory(Action):
#     def name(self) -> str:
#         return "action_proceed_to_story"

#     def run(self, dispatcher, tracker, domain):
#         # Any custom logic can go here
#         dispatcher.utter_message(text="Proceeding with the recommendation process.")
#         # Set a slot to indicate transition to story
#         return [SlotSet("transition_to_story", True)]


























#***********************************************

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

#Writing code to update the recommendations technique, by considering the user input (skin type, allergies, product category etc)
# class ActionRecommendProduct(Action):
#     def name(self) -> str:
#         return "action_recommend_products"

#     def __init__(self):
#         self.product_details = pd.read_csv(r"/Users/payodhi/aiproject/skinrecommendationchatbot/dataset/product_database.csv")
#         self.customer_details = pd.read_csv(r"/Users/payodhi/aiproject/skinrecommendationchatbot/dataset/CustomerDetails.csv")
#         print(f"{self.customer_details}")

#     def run(self, dispatcher, tracker, domain) -> list:
#         #Extracting customer name and product category from the user request
#         customer_name = tracker.get_slot("name")
#         product_category = tracker.get_slot("category")

        

#         #Printing the product category extracted from user request -> For debugging purpose; can be removed later if not required
#         print(f"Product Category given was: {product_category}")

#         #if no category is extracted from the slot, using the user's latest message to extract product category
#         if not product_category:
#             product_category = self.extract_product_category(tracker.latest_message.get('text'))


#         if product_category:
#             dispatcher.utter_message(f"Looking for products to recommend for {product_category}")
#             #Invoking the recommendation function to get products
#             recommended_product = self.get_product_recommendation_based_on_user_preference(customer_name, product_category)
#             #if system is able to fetch the product based on user preference then this flow
#             if recommended_product:
#                 response = f"Here is a List of {product_category} based on your preference\n"
#                 #Displaying the recommendations by appending it to the response

#                 recommended_product  = recommended_product.to_string(index=False)
#                 response += recommended_product 
#                 # for product in recommended_product:
#                 #     response += f"- {product['Label']} | {product['Brand']} : {product['Name']} | Rating: {product['Rank']}\n" 
                
#                 dispatcher.utter_message(response)
#                 return [SlotSet("category", product_category), SlotSet("name", customer_name)]
#             else:
#                 dispatcher.utter_message(f"Sorry, Couldn't find {product_category} based on your preference\n")
#                 return [SlotSet("category", None), SlotSet("name", customer_name)]
        
#         else:
#             dispatcher.utter_message("Please specify any product category (moisturizer, cleanser, sunscreen, face mask, eye cream)")
#             return [SlotSet("category", None)]


#     def extract_category(self, user_input):
#         #category matching 
#         #changed category matching logic from list to dictionary to handle synonyms of product category
#         #categories = ['moisturizer', 'cleanser', 'face mask', 'sun protect', 'treatment', 'eye cream']
#         category_map = {"moisturizer":["lotion", "cream", "moisturizer", "face cream"], "sun protect":["sunscreen", "sun protect", "sunprotect", "sun screen", "spf", "sun block"]}
#         for key, value in category_map.items():
#             if value in user_input.lower():
#                 return key
#         return None

#     def get_product_recommendation_based_on_user_preference(self, cust_name, required_product):
#         # handling the synonyms of product category
#         category_map = {"moisturizer":["lotion", "cream", "moisturizer", "face cream"], "sun protect":["sunscreen", "sun protect", "sunprotect", "sun screen", "spf", "sun block"]}
#         for key, value in category_map.items():
#              if required_product in value:
#                  required_product = key
        
#         #Handle cases where Skin type or Allegies are unknown

#         #Extract customer details based on the customer name from customer details database
#         #customer = self.customer_details[self.customer_details['Name'].lower().strip() == cust_name.lower().strip()].iloc[0]
#         customer = self.customer_details[self.customer_details['Name'] == cust_name].iloc[0]
#         cust_age = customer['Age']
#         cust_skinType = customer['Skin_type']
#         cust_allergies = customer['Allergies']

#         #iterating over product database to get required product based on skin type and allergies
#         product_to_recommend = []
#         for idx, product in self.product_details.iterrows():
#             if (product.iloc[0].lower().strip() == required_product.lower().strip()) and product[cust_skinType]==1 and cust_allergies not in product['Ingredients'] and product['Rank'] >4.8:
#                 product_to_recommend.append(product)
            
#         product_to_recommend = pd.DataFrame(product_to_recommend)
#         return product_to_recommend


# #Working version of the product recommendation code -> recommends product based on user specified category with rating more than 4.5
# # class ActionRecommendProduct(Action):
# # #
# #     def name(self) -> str:
# #         return "action_recommend_products"
    
# #     def __init__(self):
# #         self.products = pd.read_csv("/Users/payodhi/aiproject/skinrecommendationchatbot/cosmetics.csv")
# # #
# #     def run(self, dispatcher, tracker, domain):
        
# #         #Get the user's request
# #         #logger.dubug("Action Recommend Product Triggered")
        
# #         user_request = tracker.latest_message.get('text')
# #         #Extract product category from the user requrest
# #         category = tracker.get_slot("category")
# #         print(f"Category slot value: {category}")
# #         if not category:
# #             category = self.extract_category(user_request)

# #         if category:
# #             dispatcher.utter_message(f"Looking for {category} products")
# #             recommended_products = self.get_recommended_products(category)
# #             if recommended_products:
# #                 response = f"List of recommended {category} products"
# #                 for product in recommended_products:
# #                     response += f"- {product['Label']} | ${product['Brand']} | Rating: {product['Rank']}\n"
# #                 dispatcher.utter_message(response)
# #                 return [SlotSet("category", category)]
# #             else:
# #                 dispatcher.utter_message(f"Sorry, I couldn't find {category} that matches your preference")
# #                 return [SlotSet("category", None)]
# #         else:
# #             dispatcher.utter_message("Could you specify product category")
# #             return [SlotSet("category", None)]

# #     def extract_category(self, user_input):
# #         #category matching 
# #         categories = ['moisturizer', 'cleanser', 'face mask', 'sunscreen', 'treatment']

# #         for category in categories:
# #             if category in user_input.lower():
# #                 return category
# #         return None
    
# #     def get_recommended_products(self, category):
# #         category_map = {"moisturizer":["lotion", "cream", "moisturizer", "face cream"], "sun protect":["sunscreen", "sun protect", "sunprotect", "sun screen", "spf", "sun block"]}
# #         for key, value in category_map.items():
# #             if category in value:
# #                 recommended_product = self.products[(self.products["Label"].str.lower() == key.lower()) & (self.products['Rank'] > 4.5)]
# #                 return recommended_product.to_dict(orient='records')
    
#     # def get_recommended_products(self, category):
#     #     #filter products based on category
#     #     recommended_product = self.products[(self.products['Label'].str.lower() == category.lower()) & (self.products['Rank'] > 4.5)]
#     #     return recommended_product.to_dict(orient='records')

# class ActionFilterProduct(Action):
#     def name(self) -> str:
#         return "action_filter_products"

#     def run(self, dispatcher, tracker, domain):
#         product = next(tracker.get_latest_entity_values("product"), None)
        
#         filtered_product = [product for product in ["moisturizer A", "moisturizer B", "Cleanser A"]
#                             if (product == product)]
        
#         if filtered_product:
#             dispatcher.utter_message(f"Here is the product I found {', '.join(filtered_product)}")
#         else:
#             dispatcher.utter_message(f"Sorry, couldn't find what you are looking for")

#         return []
             

# #Functions to get user information from the chatbot input
# class ActionGetUserDetails(FormAction):
#     def name(self) -> str:
#         #calling the action to execute the code below
#         return "submit_form"

#     def required_slots(tracker):
#         return ["name", "age", "skin_type", "allergies"]
    
#     def slot_mappings(self):
#         return {
#             "name": [self.from_text()], 
#             "age": [self.from_text()],
#             "skin_type": [self.from_text()],
#             "allergies": [self.from_text()]
#         }
    
#     def run(self, dispatcher, tracker, domain):
#         cust_name = tracker.get_slot('name')
#         cust_age = tracker.get_slot('age')
#         cust_skin_type = tracker.get_slot('skin_type')
#         cust_allergies = tracker.get_slot('allergies')


#         # checking if customer details file exists
#         # if yes, loading the data into a dataframe and appending the new information to the csv file
#         # if file doesn't exist, creating a new dataframe and writing to csv file 

#         try:
#             cust_details = pd.read_csv(r'/Users/payodhi/aiproject/skinrecommendationchatbot/dataset/CustomerDetails.csv')
#         except:
#             cust_details = pd.DataFrame(columns=['Name', 'Age', 'Skin_type', 'Allergies'])
        
#         #adding new customer details to the dataframe
#         new_customer = pd.DataFrame([[cust_name, cust_age, cust_skin_type, cust_allergies]], columns=['Name', 'Age', 'Skin_type', 'Allergies'])
#         cust_details = pd.concat([cust_details, new_customer], ignore_index=False)

#         #Saving the user details into a CSV file
#         cust_details.to_csv(r'/Users/payodhi/aiproject/skinrecommendationchatbot/dataset/CustomerDetails.csv', index=False)

#         dispatcher.utter_message(text=f"Your information is saved for making recommendations\n")

#         return []

    
    # def run(self, dispatcher, tracker, domain):
    #     #fetching the information from the user input
    #     cust_name = tracker.get_slot('name')
    #     cust_age = tracker.get_slot('age')
    #     cust_skin_type = tracker.get_slot('skin_type')
    #     cust_allergies = tracker.get_slot('allergies')

    #     #Displaying the collected user details to the user
    #     dispatcher.utter_message(text=f"Your details: name {cust_name}, age {cust_age}, skin_type {cust_skin_type}, allergies {cust_allergies}")

    #     return [
    #         SlotSet("name", cust_name),
    #         SlotSet("age", cust_age),
    #         SlotSet("skin_type", cust_skin_type),
    #         SlotSet("allergies", cust_allergies)
    #     ]
#Function to store user information into a csv file
# class ActionSaveUserToCSV(Action):
#     def name(self) -> str:
#         return "action_save_user_details_to_csv"

#     def run(self, dispatcher, tracker, domain):
#         cust_name = tracker.get_slot('name')
#         cust_age = tracker.get_slot('age')
#         cust_skin_type = tracker.get_slot('skin_type')
#         cust_allergies = tracker.get_slot('allergies')


#         # checking if customer details file exists
#         # if yes, loading the data into a dataframe and appending the new information to the csv file
#         # if file doesn't exist, creating a new dataframe and writing to csv file 

#         try:
#             cust_details = pd.read_csv(r'/Users/payodhi/aiproject/skinrecommendationchatbot/dataset/CustomerDetails.csv')
#         except:
#             cust_details = pd.DataFrame(columns=['Name', 'Age', 'Skin_type', 'Allergies'])
        
#         #adding new customer details to the dataframe
#         new_customer = pd.DataFrame([[cust_name, cust_age, cust_skin_type, cust_allergies]], columns=['Name', 'Age', 'Skin_type', 'Allergies'])
#         cust_details = pd.concat([cust_details, new_customer], ignore_index=False)

#         #Saving the user details into a CSV file
#         cust_details.to_csv(r'/Users/payodhi/aiproject/skinrecommendationchatbot/dataset/CustomerDetails.csv', index=False)

#         dispatcher.utter_message(text=f"Your information is saved for making recommendations\n")

#         return []
