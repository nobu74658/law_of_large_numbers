# Statistical Laws Demonstration

This project demonstrates fundamental statistical laws through numerical experiments using a uniform distribution:

1. **Law of Large Numbers**: Shows how the sample proportion converges to the theoretical probability as the sample size increases
2. **Central Limit Theorem**: Illustrates how the distribution of sample means approaches a normal distribution regardless of the original distribution

## Problem Statement

The experiment involves:
1. Generating random numbers from a uniform distribution U[0,1]
2. Counting a "win" if the number is less than or equal to 0.4
3. Calculating the win rate (number of wins / total trials)
4. Observing how the win rate converges to the theoretical probability (0.4) as the number of trials increases

## Implementation

### Single Run Experiment

The Python script `law_of_large_numbers.py` performs the following:
- Generates random numbers from a uniform distribution U[0,1]
- Calculates the win rate for different sample sizes (n = 10, 50, 100, 500, 1000, 5000, 10000, 50000, 100000)
- Plots the results on a graph with a logarithmic x-axis
- Shows the convergence to the theoretical probability of 0.4

### Multiple Runs Experiment

The Python script `law_of_large_numbers_multiple_runs.py` extends the analysis by:
- Running the experiment multiple times (default: 5 runs)
- Plotting each run on the same graph to show the variation between runs
- Calculating and plotting the average win rate across all runs
- Computing statistics such as standard deviation for each sample size
- Demonstrating how the variation between runs decreases as the sample size increases

## Results

The experiment demonstrates that as the number of trials increases, the observed win rate converges to the theoretical probability of 0.4. This is a practical demonstration of the Law of Large Numbers, which states that as the number of trials increases, the average of the results will converge to the expected value.

### Single Run Results

From the single run results, we can observe that:
- With small sample sizes (n < 100), there is significant variation in the win rate
- As n increases to 1000 and beyond, the win rate stabilizes closer to 0.4
- By n = 10000, the win rate is very close to the theoretical value
- At n = 100000, the win rate is approximately 0.399, which is extremely close to the theoretical 0.4

### Multiple Runs Results

The multiple runs experiment provides additional insights:
- Each individual run shows the same general trend of convergence to 0.4
- The standard deviation between runs decreases significantly as n increases
- At n = 10, the standard deviation is approximately 0.2, showing high variability
- At n = 100000, the standard deviation is less than 0.0015, showing very low variability
- The average of multiple runs converges to the theoretical value more smoothly than any individual run

## Running the Code

### Single Run Experiment

To run the single experiment:

```bash
python law_of_large_numbers.py
```

This will generate a graph showing the convergence of the win rate to the theoretical probability.

### Multiple Runs Experiment

To run multiple experiments and see the variation between runs:

```bash
python law_of_large_numbers_multiple_runs.py
```

This will generate a graph showing multiple runs and their average, along with statistics about the standard deviation at each sample size.

## Central Limit Theorem

The central limit theorem states that the distribution of sample means approximates a normal distribution as the sample size gets larger, regardless of the population's distribution.

The script `central_limit_theorem.py` demonstrates this by:
- Generating samples from a uniform distribution U[0,1]
- Calculating the mean of each sample for different sample sizes (n = 1, 2, 5, 10, 30, 100)
- Plotting the distribution of these sample means
- Comparing the actual distribution with the theoretical normal distribution

The results show that:
- With n = 1, the distribution is uniform (identical to the original distribution)
- As n increases to 2, 5, and 10, the distribution gradually becomes more bell-shaped
- By n = 30, the distribution is very close to normal
- At n = 100, the distribution is practically indistinguishable from a normal distribution

The standard deviation of the sample means follows the theoretical formula σ/√n, where σ is the standard deviation of the original distribution.

## Running the Central Limit Theorem Demo

```bash
python central_limit_theorem.py
```

## Combined Demonstration

The script `combined_demonstration.py` provides a comprehensive visualization of both the Law of Large Numbers and the Central Limit Theorem in a single analysis:

### Features:
- Runs experiments with different sample sizes (10 to 3000)
- Creates a 2x2 grid of plots showing:
  1. Convergence of the mean win rate to the theoretical probability (Law of Large Numbers)
  2. Decrease in standard deviation as sample size increases
  3. Distribution of win rates for a small sample size compared to normal distribution
  4. Distribution of win rates for a large sample size compared to normal distribution
- Provides statistical information including actual vs. theoretical standard deviations

### Running the Combined Demo:

```bash
python combined_demonstration.py
```

## Running All Demonstrations

For convenience, you can run all demonstrations sequentially with:

```bash
python run_all_demos.py
```

This script will:
1. Run each demonstration one by one
2. Pause between demonstrations to allow you to examine the results
3. Display execution time for each demonstration

## Dependencies

- NumPy
- Matplotlib
- SciPy (for probability distributions)

You can install all dependencies with:

```bash
pip install -r requirements.txt
```