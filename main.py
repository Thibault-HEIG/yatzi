from training.train import evolve_generation
from tracking.ledger import TrainingLogger

def main():
    print("Welcome to Yatzi!")
    logger = TrainingLogger()
    next_gen = None
    for i in range (50):
        if next_gen:
            x = evolve_generation(i, next_gen, logger=logger)
        else:
            x = evolve_generation(i, logger=logger)
        next_gen = x[0]
        
if __name__ == "__main__":
    main()