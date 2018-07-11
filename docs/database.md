<aside class="notice">
Current settings in the api module are set to ignore tables that are not backed by a model.

You have been warned.
</aside>

## Managing database fixtures

Alembic, via Flask-Migrate is used to manage our database. Changes to the models are put into a revision history.

To create a model update for the database do the following:

```bash
cd api
python manage.py db migrate
git add migrations
# git commit / push / pull to GitHub
python manage.py db upgrade
```

1. cd to the root director of the component
- cd api
2. python manage.py db migrate
- this will add a new revision into the migrations/versions directory
3. Add the migrations to GitHub
4. python manage.py db upgrade
- this will upgrade the database to support your new model

### Manual changes to the DB
If you need to add fixture data (eg.a lookup table with default values) then you can add them to your revision of the model *or* make a new revsion and add your changes to that file.

To make a new revision file:
```bash
python manage.py db revsion -m 'short name of your revision'
```

### Want to know the Head or current revsion?
You can ask Alembic for the latest version:
```bash
python manage.py db revision
```
