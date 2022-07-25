OpenPattern
===========

**F. Métivier**

Sommaire
--------

-  `Introduction <##introduction>`__

   -  `Ques aquo <###ques-aquo>`__
   -  `Organisation <###organisation>`__
   -  `Principe de fonctionnement <###principe-de-fonctionnement>`__

-  `Tutoriel <##tutoriel>`__

   -  `Le patron de base <###le-patron-de-base>`__
   -  `La jupe <###la-jupe>`__
   -  `Le pantalon <###le-pantalon>`__
   -  `Le Body <###le-body>`__
   -  `Les transformations <###les-transformations>`__

-  `OpenPattern from
   scratch <##pour-aller-plus-loin:Openpattern-from-scratch>`__

   -  `Dessine-moi un carré <###dessines-moi-un-carre>`__
   -  `Dessine-moi une pince <###dessine-moi-une-pince>`__
   -  `Les annotations: légendes, marques et
      commentaires <###annotations>`__
   -  `Les courbes et le pistolet <###les-courbes-et-le-pistolet>`__
   -  `Utiliser des sous-patrons <###utiliser-des-sous-patrons>`__
   -  `Utiliser des mensurations <###utiliser-des-mensurations>`__

-  `Pour aller plus loin <##pour-aller-plus-loin>`__

Introduction
------------

### Ques aquo ?
---------------

OpenPattern est une librairie python, orientée objet, dont l’objectif
est de permettre le tracé de patrons, en particulier de vêtements, à
l’échelle 1:1 et leur sauvegarde au format pdf, svg ou tout format
compatible avec la libraire matplotlib. Les patrons ainsi construits
peuvent soit être directement imprimés pour utilisation soit être repris
dans un logiciel de dessin comme Inkscape.

OpenPattern offre la possibilité de créer des patrons «from scratch»,
d’utiliser des librairies de patrons existants (patrons de bases
notamment) et de les reprendre pour les adapter et les transformer (et
de les intégrer à la librairie !).

Les patrons peuvent être construits «sur-mesure» à partir d’un ensemble
de mesures effectuées sur le corps d’une personne particulière (j’ai
créé OpenPattern pour dessiner des vêtements pour ma famille), ou
construits à partir de mesures de prêt à porter classique.

Les sources que j’ai utilisées pour tracer les patrons proviennent
d’ouvrage de patronage classiques. Ces ouvrages, destinés au couturiers
amateurs ou aux étudiants d’écoles de modes, décrivent les techniques de
réalisation de ce que l’on nomme la coupe à plat c’est-à-dire la manière
de projeter et tracer sur un plan (le papier puis le tissus) une forme
géométrique 3D (le vêtement fini après couture).


Organisation
~~~~~~~~~~~~

Un patron est une série de courbes et de lignes qui dessine le contour
des pièces qu’il faut découper et coudre pour créer un vêtement. à ces
courbe s’ajoutent des points de contrôles. Dans OpenPattern les lignes
et courbes sont enregistrées dans les listes, les points de contrôle
dans des dictionnaires.

OpenPattern est organisée autour de classes qui permettent la création
de ces points et courbes et qui héritent les unes des autres. Cette
structure présente l’avantage de coller aux techniques de coupe. En
effet une chemise, une veste ou un gilet sont des adaptations d’un body,
une robe dérive de l’assemblage d’une jupe et d’un body, enfin les jupes
et les pantalons dérivent de formes génériques dites de bases (jupe de
base, pantalon de base).

OpenPattern présente pour l’instant deux niveaux d’héritage.

-  La classe parente ``Pattern`` : C’est la classe générale qui définit
   ce qu’est un patron et les méthodes permettant de le dessiner et de
   le manipuler.

-  Les classes de bases dérivées de Pattern:
   ``Basic_Bodice,     Basic_Trousers, Cuffs, Collars``.

-  Les classes dérivées des classes de base: shirt, pyjamas qui héritent
   de ``Basic_Bodice`` ou de ``Basic_Trousers``.

Les patrons font appels à une classe ``Point`` qui permet de définir un
point de patronage avec sa position et ses propriétés. Cette classe
redéfinit les opérations d’addition et offre diverses manipulations
comme la rotation. L’intérêt ici est d’avoir un objet flexible qui
permette de partir d’un patron de base et de l’altérer.

Enfin un patron se construit à partir de mesures corporelles. Celles-ci
sont stockées dans une base de données sqlite3 contenue dans le fichier
``measurement.db``. Cette base contient toute une série de mesures
standards en provenance des différents livres cités plus haut et peut
aussi contenir les mesures spécifique que vous prendrez sur vos proches.

Principe de fonctionnement
~~~~~~~~~~~~~~~~~~~~~~~~~~

Pour dessiner un patron il faut

1. créer une instance de la classe correspondante,

2. appeler différentes méthodes d’altération ou de modification,

3. dessiner et, au besoin, sauvegarder le patron.

Le dessin du patron peut aussi directement se faire à partir des classes
``Pattern`` et ``Point`` comme nous le verrons plus loin dans la suite
de ce document. Pour débuter cependant je vous recommande d’utiliser les
patrons existants de la librairie. J’ajouterai des patrons au fur et à
mesure de mon temps libre.

Tutoriel
--------

Le patron de base
~~~~~~~~~~~~~~~~~

Ce tutoriel montre comment utiliser les classes permettant de tracer des
patrons complets à partir de mesures moyennes (un 38 français par
exemple) ou à partir de mesures prises sur la personne de votre choix.
Différentes classes permettent de faire ce premier travail, le plus
difficile parfois, qui consiste à tracer une base de patron: base de
pantalon, base de jupes, base de buste et de manche. À partir de ces
patrons il est alors possible soit d’utiliser directement la base (pour
une jupe droite ou un pantalon basique par exemple) soit de les
«altérer» ou «transformer».

:warning: Dans tous les scripts du tutoriel je considère que la base de
données ``measurements.db`` est dans le même répertoire que le script
principal.

Le body
~~~~~~~

Le script suivant montre le principe d’utilisation de la librairie
OpenPattern en prenant l’exemple d’un Body. Nous allons tracer et
enregistrer un patron de Body de femme sans pinces en 36 (taille
française) selon la méthode de Gilewska.

.. code:: python

   import matplotlib.pyplot as plt
   import OpenPattern as OP

   # Creation de l'instance
   p = OP.Basic_Bodice(
     pname = "W36G",
     gender = 'w',
     style = 'Gilewska'
     )

   # appel de la fonction de dessin
   p.draw()

   plt.show()

C’est simple non ? On obtient alors la figure 1 enregistrée par defaut à
l’échelle 1:1 dans un fichier pdf.

