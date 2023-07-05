import random

def generate_centroid_number(centroid, range_start, range_end):
    weights = [abs(x - centroid) for x in range(range_start, range_end+1)]
    total_weight = sum(weights)
    probabilities = [weight/total_weight for weight in weights]
    number = random.choices(range(range_start, range_end+1), probabilities)[0]
    return number

# Example usage
centroid_value = 9
max = centroid_value + 2
min = centroid_value - 2
generated_number = generate_centroid_number(centroid_value, min, max)
print(generated_number)


def bimaximax(criteria):
    max_vals = [max(criterion) for criterion in criteria]
    bimaximax_value = max(max_vals)
    return bimaximax_value

# Example usage:
criteria = [[5, 10, 15], [20, 25, 30], [35, 40, 45]]
result = bimaximax(criteria)
print(result)


