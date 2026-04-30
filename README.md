# Projet BMO - Gestion de centres de congrès

## Description du projet

L'application permet la gestion d'un ensemble de centres de congrès, chacun composé de plusieurs éléments (salles, espaces de restauration, etc.) configurables par un gestionnaire. Ces éléments peuvent être réservés séparément ou en totalité par un ou plusieurs événements.

## Fonctionnalités implémentées

- Gestion des centres de congrès et de leurs éléments (salles, restauration)
- Gestion des réservations avec statuts (En_attente, Confirmé, Annulé)
- Confirmation et annulation de réservations avec règles métier
- Calcul automatique du prix selon les tarifs et le nombre de participants
- Vérification de disponibilité des éléments sur une période donnée
- Gestion des indisponibilités (travaux, maintenance, etc.)
- Gestion des options (matériel et prestations) liées aux réservations
- Gestion des événements liés aux réservations

## Diagramme de classes

Le diagramme de classes a été conçu et modélisé avec **BESSER**.

### Classes principales

| Classe | Description |
|--------|-------------|
| Gestionnaire | Gère les centres, les réservations et les disponibilités |
| Centre_de_congres | Représente un centre avec ses éléments |
| Element | Salle ou espace réservable (capacité max, durée minimale) |
| Salle | Sous-classe d'Element avec superficie et type |
| EspaceRestauration | Sous-classe d'Element avec type de restauration |
| Reservation | Réservation d'un ou plusieurs éléments pour une période |
| Indisponibilite | Période d'indisponibilité d'un élément |
| Tarif | Grille tarifaire selon le nombre de participants |
| Evenement | Événement lié à une réservation |
| Option | Option réservable (matériel ou prestation) |
| Materiel | Sous-classe d'Option (vidéo-projecteur, micro, etc.) |
| Prestation | Sous-classe d'Option (pause café, lunch, etc.) |

### Énumération

| Type | Valeurs |
|------|---------|
| StatusReservation | En_attente, Confirmé, Annulé |

## Choix de modélisation

- **Héritage** : `Salle` et `EspaceRestauration` héritent d'`Element` pour factoriser les attributs communs (nom, capacité max, durée minimale). De même, `Materiel` et `Prestation` héritent d'`Option`.
- **delaiConf** dans `Reservation` : configurable par réservation comme demandé dans le cahier des charges.
- **dureeMin** dans `Element` : permet de définir une durée minimale de réservation par élément.
- **salleEvenement** dans `Indisponibilite` : booléen indiquant si l'indisponibilité est liée à un événement en salle.
- **Conservation des données** : Les réservations passées et annulées sont conservées en base pour les statistiques.

## Technologies utilisées

| Technologie | Usage |
|-------------|-------|
| Java | Langage principal |
| BESSER | Modélisation UML |
| Git | Versionnement |

## Auteur

**Brenda TANON** - ISTIC L3 Informatique