.. raw:: html

   <figure>

Figure 1: Basic bodice with darts.

.. raw:: html

   </figure>

Les différentes options sont passées dans les arguments des différentes
méthodes de classe (``draw_bodice``) ou lors des instanciations de
classe (``Basic_Bodice`` dans cet exemple).

La liste des bases de body actuellement disponibles est donnée
ci-dessous Nous allons dans la suite voir en détail chacune des bases et
leurs options.

========== ====== ====== =======
Style      Femmes Hommes Enfants
========== ====== ====== =======
Chiappetta        x      2-16
Donnanno   x      x
Gilewska   x      x
========== ====== ====== =======

Notons que pour ce qui concerne les hommes, les body de Gilewska et
Donnanno sont en fait des chemises simples sans les manches. Les manches
justement font partie de la classe body car elles sont calculées à
partir des profondeurs d’emmanchures mesurées sur les body.

La jupe
~~~~~~~

Le script suivant montre comment créer une jupe de base (ou jupe crayon
ou encore fuseau ou pencil en anglais)

.. code:: python

   import OpenPattern as OP
   p = OP.Basic_Skirt(
     pname="W6C",
     style='Chiappetta',
     gender = 'G',
     ease=8,
     curves=False
     )

   p.draw()

.. raw:: html

   <figure>

Figure 2: jupe fuseau (ou jupe de base) d’une fille de 6 ans. Modèle de
J. Chiappetta.

.. raw:: html

   </figure>

Les arguments à l’instanciation de la classe sont les suivants

+----------+--------------+--------------------+-------------------+
| Argument | type         | Définition         | valeur par défaut |
+==========+==============+====================+===================+
| pname    | str          | code de la taille  | W6C               |
+----------+--------------+--------------------+-------------------+
| style    | str          | modèle utilisé     | Chiappetta        |
+----------+--------------+--------------------+-------------------+
| gender   | str          | genre              | G                 |
+----------+--------------+--------------------+-------------------+
| ease     | int ou float | aisance à          | 8                 |
|          |              | appliquer au       |                   |
|          |              | patron             |                   |
+----------+--------------+--------------------+-------------------+
| curves   | boolean      | doit on oui ou non | False             |
|          |              | dessiner une       |                   |
|          |              | taille courbe      |                   |
+----------+--------------+--------------------+-------------------+
| kwargs   | dic          | arguments          | vide              |
|          |              | supplémentaires    |                   |
|          |              | comme dbPATH       |                   |
+----------+--------------+--------------------+-------------------+

Notons que chez Donnanno la jupe crayon est symétrique alors que chez
Gilewska elle est légèrement asymétrique avec un demi-devant plus large
de 1cm que le demi-dos. Donnanno Traite cette asymétrie comme une
transformation et on la retrouvera dans la jupe «shifted-side-seams» par
exemple. Chez Chiappetta la jupe crayon fille est symétrique quel que
soit l’âge.

Le pantalon
~~~~~~~~~~~

Pour créer un pantalon avec pinces on utilise la classe
``Basic_Trousers``

.. code:: python

   import OpenPattern as OP
   pans = OP.Basic_Trousers(
       pname="M44D",
       gender="m",
       style="Donnanno",
       darts=True,
       dbPATH="../measurements/",
       figPATH="../docs/samplePatterns/",
       frmt="svg",
   )
   # pans.Donnanno_add_darts()

   pans.draw_basic_trousers(dic={"Pattern": "Basic trousers with dart"}, save=True)

.. raw:: html

   <figure>

Figure 3: Pantalon à pinces selon le modèle d’A. Donnanno.

.. raw:: html

   </figure>

À l’heure actuelle seul le style Donnanno est implémenté pour les
pantalons. Si vous choisissez un autre style un message s’affichera
indiquant l’indisponibilité du style demandé et OpenPattern tentera de
tracer un pantalon selon le style Donnano.

### Les Transformations

Aux trois classes de bases s’ajoutent des classes accessoires pour les
manchettes et les cols et en cours (et que je ne mets pas) des classes
pour les gilets et pour les chemises et pour les robes. Ces classes sont
en cours de constitution et je les complète quand j’ai du temps !

-  Waistband

-  Cuffs

-  Placket

-  Collars

-  Jupe

   -  Culotte

   -  Skirt transform (Shifted side seam, A line, Flared A Line)

-  Trousers

   -  Bermudas

   -  Flared pants

   -  Pants block

.. code:: python

   Cuffs(pname = "sophie", gender = 'w', style = 'Donnanno', age = 12, cuff_style = 'Simple',\
     overlap = 2, width = 5, ease = 3 )
   Placket(pname = "sophie", gender = 'w', placket_style = 'Simple', slit_length = 10)
   Collars(pname="sophie", gender='w', style='Gilewska', collar_style = 'Officer',\
     overlap=0, collar_height=3)

OpenPattern from scratch
------------------------

Dessine-moi un carré
~~~~~~~~~~~~~~~~~~~~

Le script suivant montre comment dessiner un carré (de tissus :=)). les
opérations consistent en

1. la création du patron par la création d’une instance de la classe
   pattern,

2. la création de quatre points,

3. l’ajout de ces points au patrons,

4. la définition de l’ordre dans lequel les tracés doivent être faits,

5. enfin la représentation graphique.

.. code:: python

   #!/usr/bin/env python3
   # -*- coding: utf-8 -*-

   import sys
   sys.path.append('/home/metivier/Nextcloud/Personnel/couture/OpenPattern')

   import matplotlib.pyplot as plt
   import OpenPattern as OP
   import numpy as np

   # 1 create a pattern instance
   myPattern = OP.Pattern()

   # 2 define points
   A = OP.Point([0,0])
   B = OP.Point([10,0])
   C = OP.Point([10,10])
   D = OP.Point([0,10])

   # 3 add them to your pattern
   myPattern.add_point('A',A)
   myPattern.add_point('B',B)
   myPattern.add_point('C',C)
   myPattern.add_point('D',D)

   # 4 prepare drawing
   myPattern.Front_vertices = [A.pos(), B.pos(), C.pos(), D.pos(), A.pos()]

   # 5 draw
   myPattern.draw(save=True, fname='simple_scripts_0')
   plt.show()

   #done !

la figure suivante montre le résultat.

.. figure:: ./samplePatterns/simple_scripts_0__FullSize.svg
   :alt: Mon beau carré

   Mon beau carré

