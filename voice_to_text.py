import speech_recognition as sr
import pyttsx3
import pandas as pd
import random
import spacy

nlp = spacy.load("en_core_web_sm")

# Base menu items
menu_items = [
    "Espresso", "Cappuccino", "Latte", "Americano", "Mocha", 
    "Flat White", "Macchiato", "Caramel Macchiato", "Frappuccino", 
    "Shaken Espresso", "Tea", "Hot Chocolate"
]

# Hot or iced drinks
hot_or_cold = ["Hot", "Iced"]

# Cup size options
cup_sizes = ["Short", "Tall", "Grande", "Venti"]

# Types of milk
milk_types = ["None", "2% Milk", "Half and Half", "Whole Milk", "Skim Milk", "Coconut Milk", "Almond Milk", "Soy Milk", "Oat Milk"]

# Types of toppings
toppings = ["None", "Drizzle", "Whipped Cream", "Cold Foam", "Cinnamon Powder", "Chocolate Powder"]

# Number of extra espresso shots 
extra_shots = ["0", "1", "2", "3", "4", "5"]

# Types of syrup
syrups = ["None", "Vanilla", "Caramel", "Hazelnut", "Peppermint", "Classic", "Mocha"]

def recognize_speech(recognizer, source):
    recognizer.pause_threshold = 0.8 
    recognizer.energy_threshold = 1000  

    audio = recognizer.listen(source)

    try:
        text = recognizer.recognize_google(audio)
        print(f"Recognized: {text}")
        return text
    except sr.UnknownValueError:
        print("Sorry, I did not understand that.")
        return None
    except sr.RequestError:
        print("Could not request results; check your internet connection.")
        return None

def speak_text(engine, text):
    engine.say(text)
    engine.runAndWait()


def construct_order_summary(parsed_order):
    order_summary_parts = []

    for quantity, item in parsed_order['items']:
        item_summary = [f"{quantity} {item}"]

        if parsed_order['sizes']:
            item_summary.append(' '.join(parsed_order['sizes']))
        if parsed_order['milks'] and parsed_order['milks'][0] != 'None':
            item_summary.append("with " + ' and '.join(parsed_order['milks']))
        if parsed_order['syrups'] and parsed_order['syrups'][0] != 'None':
            item_summary.append("with " + ' and '.join(parsed_order['syrups']))
        if parsed_order['toppings'] and parsed_order['toppings'][0] != 'None':
            item_summary.append("with " + ' and '.join(parsed_order['toppings']))
        if parsed_order['extra_shots']:
            extra_shots_summary = "with " + ' and '.join(parsed_order['extra_shots']) + " extra shot(s)"
            item_summary.append(extra_shots_summary)

        order_summary_parts.append(' '.join(item_summary))

    return ', '.join(order_summary_parts)

def calculate_price(order_components):
    total_price = 0.0

    for quantity, item_name in order_components['items']:
        base_price = random.uniform(2.5, 4.5)
        size_price = 0
        if order_components.get('sizes') and len(order_components['sizes']) > 0:
            size_price = {"Short": 0, "Tall": 0.5, "Grande": 1, "Venti": 1.5}.get(order_components['sizes'][0], 0)

        topping_price = 0.5 if 'toppings' in order_components and order_components['toppings'] and order_components['toppings'][0] != "None" else 0

        extra_shot_price = 0.5 * sum(int(shot) for shot in order_components.get('extra_shots', []) if shot.isdigit())

        syrup_price = 0.3 if 'syrups' in order_components and order_components['syrups'] and order_components['syrups'][0] != "None" else 0

        item_total_price = (base_price + size_price + topping_price + extra_shot_price + syrup_price) * quantity
        total_price += item_total_price

    return total_price

def parse_order_nlp(order):
    doc = nlp(order)

    order_components = {
        "items": [],
        "sizes": [],
        "milks": [],
        "syrups": [],
        "toppings": [],
        "extra_shots": []
    }

    current_quantity = 1  
    skip_next = False 

    for i, token in enumerate(doc):
        if skip_next:
            skip_next = False
            continue

        # print(f"Processing token: {token.text}")
        text_lower = token.text.lower()

        if token.text.isdigit():
            current_quantity = int(token.text)

        else:
            potential_item = text_lower
            if i + 1 < len(doc):
                next_word = doc[i + 1].text.lower()
                combined_item = f"{text_lower} {next_word}"
                if combined_item in [item.lower() for item in menu_items]:
                    potential_item = combined_item
                    skip_next = True

            if potential_item in [item.lower() for item in menu_items]:
                order_components['items'].append((current_quantity, potential_item.capitalize()))
                current_quantity = 1 
            elif text_lower in [size.lower() for size in cup_sizes]:
                order_components['sizes'].append(token.text.capitalize())
            elif text_lower in [milk.lower() for milk in milk_types]:
                order_components['milks'].append(token.text.capitalize())
            elif text_lower in [syrup.lower() for syrup in syrups]:
                order_components['syrups'].append(token.text.capitalize())
            elif text_lower in [topping.lower() for topping in toppings]:
                order_components['toppings'].append(token.text.capitalize())
            elif token.text in extra_shots:
                order_components['extra_shots'].append(token.text)

        print(f"Current order components: {order_components}")

    return order_components


def main():
    recognizer = sr.Recognizer()
    engine = pyttsx3.init()

    speak_text(engine, "Welcome to Starbucks! What would you like to order today?")

    full_order = ""
    total_price = 0.0

    while True:
        with sr.Microphone() as source:
            if not full_order:
                spoken_order = recognize_speech(recognizer, source)
                if spoken_order:
                    parsed_order = parse_order_nlp(spoken_order)

                    if parsed_order['items']:
                        total_price = calculate_price(parsed_order)
                        full_order = construct_order_summary(parsed_order)
                        speak_text(engine, f"Your current order is: {full_order}. Is this correct? Please say 'Yes' to confirm or 'No' to re-order.")
                    else:
                        speak_text(engine, "Sorry, we don't have that item. Please try ordering again.")
                        continue
                else:
                    continue

            confirmation_response = recognize_speech(recognizer, source)

            if confirmation_response and "yes" in confirmation_response.lower():
                speak_text(engine, "Would you like to add anything else to your order? Please say 'Yes' to add more or 'No' to finalize the order.")
                add_more_response = recognize_speech(recognizer, source)

                if add_more_response and "yes" in add_more_response.lower():
                    speak_text(engine, "What would you like to add?")
                    additional_order = recognize_speech(recognizer, source)
                    if additional_order:
                        additional_parsed_order = parse_order_nlp(additional_order)
                        if additional_parsed_order['items']:
                            total_price += calculate_price(additional_parsed_order)
                            additional_order_summary = construct_order_summary(additional_parsed_order)
                            full_order += " and " + additional_order_summary
                            speak_text(engine, f"Your updated order is: {full_order}. Is this correct? Please say 'Yes' to confirm or 'No' to modify.")
                        else:
                            speak_text(engine, "Sorry, we don't have that item. Please try ordering something else.")
                    else:
                        continue
                elif add_more_response and "no" in add_more_response.lower():
                    break
            elif confirmation_response and "no" in confirmation_response.lower():
                full_order = ""
                continue
            else:
                speak_text(engine, "Sorry, I didn't catch that. Please try again.")
                
    print(f"Thanks! Your final order is: {full_order}. The total price is ${total_price:.2f}. Have a great day!")
    speak_text(engine, f"Thanks! Your final order is: {full_order}. The total price is ${total_price:.2f}. Have a great day!")

if __name__ == "__main__":
    main()