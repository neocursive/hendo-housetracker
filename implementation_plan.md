# Restructure to Flask Application Factory

This plan outlines the steps to refactor the monolithic `app.py` into a highly scalable Flask Application Factory using Blueprints. This will set the foundation for building the multi-component financial pipeline (paychecks, buckets, discretionary spending, etc.).

## User Review Required

> \[!IMPORTANT]
> Your database connection string (`postgresql://admin:Magic...`) is currently hardcoded directly in `app.py`. As part of this refactor, I will move this to a secure `.env` file so that your password is never accidentally uploaded to GitHub.

> \[!NOTE]
> All existing HTML templates will be moved into an `app/templates` folder, but their contents will remain completely unchanged.

## Open Questions

None at this time. The current grocery tracker logic is straightforward and will map perfectly to a Blueprint.

## Proposed Changes

We will break `app.py` apart into the following modular structure:

### Configuration & Entry Point

The root of your project will contain the server start file and configuration settings.

#### [NEW] [config.py](file:///C:/Users/eddik/Documents/antigravity/housetrack-hendo/config.py)

Will contain a `Config` class that loads your database connection string securely from environment variables.

#### [NEW] [run.py](file:///C:/Users/eddik/Documents/antigravity/housetrack-hendo/run.py)

The new entry point to start the server. It will import the factory function and run the app.

***

### Application Core (`app/` directory)

This is where the actual application factory lives.

#### [NEW] [app/__init__.py](file:///C:/Users/eddik/Documents/antigravity/housetrack-hendo/app/__init__.py)

Will contain the `db = SQLAlchemy()` object and the `create_app()` factory function. The factory will initialize the database and register our Blueprints.

#### [NEW] [app/models.py](file:///C:/Users/eddik/Documents/antigravity/housetrack-hendo/app/models.py)

Will contain your `Trip` and `TripItem` SQLAlchemy models. (Later, we will add `Paycheck`, `Bucket`, etc. here).

***

### Groceries Blueprint (`app/groceries/` directory)

We will encapsulate all of your existing grocery code into its own independent "Blueprint" module.

#### [NEW] [app/groceries/__init__.py](file:///C:/Users/eddik/Documents/antigravity/housetrack-hendo/app/groceries/__init__.py)

Initializes the `groceries_bp` Blueprint object.

#### [NEW] [app/groceries/routes.py](file:///C:/Users/eddik/Documents/antigravity/housetrack-hendo/app/groceries/routes.py)

Will contain all of your current `@app.route` functions (e.g., `/`, `/trip/<id>`, `/delete-item/<id>`), updated to use `@groceries_bp.route`.

***

### Cleanup

#### [DELETE] [app.py](file:///C:/Users/eddik/Documents/antigravity/housetrack-hendo/app.py)

Once the above structure is in place, the original monolithic file will be deleted.

## Verification Plan

### Automated/Local Tests

* I will install the required Python packages (`Flask`, `Flask-SQLAlchemy`, `python-dotenv`, `psycopg2`).

* I will run `python run.py` locally to ensure the server starts without circular imports.

* I will verify the grocery routes load correctly and that the database connects successfully.