Le patron du carré est constitué d’un carré grisé délimité par quatres
segments dont les quatre sommets sont marqués par un point rouge avec
son nom. Le carroyage, qui donnent l’échelle et permet les raccords,
fait 1 cm quand on imprime le patron en taille réelle. Le patron est
enfin entouré d’une bande de 5cm de tous les côtés. Vous noterez qu’une
échelle apparaît dans cette bande. Elle est automatiquement ajoutée avec
l’option ``save = True`` c’est à dire quand votre patron finit mérite
impression. Cela vous permettra de vérifier rapidement que votre patron
est bien à l’échelle [3]_. Vous l’aurez donc compris l’unité de base
d’OpenPattern est le centimètre (ah bon pourquoi ?).

Vous noterez en ligne (27) que l’ordre du dessin du polygone est définit
A-B-C-D-A. On aurait pu mettre A-D-C-B-A pour un résultat identique à
première vue. On parle ici d’un polygone fermé. l’ordre indiqué va
permettre à la librairie graphique de tracer les segments dans l’ordre
souhaité. On verra plus tard, à mesure que la forme du patron et donc de
son contour se complexifie que cet ordre est important et conditionne la
façon dont on incluera une pince ou tracera une courbe.

Dessine-moi une pince
~~~~~~~~~~~~~~~~~~~~~

Imaginons que nous allons transformer notre carré un peu pour en faire
un demi-trapèze et lui ajouter une pince (Attention ça va faire jupe !).
Les étapes sont les mêmes l’ajout de la pince se faisant évidemment
après la définition des points du segment impacté par cet ajout.

.. code:: python

   #!/usr/bin/env python3
   # -*- coding: utf-8 -*-

   import sys
   sys.path.append('/home/metivier/Nextcloud/Personnel/couture/OpenPattern')

   import matplotlib.pyplot as plt
   import OpenPattern as OP
   import numpy as np

   # create a pattern instance
   myPattern = OP.Pattern()

   # define points
   A = OP.Point([0,0])
   B = OP.Point([20,0])
   C = OP.Point([20,15])
   D = OP.Point([5,15])

   # add a dart between C and D
   E = OP.Point([12.5,8])
   I1,I2 = myPattern.add_dart(E,C,D,2)

   # add the points to your pattern
   myPattern.add_point('A',A)
   myPattern.add_point('B',B)
   myPattern.add_point('C',C)
   myPattern.add_point('D',D)
   myPattern.add_point('E',E)
   myPattern.add_point('I1',I1)
   myPattern.add_point('I2',I2)

   # prepare drawing
   myPattern.Front_vertices = [A.pos(), B.pos(), C.pos(), I2.pos(), E.pos(),\
       I1.pos(), D.pos(), A.pos()]

   # draw
   myPattern.draw(save=True, fname='simple_scripts_1')
   plt.show()

   # done !

.. figure:: ./samplePatterns/simple_scripts_1__FullSize.svg
   :alt: Mon beau trapèze

   Mon beau trapèze

Comme on le voit ici la création de la pince se fait en deux étapes. On
définit la position du sommet de la pince (ligne 21) puis on appelle la
fonction ``add_dart`` en lui passant quatre arguments (ligne 22; il y en
a plus que nous verrons plus tard) le sommet, les deux points
définissant le segment qui doit être pincé et la largeur de la pince. la
fonction renvoie la position des deux points qui, avec le sommet,
constitueront la pince sur le patron. Il ne reste alors plus qu’à
intercaler les points de pince lors de la définition du trajet du tracé.
La figure `3.6 <#fig:trapeze>`__ montre le résultat. Comment ça elle ne
vous plait pas ma jupe ?

Les annotations: légendes, marques et commentaires
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Un patron vient souvent accompagné de commentaires et de signes
particulier comme l’indication du droit fil, les pliures et les crans de
montages. Il est possible de les insérer sur votre patron à l’aide des
commandes correspondantes comme le montre le script suivant et la figure
qui l’accompagne (les commandes sont insérées dans le script précédent
avant la commande ``draw``).

.. code:: python

   # add legends
   myPattern.set_grainline(OP.Point([8,10]), 8, -np.pi/2)
   myPattern.set_fold_line(C-[0,2], B+[0,2],'right')
   myPattern.add_comment(OP.Point([12.5,15.5]),'TOP',0)
   myPattern.add_comment(OP.Point([10,-0.5,]),'BOTTOM',0)


   a = 70
   myPattern.add_comment(OP.Point([2.8,8,]),'VV',a*np.pi/180) # workaround for notches

.. figure:: ./samplePatterns/simple_scripts_2__FullSize.svg
   :alt: Mon beau trapèze et ses annotations

   Mon beau trapèze et ses annotations

On notera au passage qu’à l’heure actuelle un cran de montage se place
comme un commentaire constitué de V en série.

Les courbes et le pistolet
~~~~~~~~~~~~~~~~~~~~~~~~~~

Bien arrondissons les angles. Une jupe ce n’est pas juste un tour de
taille mais aussi un tour de hanches et un arrondi sur le côté qui
permet un passage doux de la taille à la hanche justement. Nous verrons
à la section suivante l’utilisation des mensurations mais pour l’heure
ajoutons une hanche «au hasard» et jouons sur la courbe latérale afin de
comprendre de quoi il retourne.

.. code:: python

   #!/usr/bin/env python3
   # -*- coding: utf-8 -*-

   import sys
   sys.path.append('/home/metivier/Nextcloud/Personnel/couture/OpenPattern')

   import matplotlib.pyplot as plt
   import OpenPattern as OP
   import numpy as np

   # create a pattern instance
   myPattern = OP.Pattern()

   # define points
   A = OP.Point([0,0])
   B = OP.Point([20,0])
   C = OP.Point([20,15])
   D = OP.Point([5,15])

   # add a dart between C and D
   E = OP.Point([12.5,8])
   I1,I2 = myPattern.add_dart(E,C,D,2)

   # add the hip point somewhere between A and D
   H = OP.Point([2,10])

   # draw a curved fit between DHA
   # beware that the order of the points is important !
   curve_distance, curve_points = myPattern.pistolet([D,H,A],tot=True)

   # add the points to your pattern
   myPattern.add_point('A',A)
   myPattern.add_point('B',B)
   myPattern.add_point('C',C)
   myPattern.add_point('D',D)
   myPattern.add_point('E',E)
   myPattern.add_point('I1',I1)
   myPattern.add_point('I2',I2)
   myPattern.add_point('H',H)
   #prepare drawing
   # organize vertices
   myPattern.Front_vertices = [A.pos(), B.pos(), C.pos(), I2.pos(), E.pos(),\
       I1.pos(), D.pos()] + curve_points + [A.pos()]

   # add legends
   myPattern.set_grainline(OP.Point([8,10]), 8, -np.pi/2)
   myPattern.set_fold_line(C-[0,2], B+[0,2],'right')
   myPattern.add_comment(OP.Point([12.5,15.5]),'TOP',0)
   myPattern.add_comment(OP.Point([10,-0.5,]),'BOTTOM',0)


   a = 70
   # workaround for notches
   myPattern.add_comment(OP.Point([2.8,8,]),'VV',a*np.pi/180)
   # draw
   myPattern.draw(save=True, fname='simple_scripts_2-2')
   plt.show()

   #done !

