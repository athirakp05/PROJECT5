#views.py
import tkinter as tk
from tkinter import ttk, messagebox
from django.shortcuts import render
import pandas as pd
from sklearn.tree import DecisionTreeClassifier
from sklearn import preprocessing
from sklearn.metrics import accuracy_score, confusion_matrix, classification_report
from sklearn.model_selection import train_test_split
import matplotlib.pyplot as plt
import numpy as np

# Load the dataset
df = pd.read_csv(r'C:\Users\athir\Desktop\milkquality.csv')

# Remove leading spaces from column names
df.columns = df.columns.str.strip()


# Preprocessing
label_encoder = preprocessing.LabelEncoder()
df['grade'] = label_encoder.fit_transform(df['grade'])

# Define features and target variable
milk_features = ['pH', 'temperature', 'taste', 'odor', 'fat', 'turbidity', 'colour']
X = df[milk_features]
y = df['grade']

# Split the data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
# Train the Decision Tree Classifier model with adjusted hyperparameters
dt_clf = DecisionTreeClassifier(max_depth=5, min_samples_split=5)
dt_clf.fit(X_train, y_train)

# Get feature importance
feature_importance = dt_clf.feature_importances_


# Function to calculate accuracy score
def calculate_accuracy():
    # Predict the labels for testing data
    y_pred = dt_clf.predict(X_test)

    # Calculate the accuracy score
    accuracy = accuracy_score(y_test, y_pred)
    messagebox.showinfo("Accuracy", f"The accuracy score of the model is: {accuracy}")

    # Generate confusion matrix
    cm = confusion_matrix(y_test, y_pred)

    # Generate classification report
    cr = classification_report(y_test, y_pred, target_names=['low_quality', 'medium_quality', 'high_quality'])

    # Display confusion matrix and classification report
    messagebox.showinfo("Confusion Matrix", f"Confusion Matrix:\n{cm}\n\nClassification Report:\n{cr}")


# Function to predict grade and display quality variations graph
def predict_grade():
    try:
        # Get user input
        user_input = {}
        for i, feature in enumerate(milk_features):
            if feature in ['taste', 'odor', 'fat', 'turbidity']:  # If feature requires dropdown selection
                user_input[feature] = int(entry_boxes[i].get())  # Get selected value as integer
            else:
                user_input[feature] = float(entry_boxes[i].get())  # Get numerical value

        # Convert user input to DataFrame
        user_df = pd.DataFrame([user_input])

        # Predict the probabilities of each grade based on user input
        probabilities = dt_clf.predict_proba(user_df)[0]

        # Plot quality variations graph
        plt.figure(figsize=(8, 5))
        plt.bar(df['grade'].unique(), probabilities, color=['lightcoral', 'lightskyblue', 'lightgreen'])
        plt.xlabel('Milk Quality Grade')
        plt.ylabel('Probability')
        plt.title('Quality Variations in Milk')
        plt.xticks(np.arange(3), labels=['Low Quality', 'Medium Quality', 'High Quality'])
        plt.show()

        # Display the neural network outputs
        grades = ['low_quality', 'medium_quality', 'high_quality']
        for grade, prob in zip(grades, probabilities):
            messagebox.showinfo("Neural Network Outputs", f"{grade.capitalize()}: {prob * 100:.2f}%")
    except ValueError:
        messagebox.showerror("Error", "Please enter valid numerical values.")


# Create Tkinter window
window = tk.Tk()
window.title("Milk Quality Prediction")

# Create input fields with ttk style
entry_boxes = []
for i, feature in enumerate(milk_features):
    label = tk.Label(window, text=feature, font=("Arial", 12), pady=5, padx=5)
    label.grid(row=i, column=0, sticky="w")

    # Create dropdown menu for taste, odor, fat, and turbidity; otherwise, create a normal entry field
    if feature in ['taste', 'odor', 'fat', 'turbidity']:
        entry = ttk.Combobox(window, values=[0, 1], font=("Arial", 12), state="readonly", width=5)
        entry.grid(row=i, column=1, pady=5, padx=5, sticky="e")
    else:
        entry = ttk.Entry(window, font=("Arial", 12))
        entry.grid(row=i, column=1, pady=5, padx=5, sticky="e")
    entry_boxes.append(entry)

# Create predict button
predict_button = tk.Button(window, text="Predict Grade", font=("Arial", 12), command=predict_grade)
predict_button.grid(row=len(milk_features), columnspan=2, pady=10)

# Create accuracy button
accuracy_button = tk.Button(window, text="Calculate Accuracy", font=("Arial", 12), command=calculate_accuracy)
accuracy_button.grid(row=len(milk_features) + 1, columnspan=2, pady=10)


# Function to visualize training and selection errors during training
def visualize_errors():
    # Define the number of neurons and corresponding errors
    neurons = [1, 2, 3, 4, 5]
    training_errors = [0.3, 0.25, 0.2, 0.15, 0.1]  # Example values for demonstration
    selection_errors = [0.35, 0.3, 0.25, 0.2, 0.15]  # Example values for demonstration

    # Plot errors
    plt.figure(figsize=(8, 5))
    plt.plot(neurons, training_errors, marker='o', label='Training Error', color='blue')
    plt.plot(neurons, selection_errors, marker='o', label='Selection Error', color='orange')
    plt.xlabel('Number of Neurons')
    plt.ylabel('Error')
    plt.title('Training and Selection Errors vs. Number of Neurons')
    plt.legend()
    plt.grid(True)
    plt.show()


# Create button for visualizing errors
errors_button = tk.Button(window, text="Visualize Errors", font=("Arial", 12), command=visualize_errors)
errors_button.grid(row=len(milk_features) + 2, columnspan=2, pady=10)

# Run the Tkinter event loop
window.mainloop()

def milk_quality_prediction(request):
    return render(request, 'Milk/milk_quality_prediction.html')
