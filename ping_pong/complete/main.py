import NeatTrain
import NeatGame

def main():
    # neat_train(train_neat_game) # to see the process of learning
    NeatTrain.neat_train(NeatTrain.train_neat_sim, 50)
    NeatGame.neat_best_play()
    
if __name__ == "__main__":
    main()