.. figure:: ./samplePatterns/simple_scripts_2-2__FullSize.svg
   :alt: Ma belle jupe

   Ma belle jupe

Les lignes nouvelles sont les 25,29,39 et 42. La 25 donne la déclaration
du point de hanche H (hip en anglais). La 39 déclare ce point en
l’ajoutant au dictionnaire de points. Ces deux instructions ont déjà été
vues. La nouveauté est dans la ligne 39. On appelle la méthode
``pistolet`` de l’objet ``pattern``. Cette méthode va tracer une courbe
passant par les trois points D,H,A. l’ordre est important car la courbe
est en fait approximée par une succession de 30 points qui sont renvoyés
par le programme sous la forme d’une liste ici curve_points. Le premier
argument retourné correspond à la distance cumulée le long de la courbe
et est surtout utile pour les calculs de manches. nos points iront donc
de D à A en passant par H. cet ordre correspond à l’ordre dans lequel
est défini le polygone du pourtour de la jupe (rappelez-vous ce que nous
avons écrit lors de l’établissement de notre premier patron)). Ce
dernier est définit en ligne 42 où l’on voit la façon dont on introduit
la courbe

Notons qu’il faut au moins trois points pour tracer une courbe et
l’ordre de la courbe est au maximum egal au nombre de points moins 1.
Ici l’ordre sera de 3-1 = 2 au maximum. Ces courbes ne sont pas de
simples polynomes mais peuvent prendre deux formes.

1. Des clothoïdes ou courbes d’Euler ou encore «French curves» des
   pistolets traditionnels. Elles ne sont utilisables aujourd’hui dans
   OpenPattern que pour ajuster trois points et servent donc pour les
   emmanchures et les cols. La fonction pour utiliser le pistolet
   traditionnel est ``True_pistolet``.

2. Des b-splines qui permettent de remplacer de façon souvent très
   satisfaisante les clotoïdes. De façon générale les splines d’ordre 2
   suffisent pour tracer les pinces de côté des jupes ou les courbes de
   tailles, les splines d’ordre 3 sont nécessaires pour les têtes de
   manches qui présentent des points d’inflexions et certaines courbes
   de pantalon. Les splines d’ordre supérieur sont à peu de choses près
   inutiles en coupe à plat. La méthode pour utiliser des b-spline est
   ``pistolet``.

Utiliser des sous-patrons
~~~~~~~~~~~~~~~~~~~~~~~~~

Il est fréquent de créer un patron à partir de plusieurs bases
différentes, buste et pantalon pour les salopettes par, buste et jupe
pour certaines robes, ou encore buste, manche, col et manchette pour une
chemise [4]_.

la classe ``pattern`` peut contenir d’autres ``pattern`` qui sont
enregistrées dans la liste de patrons ``pattern_list``. Nous allons
reprendre notre patron de jupe et le copier trois fois en utilisant des
propriétés de translation et de rotation et de copie de la classe
``pattern``.

.. code:: python

   #!/usr/bin/env python3
   # -*- coding: utf-8 -*-

   import sys
   sys.path.append('/home/metivier/Nextcloud/Personnel/couture/OpenPattern')

   import matplotlib.pyplot as plt
   import OpenPattern as OP
   import numpy as np

   # create a pattern instance
   myPattern = OP.Pattern()

   # define points
   A = OP.Point([0,0])
   B = OP.Point([20,0])
   C = OP.Point([20,15])
   D = OP.Point([5,15])

   # add a dart between C and D
   E = OP.Point([12.5,8])
   I1,I2 = myPattern.add_dart(E,C,D,2)

   # add the points to your pattern
   myPattern.add_point('A',A)
   myPattern.add_point('B',B)
   myPattern.add_point('C',C)
   myPattern.add_point('D',D)
   myPattern.add_point('E',E)
   myPattern.add_point('I1',I1)
   myPattern.add_point('I2',I2)

   # prepare drawing
   # organize vertices
   myPattern.Front_vertices = [A.pos(), B.pos(), C.pos(), I2.pos(), E.pos(),\
       I1.pos(), D.pos(), A.pos()]

   # add legends
   myPattern.set_grainline(OP.Point([8,10]), 8, -np.pi/2)
   myPattern.set_fold_line(C-[0,2], B+[0,2],'right')
   myPattern.add_comment(OP.Point([12.5,15.5]),'TOP',0)
   myPattern.add_comment(OP.Point([10,-0.5,]),'BOTTOM',0)


   a = 70
   myPattern.add_comment(OP.Point([2.8,8,]),'VV',a*np.pi/180) # workaround for notches

   # draw
   # here comes the new part

   # copy and translate/rotate  myPattern
   # then add the new pattern to myPattern list of patterns
   P2 = myPattern.copy()
   P2.translate(30,0)
   myPattern.add_pattern(P2)

   P3 = myPattern.copy()
   P3.translate(0,30)
   P3.rotate(P3.Front_dic['E'].copy(),np.pi/2)
   myPattern.add_pattern(P3)

   P4 = myPattern.copy()
   P4.rotate(P4.Front_dic['A'].copy(), np.pi/4)
   P4.translate(35,30)
   myPattern.add_pattern(P4)

   # draw the subpatterns onf fig,ax
   myPattern.draw_subpatterns(overlay = True)
   # in the end draw mypattern on top of it
   myPattern.draw(save=True, fname='simple_scripts_3')

   plt.show()

   # done !

.. figure:: ./samplePatterns/simple_scripts_3__FullSize.svg
   :alt: Patron composite: mon beau trapèze et ses trois avatars

   Patron composite: mon beau trapèze et ses trois avatars

La partie qui nous intéresse ici débute à la ligne 47. Il s’agit de
copier le patron de départ dans P2, P3 et P4 puis de le translater ou
lui faire faire une rotation par rapport à un de ses points. Enfin le
patron est ajouter à la liste de sous-patrons de myPattern. Pour le
dessin on commence par dessiner les sous patrons sur une même figure
puis on dessine le patron principal et on ajoute les légendes. Enfin
lors du dessin de sous-patrons vous pouvez activer l’overlay qui les
dessine avec un remplissage plus léger dans le but de pouvoir dessiner
les altérations par dessus (ou dessous) ultérieurement dans la teinte de
gris classique.

