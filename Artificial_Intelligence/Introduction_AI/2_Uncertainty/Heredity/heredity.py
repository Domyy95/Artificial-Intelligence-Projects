import csv
import itertools
import sys

PROBS = {

    # Unconditional probabilities for having gene
    "gene": {
        2: 0.01,
        1: 0.03,
        0: 0.96
    },

    "trait": {

        # Probability of trait given two copies of gene
        2: {
            True: 0.65,
            False: 0.35
        },

        # Probability of trait given one copy of gene
        1: {
            True: 0.56,
            False: 0.44
        },

        # Probability of trait given no gene
        0: {
            True: 0.01,
            False: 0.99
        }
    },

    # Mutation probability
    "mutation": 0.01
}


def main():

    # Check for proper usage
    if len(sys.argv) != 2:
        sys.exit("Usage: python heredity.py data.csv")
    people = load_data(sys.argv[1])

    # Keep track of gene and trait probabilities for each person
    probabilities = {
        person: {
            "gene": {
                2: 0,
                1: 0,
                0: 0
            },
            "trait": {
                True: 0,
                False: 0
            }
        }
        for person in people
    }

    # Loop over all sets of people who might have the trait
    names = set(people)
    for have_trait in powerset(names):

        # Check if current set of people violates known information
        fails_evidence = any(
            (people[person]["trait"] is not None and
             people[person]["trait"] != (person in have_trait))
            for person in names
        )
        if fails_evidence:
            continue

        # Loop over all sets of people who might have the gene
        for one_gene in powerset(names):
            for two_genes in powerset(names - one_gene):

                # Update probabilities with new joint probability
                p = joint_probability(people, one_gene, two_genes, have_trait)
                update(probabilities, one_gene, two_genes, have_trait, p)

    # Ensure probabilities sum to 1
    normalize(probabilities)

    # Print results
    for person in people:
        print(f"{person}:")
        for field in probabilities[person]:
            print(f"  {field.capitalize()}:")
            for value in probabilities[person][field]:
                p = probabilities[person][field][value]
                print(f"    {value}: {p:.4f}")


def load_data(filename):
    """
    Load gene and trait data from a file into a dictionary.
    File assumed to be a CSV containing fields name, mother, father, trait.
    mother, father must both be blank, or both be valid names in the CSV.
    trait should be 0 or 1 if trait is known, blank otherwise.
    """
    data = dict()
    with open(filename) as f:
        reader = csv.DictReader(f)
        for row in reader:
            name = row["name"]
            data[name] = {
                "name": name,
                "mother": row["mother"] or None,
                "father": row["father"] or None,
                "trait": (True if row["trait"] == "1" else
                          False if row["trait"] == "0" else None)
            }
    return data


def powerset(s):
    """
    Return a list of all possible subsets of set s.
    """
    s = list(s)
    return [
        set(s) for s in itertools.chain.from_iterable(
            itertools.combinations(s, r) for r in range(len(s) + 1)
        )
    ]


def joint_probability(people, one_gene, two_genes, have_trait):
    """
    Compute and return a joint probability.

    The probability returned should be the probability that
        * everyone in set `one_gene` has one copy of the gene, and
        * everyone in set `two_genes` has two copies of the gene, and
        * everyone not in `one_gene` or `two_gene` does not have the gene, and
        * everyone in set `have_trait` has the trait, and
        * everyone not in set` have_trait` does not have the trait.
    """
    mutation = PROBS['mutation']
    joint_p = 1

    for name in people.keys():
    	n_gene = 2 if name in two_genes else (1 if name in one_gene else 0)
    	is_trait = True if name in have_trait else False
    	trait_p = PROBS['trait'][n_gene][is_trait]

    	if people[name]['mother'] is None:
    		joint_p = joint_p * PROBS['gene'][n_gene] * trait_p

    	else: 
    		mum = people[name]['mother'] 
    		give_from_mum_p = 1-mutation if mum in two_genes else ( 0.5 - mutation if mum in one_gene else mutation )
    		dad = people[name]['father'] 
    		give_from_dad_p =1-mutation if dad in two_genes else ( 0.5 - mutation if dad in one_gene else mutation )
    		if n_gene == 0:
    			joint_p = joint_p * trait_p * (1 - give_from_mum_p) * (1 - give_from_dad_p) 
    		elif n_gene == 1:
    			joint_p = joint_p * trait_p * ( (1 - give_from_mum_p) * give_from_dad_p + (1 - give_from_dad_p )* give_from_mum_p )
    		else:
    			joint_p = joint_p * trait_p * (give_from_mum_p) * (give_from_dad_p)


    return joint_p



def update(probabilities, one_gene, two_genes, have_trait, p):
    """
    Add to `probabilities` a new joint probability `p`.
    Each person should have their "gene" and "trait" distributions updated.
    Which value for each distribution is updated depends on whether
    the person is in `have_gene` and `have_trait`, respectively.
    """
    
    for name in probabilities.keys():
    	n_gene = 2 if name in two_genes else (1 if name in one_gene else 0)
    	is_trait = True if name in have_trait else False

    	probabilities[name]['gene'][n_gene] += p
    	probabilities[name]['trait'][is_trait] += p    


def normalize(probabilities):
    """
    Update `probabilities` such that each probability distribution
    is normalized (i.e., sums to 1, with relative proportions the same).
    """

    for name in probabilities.keys():
    	tot_gene = sum( p for p in probabilities[name]['gene'].values())
    	tot_trait = sum( p for p in probabilities[name]['trait'].values())

    	probabilities[name]['gene'][0] = (probabilities[name]['gene'][0])/tot_gene
    	probabilities[name]['gene'][1] = (probabilities[name]['gene'][1])/tot_gene
    	probabilities[name]['gene'][2] = (probabilities[name]['gene'][2])/tot_gene

    	probabilities[name]['trait'][True] = probabilities[name]['trait'][True] / tot_trait
    	probabilities[name]['trait'][False] = probabilities[name]['trait'][False] / tot_trait  


if __name__ == "__main__":
    main()
