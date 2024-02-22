# VoiceBarista

Developed as the final project for my Data Science 2 course, the VoiceBarista is a Python application designed to facilitate the ordering process at a coffee shop, such as Starbucks. It utilizes speech recognition to take orders from customers, processes the orders to understand the specific requests, and uses text-to-speech to communicate with the customer. This application supports customization of orders, including size, type of milk, additional shots, and more.

## Features
- Speech Recognition: Captures customer orders through spoken language.
- Text-to-Speech: Communicates with the customer to confirm orders or ask for clarifications.
- Customizable Orders: Allows for detailed customization, including drink type, hot or iced, cup size, type of milk, toppings, extra espresso shots, and syrups.
- Dynamic Pricing: Calculates the price of the order based on the selections made.

## Dependencies
- speech_recognition: For recognizing spoken words.
- pyttsx3: Text-to-speech conversion library.
- pandas: Data manipulation and analysis.
- random: To generate random pricing within a range.
- spacy: Natural language processing for parsing orders.
- en_core_web_sm: SpaCy's small English model for language understanding.

Ensure you have the above libraries installed in your Python environment. You can install them using pip:
```
pip install SpeechRecognition pyttsx3 pandas spacy random
python -m spacy download en_core_web_sm
```

## Usage
- Starting the Application: Run the script to start the application. The application will greet the customer and ask for their order.

- Placing an Order: The customer speaks their order into the microphone. The application recognizes the speech and processes the order.

- Order Confirmation: After processing, the application repeats the order back to the customer using text-to-speech for confirmation.

- Adding to the Order: Customers can add more items to their order or finalize their order.

- Finalization: Once the order is confirmed, the application calculates the total price and informs the customer.

## Customization Options

- menu_items: Available coffee and other drink items.
- hot_or_cold: Option for hot or iced drinks.
- cup_sizes: Sizes available for the drinks.
- milk_types: Types of milk or milk alternatives.
- toppings: Additional toppings.
- extra_shots: Option for extra espresso shots.
- syrups: Flavor syrups.