Utiliser des mensurations
~~~~~~~~~~~~~~~~~~~~~~~~~

*Bespoke my dear !* l’intérêt de la classe ``pattern`` c’est qu’elle
peut faire appel à des mensurations c’est à dire un ensemble de mesures
corporelles. Il en existe deux types. Les mesures standards
correspondent à des moyennes statistiques sur une population d’une
certaine taille ou d’un certain âge et d’un sexe donné. Elles varient
avec le temps et suivant les auteurs car les populations à l’origine de
ces jeux de données varient elles aussi. Les mesures individuelles (ou
sur-mesure ou encore bespoke) correspondent aux mesures prises sur une
personne précise. Elles ne correspondent qu’à elle et n’ont aucune
utilité pour les autres mais elles correspondent au mieux à cette
personne. En utilisant des mensurations standards ou sur-mesure on peut
ainsi adapter les patrons pour un publique divers ou ciblé.

Les mesures sont enregistrées dans une base sqlite3 à laquelle accède la
classe ``pattern``. Lors de la création de l’objet patron on peut
appeler une des mesures enregistrées dans la base. Par défaut la classe
est instanciée en chargeant les mensurations féminine de 38 données par
`Gilewska <#Gilewska1>`__. Ces mensurations sont chargées dans un
dictionnaire nommé ``m``.

Maintenant que vous savez tout faire le plus simple consiste à faire une
vrai jupe. Nous allons donc tracer le patron d’une demi-jupe avant d’une
fille de 8 ans selon la méthode de `Jacqueline
Chiappetta <#Chiappetta1999>`__.

.. code:: python

   #!/usr/bin/env python3
   # -*- coding: utf-8 -*-

   import sys
   sys.path.append('/home/metivier/Nextcloud/Personnel/couture/OpenPattern')

   import matplotlib.pyplot as plt
   import OpenPattern as OP
   import numpy as np

   # create a pattern instance
   # mfs = my first skirt
   # W8C  = Women / 8 year / Chiappetta
   mfs = OP.Pattern('W8C')

   # size of the dart and ease to be applied
   pince = 7.25
   ease = 8

   # basic points
   # note the way measurements are called
   A = OP.Point([0,mfs.m["hauteur_taille_genou"]-4])
   B = A + OP.Point([(mfs.m["tour_bassin"]+ ease)/2,0])
   C = OP.Point([0,0])
   D = C + OP.Point([(mfs.m["tour_bassin"]+ ease)/2,0])

   A1 = A + OP.Point([0,-mfs.m["hauteur_bassin"]])
   B1 = A1 + OP.Point([(mfs.m["tour_bassin"]+ ease)/2,0])

   A2 = A + OP.Point([0,-1])
   B2 = B +OP.Point([0,-0.5])

   F = mfs.middle(A, B)
   E = mfs.middle(C, D)

   G = A + OP.Point([mfs.m["tour_taille"]/4  + 2, 0])
   H = B + OP.Point([-mfs.m["tour_taille"]/4  - 2, 0])

   # we need two control points for the french curve because we need at lease three
   # add one point between A1 and B1
   C1 = mfs.middle(A1, B1)
   # add a second just upp by one cm to control the tangents
   C2 = C1 + OP.Point([0,-1])
   # get the curves
   points_skirt_front = [H, C1, C2]
   dbskirt_f, skirt_front_side = mfs.pistolet(points_skirt_front, 2, tot = True)
   points_skirt_back = [G, C1, C2]
   dbskirt_b, skirt_back_side = mfs.pistolet(points_skirt_back, 2, tot = True)

   # back dart
   dart1 = A + OP.Point([mfs.distance(A, G)/2,- pince])
   I1,I2 = mfs.add_dart(dart1, A2, G, 2)
   # front dart
   dart2 = B + OP.Point([-mfs.distance(B, H)/2,- pince])
   I3, I4 = mfs.add_dart(dart2, B2, H, 2)

   #dics and lists
   key=['A', 'A1','A2',  'dart1', 'G','C']
   val=[A,A1,A2,dart1,G,C]

   for i in range(len(key)): # add points to the dictionnary
       mfs.add_point(key[i], val[i], dic='back')


   key=['B', 'B1', 'B2', 'dart2', 'H','F','E','D']
   val=[B,B1,B2,dart2,H,F,E,D]

   for i in range(len(key)): # add points to the dictionnary
       mfs.add_point(key[i], val[i], dic='front')

   mfs.Back_vertices = [[A2.pos(), I1.pos(), dart1.pos(), I2.pos(), G.pos()]\
       + skirt_back_side + [E.pos(), C.pos()]]
   mfs.Front_vertices = [[B2.pos(), I4.pos(), dart2.pos(), I3.pos(), H.pos()]\
       + skirt_front_side + [E.pos(), D.pos()]]


   # add legends
   mfs.set_grainline(OP.Point([8,15]), 8, -np.pi/2)
   mfs.set_fold_line(A1-[0,2], C+[0,2],'left')
   mfs.set_fold_line(B1-[0,2], D+[0,2],'right')
   mfs.add_labelled_line(A,B, 'WAIST LINE', 't')
   mfs.add_labelled_line(A1,B1, 'HIP LINE', 't')
   mfs.add_comment(mfs.middle(C,E)+[0,2],'BACK',0)
   mfs.add_comment(mfs.middle(E,D)+[0,2],'FRONT',0)

   # draw  the pattern
   mfs.draw(save=True, fname='simple_scripts_4')
   plt.show()

   # done !

.. figure:: ./samplePatterns/simple_scripts_4__FullSize.svg
   :alt: Jupe droite, 8 ans, avec pinces, méthode de Jacqueline
   Chiappetta

   Jupe droite, 8 ans, avec pinces, méthode de Jacqueline Chiappetta

Quelques commentaires s’imposent. De façon générale et même si de
nombreuses variations existent les patrons de vêtements sont présentés
avec une partie frontale et une partie dorsale. Notre jupe aura donc une
patron pour le devant (front) et le dos (back). Ceci explique la
présence de deux dicionnaires et de deux listes de points pour le
polygone de chacun des élements du patron (lignes 55 à 72).

Notez la façon dont on appel les mesures
``mfs.m["hauteur_taille_genou"]`` par exemple qui renvoie la hauteur
taille-genou correspondant à la taille appelée lors de la création du
patron ``mfs``. La liste des mesures disponibles en fonction des tailles
et des sources est discutée plus en détail au §\ `4.1 <#par:tailles>`__

