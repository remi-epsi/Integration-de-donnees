
/* Création de la table de log

CREATE TABLE log_codeVille2 (
    nom VARCHAR(50),
    date DATE
);

*/

USE [Information]
GO

SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO

ALTER TRIGGER [dbo].[Trigger_CodeVille]
   ON [dbo].[Code_ville]
   AFTER INSERT
AS 
BEGIN
	-- SET NOCOUNT ON added to prevent extra result sets from
	-- interfering with SELECT statements.
	SET NOCOUNT ON;

    INSERT INTO log_codeville2 (nom, date) VALUES (SUSER_SNAME(), GETDATE()) 

END