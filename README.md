# Flask_Postgresql

#### A project aimed at implementing the same Flask Project with different databases.

The website is hosted in heroku and uses Heroku-Postgres as the database. It makes use of psycog2 python module to connect to the local postgres server. This can be done by setting the 
DATABASE_URL as postgresql://userame:password@localhost:port/database_name.

While deploying on Heroku , One thing to take care is that by default the DATABASE_URL dialect set by Heroku will be "postgres://" and not "postgresql://". This will become an issue as heroku requires the latter, the 
corresponding changes must be done in the code.