Un vêtement est dessiné avec une aisance (ease) qui doit être donnée en
début de dessin. Ici on prend une aisance de 8cm pour l’ensemble du
patron (17). La profondeur de pince dépend souvent aussi de la taille et
de l’âge du modèle. Pour 8 ans chez Chiappetta [@Chiappetta1999] on a
une pince de 7.25 cm (16). Les lignes de 19 à 35 permettent de tracer
les points principaux du tracé de la jupe. Les lignes 39 et 41
permettent de créer deux points qui n’apparaîtront pas mais sont
important. il s’agit de points de contrôle pour le tracé de la courbe du
côté. En effet la courbe va de la ligne de taille à la ligne de hanche.
Chiappetta ne prend pas la peine de dire comment faire car avec un
pistolet c’est évident (essayez pour voir et vous comprendrez). Par
contre pour un spline et de façon générale en informatique il faut tout
expliquer au programme qui ne fait que ce qu’on lui dit de faire (ce
n’est pas un réseau de neurones !). Il faut donc définir le point milieu
de la ligne de hanche (39) puis un point situé 1 cm au dessus qui
permettra un tombé vertical de la courbe au point de hanches (41). Ces
deux points ajoutés au point de taille H ou G suffisent à tracer une
courbe pour le demi-devant et le demi-dos (43-46). La suite ne pose
aucun problème maintenant: ajout des pinces, enregistrement des points
et des positions qui définissent chaque polygone de demi-jupe, ajout des
commentaires et enfin dessin ! Ce patron peut-être imprimé en taille
réelle et directement utilisé pour une jupe droite d’une fille de 8 ans.
Manque juste la ceinture que vous pourriez réaliser très facilement
maintenant (on y viendra plus tard rassurez-vous) !

Charger des mesures dans la base
--------------------------------

Pour aller plus loin
--------------------

Les tailles
~~~~~~~~~~~

Le tableau suivant recense l’état des mesures que contient la base sql
d’OpenPattern.

========== ======= =========== =========== ======= ===============
Source     Genre   Taille min. Taille max. Mesures example de Code
========== ======= =========== =========== ======= ===============
Gilewska   Femmes  34          48          25      W34G
Gilewska   Hommes  36          54          24      M36G
Donnanno   Femmes  40          50          21      W40D
Donnanno   Hommes  44          54          19      M44D
Wargnier   Hommes  38          48          25      M38W
Chiappetta Filles  2 ans       16 ans      23      W3C
Chiappetta Garçons 6 ans       16 ans      20      G6C
Chiappetta Homme   36          50          22      M38mC
========== ======= =========== =========== ======= ===============

*Tailles disponibles dans la base measurements. Le code donné en exemple
correspond au code d’appel de la taille minimum.*

Notons que la distinction garçon, homme n’est pas anodine. En effet si
les effets de la puberté sur les filles sont connus et aboutissent
notamment à l’usage des pinces de buste et de taille, les patrons de
bases sans pinces ne changent pratiquement pas. Chez les hommes la
puberté produit une inversion de la forme du buste. Le tour de poitrine
d’un garçon est en effet plus petit que son tour de bassin à l’instar
d’une femme. De ce point de vue, important pour le dessin d’un patron,
le garçon et la fille sont de morphologies proches et plus proche de la
femme que de l’homme. La puberté inverse la situation chez l’homme dont
le tour de poitrine devient plus grand que son tour de bassin. Ce
changement influence de façon nette le traçage du patron masculin et ce
qu’on y projette dans tous les sens du terme même si de façon étonnante
ceci n’est jamais discuté.

Un conséquence de cela est qu’on aura probablement plutôt intérêt à
utiliser des modèles féminins pour dessiner le patron d’un homme dont le
bassin est plus large que sont tour de poitrine. L’effet sera
probablement meilleur qu’avec un patron masculin classique.

En entrant ces mesures et en commençant à les utiliser j’ai recensé pas
moin de 52 mesures différentes chez mes sources. La répartition de ces
différentes mesures en fonction des sources donne la mesure :joy: des
ennuis à venir. Chacun utilise un jeu de mesures communes mais brode en
ajoutant ou pas des mesures différentes. Cela posera problème par
exemple pour le tracé des épaules de l’homme qui présente des
incohérence suivant les auteurs ou autrices. De façon générale l’homme
est moins bien traité que la femme dans ces ouvrages (à l’exception des
garçons de Chiappetta), probablement à cause du marché restreint qu’il
représente et du moindre intérêt de son vestiraire (chemise, veste,
pantalon pour faire simple). Et de fait cela part dans tous les sens
chez les hommes... le plus gros écart sépare les stylistes qui mesurent
la largeur des épaules et ceux ou celles qui mesurent la longueur des
épaules. Quelques un.e.s mesurent les deux mais c’est plus rare. On
notera que les mesures type varient d’un livre à l’autre. Pas toujours
de mesure du tour de bras, du tour de mollet, du tour de cuisse.
Chiappetta différencie les tailles de chemises et les tailles de
pantalon (celle que je conserve ici), le drop associé (différence entre
demi tour de poitrine et demi tour de taille) et la stature (trois
hauteurs sont données 170,175 et 180 cm).

Enfin pour ne rien gâcher les correspondances de tailles varient d’un
pays à l’autre donc un 38 de Gilewska n’est pas un 38 de Donnanno...
Officiellement il faut rajouter 4 aux tailles italiennes pour retrouver,
approximativement, la taille française. Un 36 de Gilewska correspond
donc à un 40 de Donnanno. Sauf que dans les fait quand on compare les
valeurs on est plutôt sur une différence de 2 (un 38 Gilewska
correspondrait plutôt de mon point de vue à un 40 Donnanno).

