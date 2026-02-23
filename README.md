# Exam Rank 02 — Mock Exam

Simulateur d'examen pour préparer le **Exam Rank 02** de l'école 42.
Le programme reproduit les conditions réelles : timer de 3h, sujets aléatoires par niveau, correction automatique, et révélation de la solution à la fin.

---

## Prérequis

- Python 3.10+
- `cc` (clang ou gcc) disponible dans le PATH

---

## Lancement

```bash
python3 main.py
```

Mode debug (accès à `skip`, timer affiché avec `[DEBUG]`) :

```bash
python3 main.py --debug
```

Filtrer par niveau(x) :

```bash
# Un seul niveau
python3 main.py --levels 3

# Plusieurs niveaux (virgule)
python3 main.py --levels 3,4

# Plage de niveaux (tiret)
python3 main.py --levels 1-3

# Combinable avec --debug
python3 main.py --levels 3,4 --debug
```

---

## Déroulement d'une session

1. Le programme choisit un sujet aléatoire parmi ceux du **level 1** et le copie dans `subjects/`.
2. Tu lis le sujet et tu écris ta réponse dans `render/`.
3. Tu tapes `grademe` pour te faire corriger.
4. Si tous les tests passent, tu passes automatiquement au niveau suivant.
5. Il y a **4 niveaux** au total. Les compléter tous avant la fin du temps = réussite.

---

## Commandes disponibles

| Commande  | Disponibilité | Description |
|-----------|--------------|-------------|
| `grademe` | Toujours | Compile et teste ton rendu dans `render/` |
| `finish`  | Toujours | Termine l'examen et révèle la solution du sujet courant |
| `quit`    | Toujours | Alias de `finish` |
| `status`  | Toujours | Affiche le niveau actuel, le sujet et les temps écoulé/restant |
| `subject` | Toujours | Rappelle le nom et le fichier du sujet courant |
| `skip`    | Debug only | Passe l'exercice sans le réussir et révèle la solution |

---

## Structure des dossiers

```
exam02_mock_exam/
├── main.py             # Programme principal
├── exams/              # Sujets des exercices (fichiers .txt)
│   ├── level1/
│   ├── level2/
│   ├── level3/
│   ├── level4/
│   └── .tester/        # Testers automatiques pour les fonctions
│       ├── run_all.sh          # Script de test autonome
│       ├── ft_list.h           # Header fourni par l'examen (listes)
│       ├── list.h              # Header fourni par l'examen (sort_list)
│       ├── t_point.h           # Header fourni par l'examen (flood_fill)
│       └── *_test.c            # 28 mains de test (un par fonction)
├── subjects/           # Sujet actif (1 fichier .txt à la fois)
├── render/             # Dossier où tu déposes ton rendu (.c, .h)
└── traces/             # Résultats des corrections et solutions révélées
```

---

## Workflow typique

```
# Lire le sujet
cat subjects/ft_strlen.txt

# Écrire ta solution
vim render/ft_strlen.c

# Se faire corriger
grademe

# Si tous les tests passent → passage automatique au niveau suivant
# Sinon → lire le score et corriger

# Terminer et voir la solution
finish
```

---

## Système de correction (`grademe`)

1. Vérifie que tous les fichiers listés dans `Expected files` sont présents dans `render/`.
2. Compile avec `cc -Wall -Wextra -Werror`.
3. **Sujets programmes** (avec exemples `$> ./nom args`) : exécute chaque exemple et compare la sortie attendue.
4. **Sujets fonctions** (sans exemples) : compile puis exécute le tester dédié dans `exams/.tester/` s'il existe. Le tester doit afficher `ALL TESTS PASSED` et retourner 0.
5. Si tous les tests passent → avance au niveau suivant.
6. Génère un fichier de trace dans `traces/` avec le détail de chaque test.

### Tester autonome

Pour tester tes fonctions sans lancer le grader :

```bash
# Tester toutes les fonctions (si les .c sont dans render/)
./exams/.tester/run_all.sh

# Tester une seule fonction
./exams/.tester/run_all.sh ft_strlen
```

Chaque tester couvre 10+ cas dont les cas limites (NULL, chaîne vide, négatifs…).

---

## Solutions

Les solutions sont **embarquées dans `main.py`** sous forme encodée — elles ne sont **jamais accessibles pendant l'examen**.

Elles sont révélées dans `traces/` uniquement lorsque tu tapes `finish`, `quit`, ou `skip` (debug).

Exemple : après `finish` sur `rotone`, le fichier `traces/rotone_solution.c` est créé.

---

## Exercices par niveau

La colonne **T** indique si un tester automatique est disponible dans `exams/.tester/`.

### Level 1 (12 exercices)
| Exercice | T | Description |
|---|:-:|---|
| `first_word` | | Affiche le premier mot d'une chaîne |
| `fizzbuzz` | | FizzBuzz de 1 à 100 |
| `ft_putstr` | ✓ | Affiche une chaîne avec `write` |
| `ft_strcpy` | ✓ | Copie une chaîne |
| `ft_strlen` | ✓ | Retourne la longueur d'une chaîne |
| `ft_swap` | ✓ | Échange deux entiers |
| `repeat_alpha` | | Répète chaque lettre autant de fois que sa position dans l'alphabet |
| `rev_print` | | Affiche une chaîne à l'envers |
| `rot_13` | | Applique le chiffrement ROT-13 |
| `rotone` | | Décale chaque lettre d'un rang |
| `search_and_replace` | | Remplace un caractère par un autre |
| `ulstr` | | Alterne majuscules/minuscules |

