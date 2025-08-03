# Déploiement sur Render

## Prérequis

1. Compte Render.com
2. Repository Git (GitHub, GitLab, etc.)

## Étapes de déploiement

### 1. Préparer le repository

Assurez-vous que tous les fichiers de configuration sont présents :
- `build.sh`
- `requirements.txt`
- `render.yaml`
- `runtime.txt`

### 2. Déployer sur Render

#### Option A : Déploiement automatique avec render.yaml

1. Connectez votre repository GitHub à Render
2. Render détectera automatiquement le fichier `render.yaml`
3. Cliquez sur "Create New Service" → "Blueprint"
4. Sélectionnez votre repository
5. Render créera automatiquement :
   - La base de données PostgreSQL
   - Le service web Django

#### Option B : Déploiement manuel

1. **Créer la base de données** :
   - New → PostgreSQL
   - Nom : `ar-targets-db`
   - Plan : Free

2. **Créer le service web** :
   - New → Web Service
   - Connecter votre repository
   - Configuration :
     - **Build Command** : `./build.sh`
     - **Start Command** : `gunicorn ar.wsgi:application`
     - **Environment** : Python 3

3. **Variables d'environnement** :
   ```
   PYTHON_VERSION=3.11.0
   DJANGO_SETTINGS_MODULE=ar.settings
   SECRET_KEY=<généré automatiquement>
   DATABASE_URL=<URL de la base de données>
   ALLOWED_HOSTS=.onrender.com
   DEBUG=false
   CORS_ALLOWED_ORIGINS=https://your-frontend-domain.com
   CORS_ALLOW_ALL_ORIGINS=false
   ```

### 3. Configuration CORS

Après le déploiement, mettez à jour les variables d'environnement :

1. Allez dans votre service web sur Render
2. Settings → Environment Variables
3. Mettez à jour `CORS_ALLOWED_ORIGINS` avec l'URL de votre frontend

### 4. Créer un superutilisateur

```bash
# Via Render Shell
render exec ar-targets-api python manage.py createsuperuser
```

## URLs de l'API

Une fois déployé, votre API sera accessible sur :
- **Base URL** : `https://your-app-name.onrender.com`
- **API Endpoints** :
  - `GET /api/targets/` - Liste des cibles AR
  - `POST /api/targets/` - Créer une cible
  - `GET /api/targets/{id}/` - Détails d'une cible
  - `GET /api/targets/stats/` - Statistiques
  - `POST /api/targets/{id}/upload_to_vuforia/` - Upload vers Vuforia

## Mise à jour du frontend

Mettez à jour l'URL de l'API dans votre frontend :

```typescript
// lib/api.ts
const API_BASE_URL = 'https://your-app-name.onrender.com/api';
```

## Monitoring

- **Logs** : Disponibles dans l'onglet "Logs" de votre service
- **Métriques** : CPU, mémoire, requêtes dans l'onglet "Metrics"
- **Base de données** : Monitoring dans l'onglet de la base de données

## Troubleshooting

### Erreurs communes

1. **Build failed** :
   - Vérifiez que `build.sh` est exécutable
   - Vérifiez les dépendances dans `requirements.txt`

2. **Database connection failed** :
   - Vérifiez que `DATABASE_URL` est correctement configuré
   - Vérifiez que la base de données est créée

3. **CORS errors** :
   - Vérifiez `CORS_ALLOWED_ORIGINS`
   - Assurez-vous que l'URL du frontend est incluse

4. **Static files not found** :
   - Vérifiez que `collectstatic` s'exécute correctement
   - Vérifiez la configuration WhiteNoise

### Commandes utiles

```bash
# Voir les logs
render logs ar-targets-api

# Accéder au shell
render exec ar-targets-api bash

# Redémarrer le service
render restart ar-targets-api
``` 