========================== == == == == == === === ==
Mesure                     FG HG FD HD HW FiC GaC HC
========================== == == == == == === === ==
carrure_devant             X  X  X     X  X       X
carrure_dos                X  X  X     X  X   X   X
cheville_terre                   X        X   X   X
crane                                     X   X   X
ecart_poitrine             X     X
encolure_dos                     X
enfourchure                            X
entrejambe                    X        X
entrejambe_terre                              X   X
fourche                    X
genou_sol                                         X
genou_terre                                   X
hauteur_bassin             X  X  X  X  X  X
hauteur_carrure            X
hauteur_corps                          X          X
hauteur_coude              X  X     X     X   X
hauteur_cou_dessous_bras         X
hauteur_emmanchure         X
hauteur_petites_hanches    X
hauteur_poitrine           X
hauteur_taille_genou       X     X  X  X  X
hauteur_taille_terre             X     X
hauteur_tete                           X
largeur_bras                     X
largeur_encolure           X
largeur_epaule                X     X
largeur_secteur                     X
longueur_7cerv_enc                                X
longueur_col_devant        X                      X
longueur_col_dos           X                      X
longueur_devant            X  X  X  X  X  X
longueur_devant_7c                     X
longueur_dos               X  X  X  X  X  X   X   X
longueur_emmanchure_devant X        X             X
longueur_emmanchure_dos    X        X             X
longueur_epaule            X  X  X  X  X  X   X   X
longueur_manche            X  X  X  X  X  X   X   X
longueur_taille_terre      X  X     X     X
montant                    X  X  X  X  X  X   X   X
profondeur_emmanchure      X        X
profondeur_encolure_devant X
profondeur_encolure_dos    X
profondeur_poitrine              X
stature                          X  X
tour_abdomen                     X
tour_bassin                X  X  X  X  X  X   X   X
tour_bras                  X  X  X        X   X   X
tour_cheville              X     X        X   X   X
tour_cou                         X
tour_coude                       X
tour_cuisse                X  X  X     X          X
tour_encolure              X  X     X  X  X   X   X
tour_genou                 X     X        X   X   X
tour_jarret                            X
tour_mollet                            X  X   X   X
tour_petites_hanches       X
tour_poignet               X  X  X     X  X   X   X
tour_poitrine              X  X  X  X  X  X   X   X
tour_poitrine_haute              X
tour_taille                X  X  X  X  X  X   X   X
tour_tete                              X
========================== == == == == == === === ==

*Répartition des mesures par source*

Déplier un patron
~~~~~~~~~~~~~~~~~

Déplier un patron peut-être utile pour des transformations. En effet
très souvent les demi patrons de buste, de jupe et de robes sont au pli
afin d’éviter des coutures inesthétiques au milieu (devant et dos). Lors
des transformations par contre, comme pour transformer une jupe de base
en jupe portefeuille par exemple, il peut être utile de travailler sur
le patron déplié. La méthode ``unfold`` permet cela. Sur le principe on
fournit un axe AB de symétrie, et pour chaque point du patron on cherche
le point miroir. Ici cela est fait en deux temps: (1) projeter un point
:math:`O` du patron sur la droite :math:`(AB)` pour obtenir le point
:math:`M` et (2) chercher le point :math:`O'` qui se trouve à deux fois
la distance de projection soit

