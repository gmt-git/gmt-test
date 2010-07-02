--------
-- Вообще хотел такую конструкцию записать в файл,
-- но sqlite3 не поддерживает ALERT COLUMN
--------

-- BEGIN TRANSACTION;
-- ALTER TABLE "hello_httpreqs" ADD COLUMN "priority" integer;
-- UPDATE "hello_httpreqs" SET "priority"=0;
-- ALTER TABLE "hello_httpreqs" ALTER COLUMN "priority" SET NOT NULL;
-- COMMIT;

--------
-- Поэтому пишу следующую, хотя не совсем соответствует тому,
-- что выдает ./manage.py sql hello 
--------

ALTER TABLE "hello_httpreqs" ADD COLUMN "priority" integer NOT NULL DEFAULT 0;
