from training.train import evolve_generation

def main():
    print("Welcome to Yatzi!")
    next_gen = None
    for i in range (5):
        if next_gen:
            x = evolve_generation(next_gen)
        else:
            x = evolve_generation()
        next_gen = x[0]
        
if __name__ == "__main__":
    main()