.. math:: \overrightarrow{OO'} = 2\overrightarrow{OM}.

Le script suivant montre comment procéder et la
figure `4.1 <#fig:unfold>`__ donne le résultat

.. code:: python

   #!/usr/bin/env python3
   # -*- coding: utf-8 -*-

   import sys
   sys.path.append('/home/metivier/Nextcloud/Personnel/couture/OpenPattern')

   import matplotlib.pyplot as plt
   import OpenPattern as OP
   import numpy as np

   # create a pattern instance
   P1 = OP.Pattern()

   # define points
   A = OP.Point([0,0])
   B = OP.Point([20,0])
   C = OP.Point([20,15])
   D = OP.Point([5,15])

   # add a dart between C and D
   E = OP.Point([12.5,8])
   I1,I2 = P1.add_dart(E,C,D,2)

   # add the points to your pattern
   P1.add_point('A',A)
   P1.add_point('B',B)
   P1.add_point('C',C)
   P1.add_point('D',D)
   P1.add_point('E',E)
   P1.add_point('I1',I1)
   P1.add_point('I2',I2)

   # prepare drawing
   P1.Front_vertices = [[A.pos(), B.pos(), C.pos(), I2.pos(), E.pos(),\
       I1.pos(), D.pos(), A.pos()]]

   #Mirror the pattern to unfold it
   du, vu = P1.unfold(P1.Front_dic,P1.Front_vertices[0],P1.Front_dic['C'],P1.Front_dic['B'])

   P1.Front_vertices.append(vu)
   for key,val in du.items():
       P1.add_point(key,val)


   # draw the unfolded pattern
   P1.draw(save=True, fname='simple_scripts_5')
   plt.show()

   # done !

.. figure:: ./samplePatterns/simple_scripts_5__FullSize.svg
   :alt: Mon beau trapèze déplié

   Mon beau trapèze déplié

Participer
----------

Ajouter des patrons
~~~~~~~~~~~~~~~~~~~

La façon la plus simple de participer est d’intégrer des patrons dans la
librairie. Il suffit de vous inspirer de la façon dont sont créés des
patrons existant pour savoir comment écrire le code. Il est important de
référencer l’origine du patron (s’agit-il d’un patron publié ou est-ce
votre création). Il faut ensuite vérifier que votre patron est
compatible avec le mesures existantes.

Ajouter des fonctionnalités
~~~~~~~~~~~~~~~~~~~~~~~~~~~

Plus compliqué. Il reste des dizaines de choses à faire comme par
exemple, pour celles et ceux qui le souhaite, intégrer une option
permettant le tracé des marges de couture. Je ne le fais pas d’abord par
choix — je les trace directement sur le tissus après avoir tracé le
patron —, mais il se trouve que cela simplifie pas mal l’écriture car
les marges ne sont pas une simple homothétie du patron fini.

Commentaires (pour moi surtout !)
---------------------------------

### Ligne d’épaule

Pour les femmes de style G, la construction des épaules repose sur des
angles fixes. Pour les hommes de style G, cela dépend des distances par
rapport à la ligne des épaules comme podonc ur le style D. Pourquoi ce
changement? Cela pose un problème car, si l’on suit les instructions,
l’épaule est plus longue que les mesures (si elles existent) et les
épaules avant et arrière n’ont pas la même longueur. Dans le cas où la
longueur d’épaule est donnée, la solution est alors d’ajuster la
longueur d’épaule à la longueur mesurée à laquelle la ligne d’épaule a
été établie (comme suggéré par Donnanno). J’ai donc ajouté un test pour
l’existence d’une mesure de la vraie longueur des épaules Si tel est le
cas, la longueur de l’épaule est ajustée pour s’adapter aux mesures.
Notons en outre que les largeurs d’épaules correspondent chez G homme si
on ne baisse pas l’épaule devant de 7cm mais de 5 (comme chez Donnanno).

Pour les adolescents (garçons) de style C, l’épaule repose sur deux
angles différents pour le dos (22 :math:`^ o`) et le devant (25
:math:`^ o`).

Emmanchure et col
~~~~~~~~~~~~~~~~~

à noter que, encore une fois, pour l’homme tout est un peu fait par
dessus la jambe. Ok des chemises des pantalons et des costumes c’est pas
folichon mais quand même !

Donnano: pour les femmes le buste de base présente un problème
d’ajustement car il ne fournit pas de points de contrôles. J’ai repris
ceux de Gilweska.

Pour l’homme: pas de buste de base j’en au créé un à partir de la
chemise de base. relativement simple à faire. Par contre problème
(toujours) pour les longueurs d’épaule. La largeur d’épaule est donnée
mais pas la longueur (qui d’ailleurs n’est que très rarement donnée pour
les hommes). or on demande la longueur d’épaule (j’adore le e.g. 17cm
mis dans l’exemple dont on ne sait pas d’où il sort)

Gilewska : pour le buste homme j’ai ajouté deux points de contrôle en
base de manche afin d’assurer la platitude d’emmanchure. Sinon les
spleen ne veulent pas faire comme le perroquet.

Chiappetta pour adolescents: (figure    ref fig: CB14) n’utilise qu’une
seule mesure de carrure celle du dos. Pour les adolescents de plus de 10
ans, elle récupère juste deux cm de carrure mesurés au dos pour le
devant. Le collier arrière a besoin d’un deuxième point de contrôle près
de la ligne de pliage pour assurer la planéité de la cannelure.

Pour l’enfant Chiapetta changer l’angle, la longueur des points de
contrôle et la carrure devant. de 2 à 8 ans les angles d’épaule devant
et derrière sont les même, les longueurs plus petites et la carrure
devant et dos sont les mêmes.

L’emmanchure et l’encolure sont faites avec des splines de second ordre.
J’ai fini par jouer sur le fit des splines et les points de contrôle. À
développer.

Bon mais comme d’hab Chiapetta ça à l’air un peu ringard sur les bords
mais ça marche tout seul. je pense que je vais investir dans les
bouquins adultes notamment pour l’homme...

Manches
~~~~~~~

Gilewska: Aucune indication pour le bas de manche de base il faut donc
se débrouiller seul avec le tour de poignet...

Les splines ici sont du troisième ordre car il y a un point d’inflexion.

De façon générale je trouve que les bustes hommes ne sont pas très
ressemblant aux dessins des livres et je suis dubitatif car le programme
reproduit exactement les instruction sauf quand c’est problématique de
façon évidente (genre les largeur d’épaules de Donnanno).

Cols
~~~~

Styles available from Gilewska men: Officer and OnePiece (for one piece
collar)

|Collar styles| |Collar styles|

Cuffs
-----

Styles availabel from Gilewska men : Simple and French

|Cuff styles| |Cuff styles|

Pantalons
~~~~~~~~~

Pants Block
^^^^^^^^^^^

Incohérence du modèle chez Donnanno. La mesure de la ceinture est

AV = Hip + 6.

Or la somme

ceinture avant + ceinture arriere = Hip +2.

Donanno indique qu’il faut séparer les patrons avant et arrière de 6cm
soit

ceinture avant + ceinture arriere + 6 = Hip +8 = AV,

d’où l’incohérence.

skirts
^^^^^^

jupe de base une pince. position de la pince.

Chiappetta: à mi-distance jusqu’à 12 ans. 2 pince au 1/3 et 2/3 de
distance pour 14 et 16 car l’écart entre taille est bassin est trop
grand pour être absorbé en une seule pince. Chiappetta rappelle qu’avant
10 ans on ne met que rarement les pinces car les jupes sont presque
systématiquement élastiquées. Est-ce encore vrai ?

Donnanno: à une distance d’1/2 bust point — non défini mais qu’on
imaginera être le téton— que je comprends comme le demi écart poitrine.

Gilewska: confirme l’utilisation du 1/2 écart poitrine. Si la différence
taille/bassin est trop importante alors Gilewska recommande deux pinces
devant une au 1/2 écart poitrine et une à mi distance entre la première
pince et la pince de côté (le côté de fait). utlise une pince de milieu
dos

la bande de taille chez Donnanno est donnée à 5cm

References
==========

Chiappetta, J., *Prêt à porter et sur mesure pour le bébé et l’enfant*,
La coupe à plat, 3, Presses du midi, 1998.

Chiappetta, J., *Prêt à porter et sur mesure pour l’homme*, La coupe
{`a} plat, 4, Presses du midi, 2000.

Donnanno, A. and Drudi, E.K., *How to make skirts, trousers and shirts
for women and men*, Fashion Patternmaking Techniques, 1, Promopress,
2005.

Donnanno, A. and Drudi, E.K., *How to make shirts, undergarments,
dresses and suits, waistcoats and jackets for women and men*, Fashion
Patternmaking Techniques, 3, Promopress, 2016.

Gilewska, T., *Coupe à plat les bases*, Le modélisme de mode, 1,
Eyrolles,2008

Gilewska, T., *Coupe à plat les transformations*, Le modélisme de mode,
2, Eyrolles,2008

Gilewska, T., *Montage et finition des vêtements*, Le modélisme de
mode,4, Eyrolles,2011

Gilewska, T., *Coupe à plat et montage homme*, Le modélisme de mode,5,
Eyrolles,2013

Wargnier, C. and Gonnet, I.\ *Le vêtement masculin: les bases du
vêtement de ville et de sport*, Become a Pattern Drafter Series, Esmod
Editions, 2012.

.. [1]
   Ces livres peuvent apparaitre un peu peu ringards de prime abord. Ne
   vous y fiez pas ! ok le dessin est vieillot et les modèles ultra
   classiques mais ils sont remarquables par la clareté des explications
   et leur reproductibilité. Ce sont mes préférés.

.. [2]
   Ces ouvrages présentent parfois des coquilles ou des imprécisions qui
   sont probablement corrigées par leurs auteurs quand elles ou ils
   enseignent.

.. [3]
   Normalement les carrés font 1cm de côté mais une requête d’un ami m’a
   fait ajouter cette échelle (pour être certain que tout va bien dirons
   nous).

.. [4]
   On verra cependant dans ce dernier cas que la manche est
   intrinsèquement liée au buste. Elle vient «après» le dessin du buste

.. |Collar styles| image:: ../patterns/collar_Gilewska_OnePiece_M44G_FullSize.pdf
   :width: 48.0%
.. |Collar styles| image:: ../patterns/collar_Gilewska_Officer_M44G_FullSize.pdf
   :width: 48.0%
.. |Cuff styles| image:: ../patterns/cuff_Gilewska_Simple_M44G_FullSize.pdf
   :width: 48.0%
.. |Cuff styles| image:: ../patterns/cuff_Gilewska_French_M44G_FullSize.pdf
   :width: 48.0%
