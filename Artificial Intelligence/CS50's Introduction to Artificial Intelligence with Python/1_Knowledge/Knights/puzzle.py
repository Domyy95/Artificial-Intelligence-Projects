from logic import *

def get_builted_cond(say,knight,knave):
    rule = And(Or(knight,knave),Not(And(knave,knight)))
    if say is None:
        return rule
    isKnight = Implication(knight,say)
    isKnave = Implication(knave,Not(say))
    cond = And(rule,isKnight,isKnave)
    return cond 

AKnight = Symbol("A is a Knight")
AKnave = Symbol("A is a Knave")

BKnight = Symbol("B is a Knight")
BKnave = Symbol("B is a Knave")

CKnight = Symbol("C is a Knight")
CKnave = Symbol("C is a Knave")

# Puzzle 0
# A says "I am both a knight and a knave."
Asay = And(AKnave,AKnight)
Acond = get_builted_cond(Asay,AKnight,AKnave)
knowledge0 = And(
    Acond
)

# Puzzle 1  
# A says "We are both knaves."
# B says nothing.
Asay = And(AKnave,BKnave)
Acond = get_builted_cond(Asay,AKnight,AKnave)
Bcond = get_builted_cond(None,BKnight,BKnave)
knowledge1 = And(
    Acond,Bcond
)

# Puzzle 2
# A says "We are the same kind."
# B says "We are of different kinds."
Asay = Or(And(AKnave,BKnave),And(AKnight,BKnight))
Acond = get_builted_cond(Asay,AKnight,AKnave)
Bsay = Or(And(AKnave,BKnight),And(AKnight,BKnave))
Bcond = get_builted_cond(Bsay,BKnight,BKnave)
knowledge2 = And(
    Acond,Bcond
)

# Puzzle 3
# A says either "I am a knight." or "I am a knave.", but you don't know which.
# B says "A said 'I am a knave'."
# B says "C is a knave."
# C says "A is a knight."
Asay = Or(AKnave,AKnight)
Acond = get_builted_cond(Asay,AKnight,AKnave)
Bsay = And(CKnave,AKnave)
Bcond = get_builted_cond(Bsay,BKnight,BKnave)
Csay = AKnight
Ccond = get_builted_cond(Csay,CKnight,CKnave)
knowledge3 = And(
   Acond,Bcond,Ccond
)
  

def main():
    symbols = [AKnight, AKnave, BKnight, BKnave, CKnight, CKnave]
    puzzles = [
        ("Puzzle 0", knowledge0),
        ("Puzzle 1", knowledge1),
        ("Puzzle 2", knowledge2),
        ("Puzzle 3", knowledge3)
    ]
    for puzzle, knowledge in puzzles:
        print(puzzle)
        if len(knowledge.conjuncts) == 0:
            print("    Not yet implemented.")
        else:
            for symbol in symbols:
                if model_check(knowledge, symbol):
                    print(f"    {symbol}")


if __name__ == "__main__":
    main()