### Level 2 (20 exercices)
| Exercice | T | Description |
|---|:-:|---|
| `alpha_mirror` | | Symétrie de l'alphabet (a↔z, b↔y…) |
| `camel_to_snake` | | Convertit camelCase en snake_case |
| `do_op` | | Effectue une opération arithmétique (+, -, *, /, %) |
| `ft_atoi` | ✓ | Implémente `atoi` |
| `is_power_of_2` | ✓ | Vérifie si n est une puissance de 2 |
| `ft_strcmp` | ✓ | Implémente `strcmp` |
| `ft_strcspn` | ✓ | Implémente `strcspn` |
| `ft_strdup` | ✓ | Implémente `strdup` |
| `ft_strpbrk` | ✓ | Implémente `strpbrk` |
| `ft_strrev` | ✓ | Inverse une chaîne en place |
| `ft_strspn` | ✓ | Implémente `strspn` |
| `inter` | | Affiche les caractères communs à deux chaînes (sans doublon) |
| `last_word` | | Affiche le dernier mot d'une chaîne |
| `max` | ✓ | Retourne le maximum d'un tableau |
| `print_bits` | ✓ | Affiche les bits d'un octet |
| `reverse_bits` | ✓ | Inverse les bits d'un octet |
| `snake_to_camel` | | Convertit snake_case en camelCase |
| `swap_bits` | ✓ | Échange les deux nibbles (groupes de 4 bits) |
| `union` | | Affiche l'union de deux chaînes (sans doublon) |
| `wdmatch` | | Vérifie si les lettres de s1 apparaissent dans l'ordre dans s2 |

### Level 3 (15 exercices)
| Exercice | T | Description |
|---|:-:|---|
| `add_prime_sum` | | Somme des nombres premiers jusqu'à n |
| `epur_str` | | Supprime les espaces superflus d'une chaîne |
| `expand_str` | | Sépare les mots par exactement 3 espaces |
| `ft_atoi_base` | ✓ | `atoi` dans une base donnée (base ≤ 16) |
| `ft_list_size` | ✓ | Compte les éléments d'une liste chaînée |
| `ft_range` | ✓ | Tableau d'entiers de start à end (inclus des deux côtés) |
| `ft_rrange` | ✓ | Idem, de end vers start |
| `hidenp` | | Vérifie si s1 est une sous-séquence de s2 |
| `lcm` | ✓ | Calcule le PPCM |
| `paramsum` | | Affiche le nombre d'arguments |
| `pgcd` | | Calcule le PGCD |
| `print_hex` | | Affiche un entier en hexadécimal |
| `rstr_capitalizer` | | Capitalise la dernière lettre de chaque mot |
| `str_capitalizer` | | Capitalise la première lettre de chaque mot |
| `tab_mult` | | Affiche la table de multiplication de n |

### Level 4 (10 exercices)
| Exercice | T | Description |
|---|:-:|---|
| `flood_fill` | ✓ | Remplit une zone d'un tableau 2D (utilise `t_point.h`) |
| `fprime` | | Affiche les facteurs premiers |
| `ft_itoa` | ✓ | Convertit un entier en chaîne |
| `ft_list_foreach` | ✓ | Applique une fonction à chaque élément d'une liste |
| `ft_list_remove_if` | ✓ | Supprime les nœuds d'une liste selon un critère |
| `ft_split` | ✓ | Découpe une chaîne selon les espaces/tabs/newlines |
| `rev_wstr` | | Affiche les mots dans l'ordre inverse |
| `rostring` | | Déplace le premier mot à la fin |
| `sort_int_tab` | ✓ | Trie un tableau d'entiers (tri à bulles) |
| `sort_list` | ✓ | Trie une liste chaînée avec une fonction de comparaison |

---

## Conseils pour l'examen

- Lis bien le sujet, notamment **Expected files** et les exemples `$>`
- Place **tous** les fichiers attendus dans `render/` avant de taper `grademe`
- Les exercices de type "fonction" (sans `main`) sont compilés avec `-c` + testés via le tester dédié
- Pour `ft_list_size` et `ft_list_foreach` : **ne soumets pas** `ft_list.h` (fourni par l'examen)
- Pour `sort_list` : **ne soumets pas** `list.h` (fourni par l'examen, le sujet le précise)
- Pour `flood_fill` : **soumets** `t_point.h` (listé dans `Expected files: *.c, *.h`)
- `traces/` contient le détail de chaque test raté : consulte-le pour débugger

## Bugs connus et corrections apportées

| Bug | Fix |
|---|---|
| `(newline only)` lu comme texte littéral dans les exemples | Converti en `"\n"` dans `parse_examples()` |
| `expected_parts` vide donnait `""` au lieu de `"\n"` | Toujours `+ "\n"` en fin de jointure |
| `$>` sans argument causait un IndexError | `parts = [binary]` si la liste est vide |
| Fonctions sans exemples jamais testées | Intégration des testers `exams/.tester/` dans `grademe` |
| Headers manquants lors de la compilation (`-I` absent) | `-I render/ -I exams/.tester/` dans toutes les commandes `cc` |
