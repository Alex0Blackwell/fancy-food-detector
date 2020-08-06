import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'  # restrict tensorflow debugging info

from imageai.Prediction import ImagePrediction
import time as t
import spoonacular as sp
import json


def waitAnim():
    for i in range(1, 3):
        print('.' * i, end="\r")
        t.sleep(0.5)
    print("...")



def main():
    f = open('settings.json',)
    data = json.load(f)

    photoRef = data["Photo_Reference"];

    api = sp.API(data["API_Key"])

    print("Nice meal! I think that the following ingredients may be in the meal:")

    prediction = ImagePrediction()
    prediction.setModelTypeAsResNet()
    prediction.setModelPath("./training-data/resnet50_weights_tf_dim_ordering_tf_kernels.h5")
    prediction.loadModel()


    try:
        predictions, percentage_probabilities = prediction.predictImage("./images/"+photoRef, result_count=8)
    except Exception as e:
        print("Oops that didn't work :(\nMake sure you are referencing the file properly.")

    excludeFile = open("./dict/exclude.txt", "r")
    exclude = excludeFile.read();

    ingredients = []

    for i in range(len(predictions)):
        if(predictions[i] not in exclude):
            ingredients.append(predictions[i].replace('_', ' '))

    for i in range(len(ingredients)):
        if(i == len(ingredients)-1):
            print("and " + ingredients[i])
        else:
            print(ingredients[i] + ", ", end="")


    waitAnim()
    # get how expensive each ingredient is
    print("\nOk ok nice nice, let me guess how expensive the ingredients in that meal was!")
    totalPrice = thisPrice = 0;
    for i in range(len(ingredients)):
        response = api.parse_ingredients(ingredients[i], servings=1)
        data = response.json()

        try:
            thisPrice = float(data[0]['estimatedCost']['value']) * 10;

            if(i == 0):
                print(f"Ok I think the {ingredients[i]} was {int(thisPrice)} cents")
            else:
                print(f"and the {ingredients[i]} was {int(thisPrice)} cents")
        except:
            print(f"Ok I have no idea how much the {ingredients[i]} would cost.")
            thisPrice = 0;

        totalPrice += thisPrice;



    totalPrice = int(totalPrice) / 100

    waitAnim()
    print(f"\nOk the results are in!\nI guess cost for that meal's raw ingredients was about ${totalPrice} American.")


if __name__ == '__main__':
    main()
