import pandas as pd
from itertools import combinations

# The transactions from the dataset
transactions = [
    ["A", "B", "C", "D", "E", "F"],
    ["B", "D", "E", "F", "G"],
    ["A", "B", "E", "F", "G"],
    ["A", "B", "C", "G", "H"],
    ["B", "C", "E", "H"],
    ["A", "B", "C", "F", "G"],
    ["A", "B", "D", "F"],
    ["C", "D", "E", "H"],
    ["B", "D", "E", "G"],
    ["A", "C", "E", "F", "H"],
]

# Minimum support and confidence
MIN_SUPPORT = 2
MIN_CONFIDENCE = 0.60


# Function to calculate support
def calc_support(transactions, itemset):
    return sum(1 for trans in transactions if set(itemset).issubset(set(trans)))


# Function to calculate confidence
def calc_confidence(antecedent, consequent):
    antecedent_support = calc_support(transactions, antecedent.split("，"))
    rule_support = calc_support(
        transactions, antecedent.split("，") + consequent.split("，")
    )
    return rule_support / antecedent_support


# Generate all possible non-empty itemsets
itemsets = []
for i in range(1, len(set().union(*transactions)) + 1):
    for combination in combinations(sorted(set().union(*transactions)), i):
        itemsets.append(combination)

# Dataframe to hold itemsets and support
support_data = pd.DataFrame({"itemset": ["，".join(itemset) for itemset in itemsets]})
support_data["support"] = support_data["itemset"].apply(
    lambda x: calc_support(transactions, x.split("，"))
)

# Frequent itemsets with support >= min_support
frequent_itemsets = support_data[support_data["support"] >= MIN_SUPPORT]

# Generate rules from the frequent itemsets
rules = []
for itemset in frequent_itemsets["itemset"]:
    items = itemset.split("，")
    for i in range(1, len(items)):
        for antecedent in combinations(items, i):
            antecedent = set(antecedent)
            consequent = set(items) - antecedent
            if consequent:
                rules.append((antecedent, consequent))

# Dataframe to hold the rules
rules_data = pd.DataFrame(rules, columns=["antecedent", "consequent"])
rules_data["antecedent"] = rules_data["antecedent"].apply(lambda x: "，".join(x))
rules_data["consequent"] = rules_data["consequent"].apply(lambda x: "，".join(x))


# Calculating confidence for each rule
rules_data["confidence"] = rules_data.apply(
    lambda x: calc_confidence(x["antecedent"], x["consequent"]), axis=1
)

# Strong rules with confidence >= min_confidence
strong_rules = rules_data[rules_data["confidence"] >= MIN_CONFIDENCE].copy()

# Sort the itemsets and rules by support and confidence respectively
frequent_itemsets.sort_values(by="support", ascending=False, inplace=True)
strong_rules.sort_values(by="confidence", ascending=False, inplace=True)

# Convert to tuples for display
strong_rules["antecedent"] = strong_rules["antecedent"].apply(
    lambda x: tuple(x.split("，"))
)
strong_rules["consequent"] = strong_rules["consequent"].apply(
    lambda x: tuple(x.split("，"))
)

# Save the frequent itemsets and strong rules to CSV files
itemsets_file_path = "./frequent_itemsets.csv"
rules_file_path = "./strong_rules.csv"
frequent_itemsets.to_csv(itemsets_file_path, index=False)
strong_rules.to_csv(rules_file_path, index=False)
