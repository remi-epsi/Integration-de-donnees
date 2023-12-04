CREATE VIEW vue_departement_59_62 AS
SELECT [code_commune_INSEE]
      ,[Nom_de_la_commune]
      ,[Code_postal]
  FROM [Information].[dbo].[Code_ville]
  where code_commune_INSEE like '59%' or code_commune_INSEE like '62%'

  Select * from vue_departement_59_62