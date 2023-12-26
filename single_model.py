from scipy.stats import binom

def calculate_wound_probability(num_attackers, num_weapon_attacks, bs_ws, strength, armor_penetration, damage, toughness, save, invulnerable_save, fnp, sustained_hits, lethal_hits, devastating_wounds,  reroll_hits):
    """
    Calculates the probability of inflicting a wound per attack and the total number of attacks
    based on the provided attack and defense profiles, as well as additional mechanics like Sustained Hits,
    Lethal Hits, and Devastating Wounds.
    """
    # Calculate the total number of attacks
    num_attacks = num_attackers * num_weapon_attacks

    # Probability of hitting and scoring a critical hit based on BS/WS
    prob_hit = (7 - bs_ws) / 6
    prob_critical_hit = 1 / 6  # Assuming critical hit on a roll of 6

    # Adjust for reroll hits
    if reroll_hits:
        # Calculate the probability of missing and hitting the reroll
        prob_miss_then_hit = (1 - prob_hit) * prob_hit
        # Add the probabilty hitting in the reroll to the hit total
        prob_hit += prob_miss_then_hit

    additional_hits = prob_critical_hit * sustained_hits  # Additional hits per attack
    num_attacks += num_attacks * additional_hits  # Total additional hits

    prob_normal_hits = prob_hit - prob_critical_hit
    total_hits = num_attacks * prob_normal_hits

    # Adjust for sustained hits
    if sustained_hits:
        total_critical_hits = num_attacks * prob_critical_hit
        total_sustained_hits = total_critical_hits * sustained_hits
        total_hits += total_critical_hits + total_sustained_hits

    # Probability of wounding based on the comparison of strength and toughness
    if strength >= 2 * toughness:
        prob_wound = 5/6
    elif strength > toughness:
        prob_wound = 2/3
    elif strength == toughness:
        prob_wound = 1/2
    elif strength * 2 <= toughness:
        prob_wound = 1/6
    else:
        prob_wound = 1/3

    # Probability of failing the save (considering AP and choosing the best between SV and INVUL)
    mod_save = max(save - armor_penetration, invulnerable_save)
    prob_fail_save = (7 - mod_save) / 6

    # Adjust for devastating wounds
    if devastating_wounds:
        # Critical wounds bypass saves, adjust the fail save probability
        prob_fail_save += prob_critical_hit * (1 - prob_fail_save)

    # Probability of failing FNP
    prob_fail_fnp = (7 - fnp) / 6

    # Total probability of inflicting a wound per attack
    wound_prob = prob_hit * prob_wound * prob_fail_save * prob_fail_fnp

    if lethal_hits:
        prob_wound_final = (total_critical_hits * 1 + (total_hits - total_critical_hits) * wound_prob) / total_hits
    else:
        prob_wound_final = wound_prob

    return prob_wound_final, num_attacks

def calculate_success_probability(wound_prob, num_attacks_rounded, target_wounds):
    """
    Calculates the probability that the number of wounds generated is 
    equal to or greater than a given value.
    """
    # Calculate the binomial distribution for the range of interest wounds
    probabilities = binom.pmf(range(target_wounds, num_attacks_rounded+1), num_attacks_rounded, wound_prob)

    # Sum the probabilities to get the total probability of obtaining target_wounds or more wounds
    total_probability = sum(probabilities)

    return total_probability

# Attack and defense profiles
attack_profile = {
    'num_attackers': 3,
    'num_weapon_attacks': 3,
    'bs_ws': 5,
    'strength': 5,
    'armor_penetration': 1,
    'damage': 3,
    'sustained_hits': 2,
    'lethal_hits': True,
    'devastating_wounds': True,
    'reroll_hits': False
}

defense_profile = {
    'toughness': 4,
    'save': 2,
    'invulnerable_save': 4,
    'fnp': 6
}

target_wounds = 2

# Calculate wound probability and number of attacks
wound_prob, num_attacks = calculate_wound_probability(**attack_profile, **defense_profile)
num_attacks_rounded = round(num_attacks)

# Calculate and display the total probability
total_probability = calculate_success_probability(wound_prob, num_attacks_rounded, target_wounds)
print(f"""
      The probability of wounding per attack is {wound_prob:.2%}
      The total number of attacks rounded is {num_attacks_rounded}
      The probability of generating {target_wounds} or more wounds with {num_attacks} attacks is: {total_probability:.2%}
      """)
