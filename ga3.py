import pandas as pd
import numpy as np

# Read the text file into a DataFrame
df = pd.read_csv('msft_data.txt', sep='\t')

# Calculate the predicted next day's move using the formula
def predict_next_day_move(row, weights_bias):
    # # Define the weights and bias (you can optimize these with GE)
    # weights = [0.1, 0.2, 0.3, 0.4, 0.5, 0.6]  # Example weights
    # bias = 0.0  # Example bias        
    
    # Split the weights_bias string into individual weights and bias
    weights_bias = weights_bias.split(',')
    # Extract weights and bias as separate lists
    weights = [float(w) for w in weights_bias[:-1]]  # Extract all elements except the last one
    bias = float(weights_bias[-1])  # Extract the last element as bias
    
    # print(str(weights[3]) + " " + str(bias))
    
    # Extract the percentage moves of the previous 6 days
    prev_moves = [row[f'Percent_Move(t-{i})'] for i in range(0, 5)]
       
    # Calculate the predicted next day's move
    predicted_move = sum(w * prev_move for w, prev_move in zip(weights, prev_moves)) + bias
    
    return predicted_move


def fitness(weights_bias):
    # Calculate the predicted moves for each row starting from the 7th row
    df['Predicted_Move'] = df.iloc[6:].apply(predict_next_day_move, axis=1, weights_bias=(weights_bias))

    
    # Calculate the error (absolute difference) between the predicted move and the actual next day's move
    df['Error'] = abs(df['Predicted_Move'] - df['Next_Day_Move'])
    
    # Calculate the average error
    viga = df['Error'].mean()
    #print(viga)
    return viga

#viga = fitness("0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.0")
#print(f"Average error: {viga}")
